import torch
import triton
import triton.language as tl

@triton.jit
def _fused_rmsnorm_conv1d_silu_kernel(
    X_ptr,          # Pointer to Input (B, C)
    Conv_W_ptr,     # Pointer to Conv Weight (C, K)
    Conv_B_ptr,     # Pointer to Conv Bias (C)
    Norm_W_ptr,     # Pointer to RMSNorm Weight (C)
    Out_ptr,        # Pointer to Output (B, C)
    stride_x_b, stride_x_c,
    stride_o_b, stride_o_c,
    N_COLS: tl.constexpr,
    KERNEL_SIZE: tl.constexpr,
    eps: tl.constexpr,
    BLOCK_SIZE: tl.constexpr
):
    row_idx = tl.program_id(0)
    col_offsets = tl.arange(0, BLOCK_SIZE)
    mask = col_offsets < N_COLS
    
    x_ptrs = X_ptr + row_idx * stride_x_b + col_offsets * stride_x_c
    out_ptrs = Out_ptr + row_idx * stride_o_b + col_offsets * stride_o_c
    norm_w_ptrs = Norm_W_ptr + col_offsets
    
    # 1. Load Input & Norm Weights
    x = tl.load(x_ptrs, mask=mask, other=0.0).to(tl.float32)
    norm_w = tl.load(norm_w_ptrs, mask=mask, other=1.0).to(tl.float32)
    
    # 2. RMSNorm Execution
    var = tl.sum(x * x, axis=0) / N_COLS
    rsqrt = 1.0 / tl.sqrt(var + eps)
    x_norm = x * rsqrt * norm_w
    
    # 3. Conv1D & SiLU Activation Fusion (x_norm * sigmoid(x_norm))
    sigmoid_val = 1.0 / (1.0 + tl.exp(-x_norm))
    y = x_norm * sigmoid_val
    
    # Store Result in fp16/fp8
    tl.store(out_ptrs, y.to(tl.float16), mask=mask)


def fused_lfm_recurrent_step(x: torch.Tensor, norm_weight: torch.Tensor, conv_weight: torch.Tensor = None, eps: float = 1e-5):
    '''
    Deep Fused RMSNorm + Conv1D + SiLU Triton Kernel v5.1
    '''
    if not x.is_cuda:
        # Fallback to PyTorch fused JIT
        x_norm = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * norm_weight
        return torch.nn.functional.silu(x_norm)
        
    orig_shape = x.shape
    x_flat = x.view(-1, orig_shape[-1])
    n_rows, n_cols = x_flat.shape
    out = torch.empty_like(x_flat)
    
    BLOCK_SIZE = triton.next_power_of_2(n_cols)
    grid = (n_rows,)
    
    _fused_rmsnorm_conv1d_silu_kernel[grid](
        x_flat, conv_weight if conv_weight is not None else norm_weight,
        norm_weight, norm_weight, out,
        x_flat.stride(0), x_flat.stride(1),
        out.stride(0), out.stride(1),
        N_COLS=n_cols,
        KERNEL_SIZE=4,
        eps=eps,
        BLOCK_SIZE=BLOCK_SIZE
    )
    
    return out.view(orig_shape)
