import torch
import triton
import triton.language as tl

@triton.jit
def _fused_short_conv_update_kernel(
    bcx_ptr,           # [num_tokens, 3 * dim]
    state_ptr,         # [num_blocks, dim, L_cache] or [num_blocks, L_cache, dim]
    weights_ptr,       # [dim, L_cache]
    bias_ptr,          # [dim]
    y_ptr,             # [num_tokens, dim]
    state_indices_ptr, # [num_tokens]
    stride_bcx_tok, stride_bcx_dim,
    stride_state_blk, stride_state_dim, stride_state_l,
    stride_weights_dim, stride_weights_l,
    stride_y_tok, stride_y_dim,
    dim, L_cache: tl.constexpr,
    BLOCK_SIZE_DIM: tl.constexpr
):
    pid_tok = tl.program_id(0)
    pid_dim = tl.program_id(1)
    
    state_idx = tl.load(state_indices_ptr + pid_tok)
    
    dim_offset = pid_dim * BLOCK_SIZE_DIM + tl.arange(0, BLOCK_SIZE_DIM)
    mask_dim = dim_offset < dim
    
    b_ptr = bcx_ptr + pid_tok * stride_bcx_tok + dim_offset * stride_bcx_dim
    c_ptr = bcx_ptr + pid_tok * stride_bcx_tok + (dim + dim_offset) * stride_bcx_dim
    x_ptr = bcx_ptr + pid_tok * stride_bcx_tok + (2 * dim + dim_offset) * stride_bcx_dim
    
    b = tl.load(b_ptr, mask=mask_dim)
    c = tl.load(c_ptr, mask=mask_dim)
    x = tl.load(x_ptr, mask=mask_dim)
    
    bx = b * x
    bx_f32 = bx.to(tl.float32)
    
    state_base = state_ptr + state_idx * stride_state_blk
    
    dot_acc = tl.zeros([BLOCK_SIZE_DIM], dtype=tl.float32)
    
    for i in range(L_cache - 1):
        val = tl.load(state_base + dim_offset * stride_state_dim + (i + 1) * stride_state_l, mask=mask_dim)
        tl.store(state_base + dim_offset * stride_state_dim + i * stride_state_l, val, mask=mask_dim)
        
        w = tl.load(weights_ptr + dim_offset * stride_weights_dim + i * stride_weights_l, mask=mask_dim)
        dot_acc += val.to(tl.float32) * w.to(tl.float32)
        
    tl.store(state_base + dim_offset * stride_state_dim + (L_cache - 1) * stride_state_l, bx, mask=mask_dim)
    
    w_last = tl.load(weights_ptr + dim_offset * stride_weights_dim + (L_cache - 1) * stride_weights_l, mask=mask_dim)
    dot_acc += bx_f32 * w_last.to(tl.float32)
    
    bias = tl.load(bias_ptr + dim_offset, mask=mask_dim)
    dot_acc += bias.to(tl.float32)
    
    y = c.to(tl.float32) * dot_acc
    y_out = y.to(bcx_ptr.dtype.element_ty)
    
    y_out_ptr = y_ptr + pid_tok * stride_y_tok + dim_offset * stride_y_dim
    tl.store(y_out_ptr, y_out, mask=mask_dim)

def fused_lfm_short_conv_update(bcx, conv_state, conv_weights, conv_bias, state_indices):
    num_tokens = bcx.size(0)
    dim = conv_weights.size(0)
    L_cache = conv_weights.size(1)
    
    y = torch.empty((num_tokens, dim), device=bcx.device, dtype=bcx.dtype)
    
    BLOCK_SIZE_DIM = triton.next_power_of_2(dim) if dim < 1024 else 1024
    grid = lambda meta: (num_tokens, triton.cdiv(dim, meta['BLOCK_SIZE_DIM']))
    
    _fused_short_conv_update_kernel[grid](
        bcx, conv_state, conv_weights, conv_bias, y, state_indices,
        bcx.stride(0), bcx.stride(1),
        conv_state.stride(0), conv_state.stride(1), conv_state.stride(2),
        conv_weights.stride(0), conv_weights.stride(1),
        y.stride(0), y.stride(1),
        dim, L_cache,
        BLOCK_SIZE_DIM=BLOCK_SIZE_DIM
    )
    return y
