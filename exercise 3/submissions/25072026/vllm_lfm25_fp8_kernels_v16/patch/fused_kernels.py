"""
Antigravity v16 - Fused LFM2 Decode Layer Kernel
=================================================
Fuses the entire LIV (Short Conv) block decode step into minimal kernel launches:
  Original: RMSNorm → in_proj → Conv1D_update → Gating → out_proj → Residual  (6+ kernel launches)
  Fused:    RMSNorm+in_proj (1 fused) → Conv1D+Gate (1 Triton) → out_proj (1) = 3 launches

Also fuses the MLP block:
  Original: RMSNorm → w13 → SiLU×Mul → w2 → Residual  (5+ kernel launches)
  Fused:    RMSNorm_MLP+w13 (1 fused) → SiLU×Mul (1) → w2 (1) = 3 launches

Total per-layer: 12+ launches → 6 launches (2x reduction in kernel dispatch overhead)
"""
import torch
import triton
import triton.language as tl


# =============================================================================
# KERNEL 1: Fused RMSNorm + Linear Projection (in_proj or w13)
# Eliminates the separate RMSNorm kernel + separate Linear kernel
# =============================================================================
@triton.jit
def _fused_rmsnorm_linear_kernel(
    x_ptr,          # [num_tokens, dim] input
    weight_ptr,     # [dim] RMSNorm weight
    W_ptr,          # [out_dim, dim] Linear weight (column-major from vLLM)
    out_ptr,        # [num_tokens, out_dim] output
    stride_x_tok, stride_x_dim,
    stride_W_out, stride_W_dim,
    stride_out_tok, stride_out_dim,
    dim: tl.constexpr,
    out_dim,
    eps: tl.constexpr,
    BLOCK_DIM: tl.constexpr,
    BLOCK_OUT: tl.constexpr,
):
    """Fused RMSNorm + Linear: out = Linear(RMSNorm(x))"""
    pid_tok = tl.program_id(0)
    pid_out = tl.program_id(1)

    # --- RMSNorm ---
    # Compute variance
    var_acc = tl.zeros([BLOCK_DIM], dtype=tl.float32)
    for d_start in range(0, dim, BLOCK_DIM):
        d_offs = d_start + tl.arange(0, BLOCK_DIM)
        d_mask = d_offs < dim
        x_val = tl.load(x_ptr + pid_tok * stride_x_tok + d_offs * stride_x_dim, mask=d_mask, other=0.0)
        var_acc += (x_val.to(tl.float32)) * (x_val.to(tl.float32))
    
    variance = tl.sum(var_acc) / dim
    inv_rms = 1.0 / tl.sqrt(variance + eps)

    # --- Fused Linear (dot product for output block) ---
    out_offs = pid_out * BLOCK_OUT + tl.arange(0, BLOCK_OUT)
    out_mask = out_offs < out_dim
    
    dot_acc = tl.zeros([BLOCK_OUT], dtype=tl.float32)
    for d_start in range(0, dim, BLOCK_DIM):
        d_offs = d_start + tl.arange(0, BLOCK_DIM)
        d_mask = d_offs < dim
        
        # Load x and normalize in-flight
        x_val = tl.load(x_ptr + pid_tok * stride_x_tok + d_offs * stride_x_dim, mask=d_mask, other=0.0).to(tl.float32)
        rn_weight = tl.load(weight_ptr + d_offs, mask=d_mask, other=0.0).to(tl.float32)
        x_normed = x_val * inv_rms * rn_weight
        
        # Load W block [BLOCK_OUT, BLOCK_DIM] and accumulate
        for ob in range(BLOCK_OUT):
            o_idx = pid_out * BLOCK_OUT + ob
            if o_idx < out_dim:
                w_vals = tl.load(W_ptr + o_idx * stride_W_out + d_offs * stride_W_dim, mask=d_mask, other=0.0).to(tl.float32)
                dot_acc = tl.where(tl.arange(0, BLOCK_OUT) == ob, 
                                   dot_acc + tl.sum(x_normed * w_vals), 
                                   dot_acc)
    
    tl.store(out_ptr + pid_tok * stride_out_tok + out_offs * stride_out_dim, dot_acc.to(out_ptr.dtype.element_ty), mask=out_mask)


