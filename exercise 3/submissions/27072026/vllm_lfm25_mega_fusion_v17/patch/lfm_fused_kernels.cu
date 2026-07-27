#include <torch/extension.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <cuda_fp16.h>
#include <cuda_bf16.h>
#include <stdexcept>

template <typename bcx_t, typename state_t>
__global__ void fused_short_conv_update_dual_dtype_kernel(
    const bcx_t* __restrict__ bcx,
    state_t* __restrict__ state,
    const bcx_t* __restrict__ weights,
    const bcx_t* __restrict__ bias,
    bcx_t* __restrict__ y,
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
            *(y + pid_tok * stride_y_tok + pid_dim * stride_y_dim) = static_cast<bcx_t>(0.0f);
            return;
        }

        const bcx_t* b_ptr = bcx + pid_tok * stride_bcx_tok + pid_dim * stride_bcx_dim;
        const bcx_t* c_ptr = bcx + pid_tok * stride_bcx_tok + (dim + pid_dim) * stride_bcx_dim;
        const bcx_t* x_ptr = bcx + pid_tok * stride_bcx_tok + (2 * dim + pid_dim) * stride_bcx_dim;

        float b = static_cast<float>(*b_ptr);
        float c = static_cast<float>(*c_ptr);
        float x = static_cast<float>(*x_ptr);

        float bx = b * x;

        // Correct pointer offset based on state_t element size (Float32 or Half/BFloat16)
        state_t* state_base = state + state_idx * stride_state_blk + pid_dim * stride_state_dim;
        const bcx_t* weights_base = weights + pid_dim * stride_weights_dim;

        float dot_acc = 0.0f;

        if (L_cache > 0) {
            #pragma unroll
            for (int i = 0; i < L_cache - 1; ++i) {
                state_t val = *(state_base + (i + 1) * stride_state_l);
                *(state_base + i * stride_state_l) = val; // shift in state_t precision

                float w = static_cast<float>(*(weights_base + i * stride_weights_l));
                dot_acc += static_cast<float>(val) * w;
            }

            *(state_base + (L_cache - 1) * stride_state_l) = static_cast<state_t>(bx);

            float w_last = static_cast<float>(*(weights_base + (L_cache - 1) * stride_weights_l));
            dot_acc += bx * w_last;
        }

        // Add bias safely only if bias pointer is valid CUDA memory
        float b_val = (bias != nullptr) ? static_cast<float>(*(bias + pid_dim * stride_bias)) : 0.0f;
        dot_acc += b_val;

        float out = c * dot_acc;

        *(y + pid_tok * stride_y_tok + pid_dim * stride_y_dim) = static_cast<bcx_t>(out);
    }
}

torch::Tensor fused_lfm_short_conv_update(
    torch::Tensor bcx,
    torch::Tensor state,
    torch::Tensor weights,
    torch::Tensor bias,
    torch::Tensor state_indices
) {
    // Safety check for undefined tensors to prevent PyBind11 segfaults
    if (!bcx.defined() || !state.defined() || !weights.defined() || !state_indices.defined()) {
        throw std::invalid_argument("One or more required input tensors to fused_lfm_short_conv_update are undefined/None");
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

    // Strict CUDA pointer check: Ensure bias is valid, non-empty, and on CUDA device
    bool has_valid_bias = bias.defined() && bias.numel() > 0 && bias.is_cuda();
    const void* bias_ptr = has_valid_bias ? bias.data_ptr() : nullptr;
    int bias_stride = has_valid_bias ? bias.stride(0) : 0;

    // DUAL-TYPE DISPATCH: Handle bcx dtype (BFloat16/Half) and state dtype (Float32/BFloat16) independently!
    AT_DISPATCH_FLOATING_TYPES_AND2(at::ScalarType::Half, at::ScalarType::BFloat16, bcx.scalar_type(), "bcx_dispatch", ([&] {
        using bcx_t = scalar_t;
        AT_DISPATCH_FLOATING_TYPES_AND2(at::ScalarType::Half, at::ScalarType::BFloat16, state.scalar_type(), "state_dispatch", ([&] {
            using state_t = scalar_t;
            fused_short_conv_update_dual_dtype_kernel<bcx_t, state_t><<<grid, threads>>>(
                bcx.data_ptr<bcx_t>(),
                state.data_ptr<state_t>(),
                weights.data_ptr<bcx_t>(),
                static_cast<const bcx_t*>(bias_ptr),
                y.data_ptr<bcx_t>(),
                state_indices_32.data_ptr<int32_t>(),
                num_tokens, dim, L_cache, num_blocks,
                bcx.stride(0), bcx.stride(1),
                state.stride(0), state.stride(1), state.stride(2),
                weights.stride(0), weights.stride(1),
                y.stride(0), y.stride(1),
                bias_stride
            );
        }));
    }));

    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        throw std::runtime_error(std::string("CUDA Error: ") + cudaGetErrorString(err));
    }

    return y;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("fused_lfm_short_conv_update", &fused_lfm_short_conv_update, "Dual-Type Vectorized Fused LFM Short Conv Update (CUDA)");
}
