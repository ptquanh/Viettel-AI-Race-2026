import torch
import triton
import triton.language as tl

@triton.jit
def _fused_rmsnorm_silu_kernel(
    X_ptr,          # Pointer to Input
    W_ptr,          # Pointer to Weight (Norm)
    Out_ptr,        # Pointer to Output
    stride_x_batch, # Stride of X batch
    stride_x_dim,   # Stride of X dim
    stride_o_batch, # Stride of Out batch
    stride_o_dim,   # Stride of Out dim
    N_COLS: tl.constexpr,
    eps: tl.constexpr,
    BLOCK_SIZE: tl.constexpr
):
    # Program ID
    row_idx = tl.program_id(0)
    
    # Offsets
    col_offsets = tl.arange(0, BLOCK_SIZE)
    mask = col_offsets < N_COLS
    
    # Pointers
    x_ptrs = X_ptr + row_idx * stride_x_batch + col_offsets * stride_x_dim
    w_ptrs = W_ptr + col_offsets
    out_ptrs = Out_ptr + row_idx * stride_o_batch + col_offsets * stride_o_dim
    
    # Load input & weights
    x = tl.load(x_ptrs, mask=mask, other=0.0).to(tl.float32)
    w = tl.load(w_ptrs, mask=mask, other=1.0).to(tl.float32)
    
    # RMS Norm calculation
    var = tl.sum(x * x, axis=0) / N_COLS
    rsqrt = 1.0 / tl.sqrt(var + eps)
    x_norm = x * rsqrt * w
    
    # SiLU Activation: x * sigmoid(x)
    sigmoid_x = 1.0 / (1.0 + tl.exp(-x_norm))
    y = x_norm * sigmoid_x
    
    # Store output
    tl.store(out_ptrs, y.to(tl.float16), mask=mask)


def fused_rmsnorm_silu_triton(x: torch.Tensor, weight: torch.Tensor, eps: float = 1e-5):
    '''
    Fused RMSNorm + SiLU Triton Kernel Wrapper
    '''
    if not x.is_cuda:
        return torch.nn.functional.silu(x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * weight)
        
    orig_shape = x.shape
    x_flat = x.view(-1, orig_shape[-1])
    n_rows, n_cols = x_flat.shape
    out = torch.empty_like(x_flat)
    
    BLOCK_SIZE = triton.next_power_of_2(n_cols)
    grid = (n_rows,)
    
    _fused_rmsnorm_silu_kernel[grid](
        x_flat, weight, out,
        x_flat.stride(0), x_flat.stride(1),
        out.stride(0), out.stride(1),
        N_COLS=n_cols,
        eps=eps,
        BLOCK_SIZE=BLOCK_SIZE
    )
    
    return out.view(orig_shape)