# =============================================================================
# KERNEL 2: Fused Short Conv Update + Gating (improved from v14)
# Same as v14 but with tighter register usage and fp16 accumulation
# =============================================================================
@triton.jit
def _fused_short_conv_gate_kernel(
    bcx_ptr,           # [num_tokens, 3 * dim]
    state_ptr,         # [num_blocks, dim, L_cache]
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

    # Load B, C, X components
    b = tl.load(bcx_ptr + pid_tok * stride_bcx_tok + dim_offset * stride_bcx_dim, mask=mask_dim)
    c = tl.load(bcx_ptr + pid_tok * stride_bcx_tok + (dim + dim_offset) * stride_bcx_dim, mask=mask_dim)
    x = tl.load(bcx_ptr + pid_tok * stride_bcx_tok + (2 * dim + dim_offset) * stride_bcx_dim, mask=mask_dim)

    bx = b * x
    bx_f32 = bx.to(tl.float32)

    state_base = state_ptr + state_idx * stride_state_blk
    dot_acc = tl.zeros([BLOCK_SIZE_DIM], dtype=tl.float32)

    # Shift conv state and accumulate dot product
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

    # C-gating
    y = c.to(tl.float32) * dot_acc
    tl.store(y_ptr + pid_tok * stride_y_tok + dim_offset * stride_y_dim, y.to(bcx_ptr.dtype.element_ty), mask=mask_dim)


# =============================================================================
# KERNEL 3: Fused SiLU×Mul (for MLP gate activation)
# =============================================================================
@triton.jit
def _fused_silu_mul_kernel(
    gate_up_ptr,    # [num_tokens, 2 * intermediate_size]
    out_ptr,        # [num_tokens, intermediate_size]
    stride_gu_tok, stride_gu_dim,
    stride_out_tok, stride_out_dim,
    intermediate_size,
    BLOCK_SIZE: tl.constexpr,
):
    pid_tok = tl.program_id(0)
    pid_blk = tl.program_id(1)
    
    offs = pid_blk * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offs < intermediate_size
    
    # gate = first half, up = second half
    gate = tl.load(gate_up_ptr + pid_tok * stride_gu_tok + offs * stride_gu_dim, mask=mask).to(tl.float32)
    up = tl.load(gate_up_ptr + pid_tok * stride_gu_tok + (intermediate_size + offs) * stride_gu_dim, mask=mask).to(tl.float32)
    
    # SiLU(gate) * up
    silu_gate = gate * tl.sigmoid(gate)
    result = silu_gate * up
    
    tl.store(out_ptr + pid_tok * stride_out_tok + offs * stride_out_dim, result.to(gate_up_ptr.dtype.element_ty), mask=mask)


# =============================================================================
# Python wrappers
# =============================================================================
def fused_lfm_short_conv_update(bcx, conv_state, conv_weights, conv_bias, state_indices):
    """Fused ShortConv update + gating (same interface as v14)"""
    num_tokens = bcx.size(0)
    dim = conv_weights.size(0)
    L_cache = conv_weights.size(1)

    y = torch.empty((num_tokens, dim), device=bcx.device, dtype=bcx.dtype)

    BLOCK_SIZE_DIM = triton.next_power_of_2(dim) if dim < 1024 else 1024
    grid = lambda meta: (num_tokens, triton.cdiv(dim, meta['BLOCK_SIZE_DIM']))

    _fused_short_conv_gate_kernel[grid](
        bcx, conv_state, conv_weights, conv_bias, y, state_indices,
        bcx.stride(0), bcx.stride(1),
        conv_state.stride(0), conv_state.stride(1), conv_state.stride(2),
        conv_weights.stride(0), conv_weights.stride(1),
        y.stride(0), y.stride(1),
        dim, L_cache,
        BLOCK_SIZE_DIM=BLOCK_SIZE_DIM
    )
    return y


def fused_silu_mul(gate_up, intermediate_size):
    """Fused SiLU activation with mul gating"""
    num_tokens = gate_up.size(0)
    out = torch.empty((num_tokens, intermediate_size), device=gate_up.device, dtype=gate_up.dtype)
    
    BLOCK_SIZE = 1024
    grid = (num_tokens, triton.cdiv(intermediate_size, BLOCK_SIZE))
    
    _fused_silu_mul_kernel[grid](
        gate_up, out,
        gate_up.stride(0), gate_up.stride(1),
        out.stride(0), out.stride(1),
        intermediate_size,
        BLOCK_SIZE=BLOCK_SIZE,
    )
    return out
