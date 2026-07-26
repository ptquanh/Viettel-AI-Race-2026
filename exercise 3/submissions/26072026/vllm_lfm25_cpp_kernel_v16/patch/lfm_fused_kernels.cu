#include <torch/extension.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <cuda_fp16.h>
#include <cuda_bf16.h>

template <typename scalar_t>
__global__ void fused_short_conv_update_kernel(
    const scalar_t* __restrict__ bcx,
    scalar_t* __restrict__ state,
    const scalar_t* __restrict__ weights,
    const scalar_t* __restrict__ bias,
    scalar_t* __restrict__ y,
    const int32_t* __restrict__ state_indices,
    const int num_tokens,
    const int dim,
    const int L_cache,
    const int num_blocks,
    const int stride_bcx_tok, const int stride_bcx_dim,
    const int stride_state_blk, const int stride_state_dim, const int stride_state_l,
    const int stride_weights_dim, const int stride_weights_l,
    const int stride_y_tok, const int stride_y_dim,
    const int stride_bias
) {
    int pid_tok = blockIdx.x;
    int pid_dim = threadIdx.x + blockIdx.y * blockDim.x;

    if (pid_tok < num_tokens && pid_dim < dim) {
        int32_t state_idx = state_indices[pid_tok];

        // Bounds check to prevent CUDA illegal memory access
        if (state_idx < 0 || state_idx >= num_blocks) {
            *(y + pid_tok * stride_y_tok + pid_dim * stride_y_dim) = static_cast<scalar_t>(0.0f);
            return;
        }

        const scalar_t* b_ptr = bcx + pid_tok * stride_bcx_tok + pid_dim * stride_bcx_dim;
        const scalar_t* c_ptr = bcx + pid_tok * stride_bcx_tok + (dim + pid_dim) * stride_bcx_dim;
        const scalar_t* x_ptr = bcx + pid_tok * stride_bcx_tok + (2 * dim + pid_dim) * stride_bcx_dim;

        float b = static_cast<float>(*b_ptr);
        float c = static_cast<float>(*c_ptr);
        float x = static_cast<float>(*x_ptr);

        float bx = b * x;

        scalar_t* state_base = state + state_idx * stride_state_blk + pid_dim * stride_state_dim;
        const scalar_t* weights_base = weights + pid_dim * stride_weights_dim;

        float dot_acc = 0.0f;

        if (L_cache > 0) {
            for (int i = 0; i < L_cache - 1; ++i) {
                scalar_t val = *(state_base + (i + 1) * stride_state_l);
                *(state_base + i * stride_state_l) = val; // shift

                float w = static_cast<float>(*(weights_base + i * stride_weights_l));
                dot_acc += static_cast<float>(val) * w;
            }

            *(state_base + (L_cache - 1) * stride_state_l) = static_cast<scalar_t>(bx);

            float w_last = static_cast<float>(*(weights_base + (L_cache - 1) * stride_weights_l));
            dot_acc += bx * w_last;
        }

        // Add bias
        float b_val = static_cast<float>(*(bias + pid_dim * stride_bias));
        dot_acc += b_val;

        float out = c * dot_acc;

        *(y + pid_tok * stride_y_tok + pid_dim * stride_y_dim) = static_cast<scalar_t>(out);
    }
}

torch::Tensor fused_lfm_short_conv_update(
    torch::Tensor bcx,
    torch::Tensor state,
    torch::Tensor weights,
    torch::Tensor bias,
    torch::Tensor state_indices
) {
    // Thao tác an toàn: Kiểm tra nếu bất kỳ tensor nào chưa định nghĩa (dạng Undefined/None từ PyBind11)
    if (!bcx.defined() || !state.defined() || !weights.defined() || !bias.defined() || !state_indices.defined()) {
        throw std::invalid_argument("One or more input tensors to fused_lfm_short_conv_update are undefined/None");
    }

    if (bcx.size(0) == 0) {
        return torch::empty({0, weights.size(0)}, bcx.options());
    }

    int num_tokens = bcx.size(0);
    int dim = weights.size(0);
    int L_cache = weights.size(1);
    int num_blocks = state.size(0);

    auto y = torch::empty({num_tokens, dim}, bcx.options());
    auto state_indices_32 = state_indices.to(torch::kInt32).contiguous();

    int threads = 256;
    int blocks_dim = (dim + threads - 1) / threads;
    dim3 grid(num_tokens, blocks_dim);

    AT_DISPATCH_FLOATING_TYPES_AND2(at::ScalarType::Half, at::ScalarType::BFloat16, bcx.scalar_type(), "fused_short_conv_update_kernel", ([&] {
        fused_short_conv_update_kernel<scalar_t><<<grid, threads>>>(
            bcx.data_ptr<scalar_t>(),
            state.data_ptr<scalar_t>(),
            weights.data_ptr<scalar_t>(),
            bias.data_ptr<scalar_t>(),
            y.data_ptr<scalar_t>(),
            state_indices_32.data_ptr<int32_t>(),
            num_tokens, dim, L_cache, num_blocks,
            bcx.stride(0), bcx.stride(1),
            state.stride(0), state.stride(1), state.stride(2),
            weights.stride(0), weights.stride(1),
            y.stride(0), y.stride(1),
            bias.stride(0)
        );
    }));

    // Check for CUDA errors
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        throw std::runtime_error(std::string("CUDA Error: ") + cudaGetErrorString(err));
    }

    return y;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("fused_lfm_short_conv_update", &fused_lfm_short_conv_update, "Fused LFM Short Conv Update (CUDA)");
}
