"""
Antigravity v21.0 - Online INT4 Weight Quantization + Marlin/Triton GEMM

Implements:
1. RTN (Round-To-Nearest) symmetric INT4 quantization of FP8/FP16 weights
2. INT4 → INT32 packing (8 values per INT32)
3. Marlin-format repacking (if available) for optimal GEMM performance
4. Custom Triton INT4 matmul kernel as fallback

This is "online quantization" - weights are quantized at model load time,
not pre-baked into the Docker image.
"""

import sys
import torch
import torch.nn.functional as F
import triton
import triton.language as tl

# ============================================================================
# SECTION 1: INT4 Quantization Utilities
# ============================================================================

def quantize_symmetric_int4(weight_fp16, group_size=128):
    """
    Quantize FP16 weight to symmetric INT4 with per-group scales.
    
    Args:
        weight_fp16: [N, K] FP16 weight tensor (PyTorch layout: [out, in])
        group_size: number of elements per quantization group along K
    
    Returns:
        w_int4: [N, K] INT8 tensor with values in [-8, 7]
        scales: [N, num_groups] FP16 per-group scale factors
    """
    N, K = weight_fp16.shape
    
    # Pad K to multiple of group_size if needed
    if K % group_size != 0:
        pad_k = group_size - (K % group_size)
        weight_fp16 = F.pad(weight_fp16, (0, pad_k))
        K = weight_fp16.shape[1]
    
    num_groups = K // group_size
    
    # Reshape to [N, num_groups, group_size]
    w_groups = weight_fp16.reshape(N, num_groups, group_size)
    
    # Compute per-group scales: max absolute value / 7
    max_abs = w_groups.abs().amax(dim=2)  # [N, num_groups]
    scales = (max_abs / 7.0).clamp(min=1e-8).to(torch.float16)  # [N, num_groups]
    
    # Quantize: round(w / scale) clamped to [-8, 7]
    w_q = torch.round(w_groups / scales.unsqueeze(2)).clamp(-8, 7).to(torch.int8)
    w_q = w_q.reshape(N, K)
    
    return w_q, scales


def pack_int4_to_int32(w_int4):
    """
    Pack INT4 values into INT32 tensors (8 values per INT32).
    Packing is along K dimension (dim=1).
    
    Args:
        w_int4: [N, K] INT8 tensor with INT4 values [-8, 7]
    
    Returns:
        w_packed: [N, K//8] INT32 tensor
    """
    N, K = w_int4.shape
    assert K % 8 == 0, f"K={K} must be divisible by 8"
    
    # Shift to unsigned [0, 15] for packing
    w_unsigned = (w_int4.to(torch.int32) + 8) & 0xF  # [N, K]
    
    # Reshape for efficient packing: [N, K//8, 8]
    w_groups = w_unsigned.reshape(N, K // 8, 8)
    
    # Pack 8 INT4 values into INT32
    w_packed = torch.zeros(N, K // 8, dtype=torch.int32, device=w_int4.device)
    for i in range(8):
        w_packed |= w_groups[:, :, i] << (4 * i)
    
    return w_packed


def quantize_and_pack(weight, group_size=128):
    """
    Full pipeline: FP16/FP8/BF16 weight → INT4 packed + scales.
    
    Args:
        weight: [N, K] weight tensor (any floating point dtype)
        group_size: quantization group size
    
    Returns:
        w_packed: [N, K_padded//8] INT32 packed weights
        scales: [N, num_groups] FP16 scales
        K_padded: padded K dimension (for GEMM size parameter)
    """
    # Convert to FP16 for quantization
    w_fp16 = weight.data.to(torch.float16)
    N, K_orig = w_fp16.shape
    
    # Pad K to multiple of max(group_size, 8)
    align = max(group_size, 8)
    if K_orig % align != 0:
        pad_k = align - (K_orig % align)
        w_fp16 = F.pad(w_fp16, (0, pad_k))
    
    K_padded = w_fp16.shape[1]
    
    # Quantize
    w_int4, scales = quantize_symmetric_int4(w_fp16, group_size)
    
    # Pack
    w_packed = pack_int4_to_int32(w_int4)
    
    return w_packed, scales, K_padded


# ============================================================================
# SECTION 2: Marlin GEMM (Fastest - uses Tensor Cores)
# ============================================================================

_marlin_available = None
_marlin_scalar_type = None

def check_marlin_available():
    """Check if Marlin GEMM ops are available in this vLLM build."""
    global _marlin_available, _marlin_scalar_type
    if _marlin_available is not None:
        return _marlin_available
    
    try:
        from vllm._C import ops as vllm_ops
        
        # Check for gptq_marlin_gemm
        if not hasattr(vllm_ops, 'gptq_marlin_gemm'):
            _marlin_available = False
            return False
        
        # Check for gptq_marlin_repack
        if not hasattr(vllm_ops, 'gptq_marlin_repack'):
            _marlin_available = False
            return False
        
        # Try to find the scalar type constant
        try:
            from vllm.scalar_type import scalar_type_uint4b8
            _marlin_scalar_type = scalar_type_uint4b8
        except ImportError:
            try:
                from vllm._C import ScalarType
                _marlin_scalar_type = ScalarType.uint4b8
            except (ImportError, AttributeError):
                try:
                    from vllm.model_executor.layers.quantization.utils.quant_utils import GPTQ_MARLIN_MIN_THREAD_N
                    # If this imports, Marlin is available but we need to find the type
                    _marlin_scalar_type = None  # Will try at runtime
                except ImportError:
                    pass
        
        _marlin_available = True
        print(f"[Antigravity v21.0] Marlin GEMM available! ScalarType: {_marlin_scalar_type}", file=sys.stderr)
        return True
        
    except Exception as e:
        print(f"[Antigravity v21.0] Marlin not available: {e}", file=sys.stderr)
        _marlin_available = False
        return False


def repack_for_marlin(w_packed, K, N):
    """
    Repack standard INT4 packed weights to Marlin-optimized layout.
    
    Args:
        w_packed: [N, K//8] INT32 (standard packing, weight layout [N, K])
        K: original (padded) K dimension
        N: output dimension
    
    Returns:
        w_marlin: repacked weight tensor for Marlin GEMM
    """
    from vllm._C import ops as vllm_ops
    
    # Marlin expects weights in [K//pack_factor, N] layout (transposed from our [N, K//8])
    w_packed_t = w_packed.t().contiguous()  # [K//8, N]
    
    # CRITICAL BUG FIX: If act_order is False, perm MUST be an empty tensor.
    # Passing torch.arange(K) tricks the C++ kernel into thinking act_order=True,
    # causing an immediate memory violation (Segmentation Fault) in gptq_marlin_repack!
    perm = torch.empty(0, dtype=torch.int32, device=w_packed.device)
    
    w_marlin = vllm_ops.gptq_marlin_repack(
        w_packed_t, perm, K, N, 4  # num_bits=4
    )
    
    return w_marlin


def marlin_gemm_forward(x, w_marlin, scales, bias, K, N):
    """
    Forward pass using Marlin GEMM kernel.
    
    Args:
        x: [M, K] FP16 input
        w_marlin: Marlin-repacked INT4 weights
        scales: [num_groups, N] FP16 scales (transposed from [N, num_groups])
        bias: [N] FP16 bias or None
        K: weight K dimension
        N: weight N dimension
    """
    from vllm._C import ops as vllm_ops
    
    M = x.shape[0]
    x_fp16 = x.to(torch.float16) if x.dtype != torch.float16 else x
    
    # Workspace buffer (required by Marlin)
    workspace = torch.zeros(N // 64 * 16, dtype=torch.int32, device=x.device)
    
    # Empty tensors for unused parameters
    empty_i32 = torch.empty(0, dtype=torch.int32, device=x.device)
    
    output = vllm_ops.gptq_marlin_gemm(
        x_fp16,
        w_marlin,
        scales,
        empty_i32,  # b_zeros (none for symmetric)
        empty_i32,  # g_idx (identity, already repacked)
        empty_i32,  # perm (identity, already repacked)
        workspace,
        _marlin_scalar_type,
        M, N, K,
        True,   # is_k_full
        False,  # has_zp
        True,   # use_fp32_reduce
    )
    
    if bias is not None:
        output = output + bias
    
    return output


# ============================================================================
# SECTION 3: Custom Triton INT4 GEMM (Fallback)
# ============================================================================

@triton.jit
def _int4_matmul_kernel(
    x_ptr,          # [M, K] FP16 input
    w_packed_ptr,   # [N, K//8] INT32 packed INT4 weights  
    scales_ptr,     # [N, num_groups] FP16 per-group scales
    out_ptr,        # [M, N] FP16 output
    M, N, K,
    stride_xm, stride_xk,
    stride_wn, stride_wk,
    stride_sn, stride_sk,
    stride_om, stride_on,
    GROUP_SIZE: tl.constexpr,
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
):
    """
    INT4 Weight-Only Quantized GEMM kernel.
    Computes: output[m, n] = sum_k(x[m, k] * dequant(w_packed[n, k]))
    
    Optimized for decode (small M = 1..32, large K and N).
    Achieves ~2x bandwidth reduction vs FP8 by reading INT4 weights.
    """
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)
    
    m_start = pid_m * BLOCK_M
    n_start = pid_n * BLOCK_N
    m_range = m_start + tl.arange(0, BLOCK_M)
    n_range = n_start + tl.arange(0, BLOCK_N)
    m_mask = m_range < M
    n_mask = n_range < N
    
    # Accumulator in FP32 for precision
    acc = tl.zeros([BLOCK_M, BLOCK_N], dtype=tl.float32)
    
    # Process K in packs of 8 (matching INT4 packing)
    num_k_packs = K // 8
    
    for ki in range(num_k_packs):
        k_base = ki * 8
        
        # Load packed INT4 weights: [BLOCK_N] INT32 values
        # Each INT32 contains 8 consecutive INT4 values along K
        packed = tl.load(
            w_packed_ptr + n_range * stride_wn + ki * stride_wk,
            mask=n_mask, other=0
        )
        
        # Load per-group scale: [BLOCK_N] FP16 values
        group_idx = k_base // GROUP_SIZE
        scale = tl.load(
            scales_ptr + n_range * stride_sn + group_idx * stride_sk,
            mask=n_mask, other=1.0
        ).to(tl.float32)
        
        # Unpack 8 INT4 values and accumulate dot product
        for i in range(8):
            k = k_base + i
            
            # Extract INT4: shift right by (i*4) bits, mask lower 4 bits, subtract 8
            w_uint4 = (packed >> (i * 4)) & 0xF
            w_int4 = w_uint4.to(tl.float32) - 8.0
            w_dequant = w_int4 * scale  # [BLOCK_N]
            
            # Load input: [BLOCK_M]
            x_val = tl.load(
                x_ptr + m_range * stride_xm + k * stride_xk,
                mask=m_mask, other=0.0
            ).to(tl.float32)
            
            # Outer product: [BLOCK_M, BLOCK_N]
            acc += x_val[:, None] * w_dequant[None, :]
    
    # Store result as FP16
    result = acc.to(tl.float16)
    tl.store(
        out_ptr + m_range[:, None] * stride_om + n_range[None, :] * stride_on,
        result,
        mask=m_mask[:, None] & n_mask[None, :]
    )


def triton_int4_matmul(x, w_packed, scales, bias, K):
    """
    Custom Triton INT4 matmul wrapper.
    
    Args:
        x: [M, K_orig] FP16 input (may need padding to K)
        w_packed: [N, K//8] INT32 packed weights
        scales: [N, num_groups] FP16 scales
        bias: [N] FP16 bias or None
        K: padded K dimension
    
    Returns:
        output: [M, N] FP16
    """
    M = x.shape[0]
    K_orig = x.shape[1]
    N = w_packed.shape[0]
    GROUP_SIZE = K // scales.shape[1]
    
    x_fp16 = x.to(torch.float16) if x.dtype != torch.float16 else x
    
    # Pad input if needed
    if K_orig < K:
        x_fp16 = F.pad(x_fp16, (0, K - K_orig))
    
    output = torch.empty(M, N, dtype=torch.float16, device=x.device)
    
    # Kernel launch configuration
    BLOCK_M = min(triton.next_power_of_2(M), 16)
    BLOCK_N = 64  # Good for H200 memory bandwidth
    
    grid = (triton.cdiv(M, BLOCK_M), triton.cdiv(N, BLOCK_N))
    
    _int4_matmul_kernel[grid](
        x_fp16, w_packed, scales, output,
        M, N, K,
        x_fp16.stride(0), x_fp16.stride(1),
        w_packed.stride(0), w_packed.stride(1),
        scales.stride(0), scales.stride(1),
        output.stride(0), output.stride(1),
        GROUP_SIZE=GROUP_SIZE,
        BLOCK_M=BLOCK_M,
        BLOCK_N=BLOCK_N,
    )
    
    if bias is not None:
        output = output + bias
    
    return output


# ============================================================================
# SECTION 4: Unified INT4 Linear Forward
# ============================================================================

_use_marlin = None

def int4_linear_forward(x, layer, bias):
    """
    Unified INT4 linear forward: tries Marlin first, falls back to Triton.
    
    Args:
        x: [M, K] input tensor
        layer: nn.Module with _int4_weights, _int4_scales, _int4_K attributes
        bias: bias tensor or None
    """
    global _use_marlin
    
    if _use_marlin is None:
        _use_marlin = check_marlin_available() and hasattr(layer, '_int4_marlin_weights')
        if _use_marlin:
            print("[Antigravity v21.0] Using Marlin INT4 GEMM (Tensor Core optimized)", file=sys.stderr)
        else:
            print("[Antigravity v21.0] Using Triton INT4 GEMM (custom kernel)", file=sys.stderr)
    
    if _use_marlin and hasattr(layer, '_int4_marlin_weights'):
        try:
            return marlin_gemm_forward(
                x, layer._int4_marlin_weights, layer._int4_marlin_scales,
                bias, layer._int4_K, layer._int4_N
            )
        except Exception as e:
            print(f"[Antigravity v21.0] Marlin GEMM failed: {e}, falling back to Triton", file=sys.stderr)
            _use_marlin = False
    
    # Triton fallback
    return triton_int4_matmul(
        x, layer._int4_weights, layer._int4_scales,
        bias, layer._int4_K
    )


def quantize_layer_to_int4(layer, group_size=128):
    """
    Quantize a Linear layer's weights to INT4 in-place.
    
    Called during process_weights_after_loading, before any forward pass.
    Sets layer._int4_weights, _int4_scales, _int4_K, _int4_N.
    Optionally sets _int4_marlin_weights if Marlin is available.
    """
    weight = layer.weight
    
    # Get FP16 weights (handle FP8 with scale)
    if weight.dtype == torch.float8_e4m3fn:
        w_fp16 = weight.data.to(torch.float16)
        # Apply weight scale if available
        if hasattr(layer, 'weight_scale') and layer.weight_scale is not None:
            w_fp16 = w_fp16 * layer.weight_scale.to(torch.float16)
    elif weight.dtype in (torch.bfloat16, torch.float32):
        w_fp16 = weight.data.to(torch.float16)
    else:
        w_fp16 = weight.data.to(torch.float16)
    
    N, K_orig = w_fp16.shape
    
    # Quantize and pack
    w_packed, scales, K_padded = quantize_and_pack(w_fp16, group_size)
    
    # Store on layer
    layer._int4_weights = w_packed.contiguous()
    layer._int4_scales = scales.contiguous()
    layer._int4_K = K_padded
    layer._int4_N = N
    layer._int4_K_orig = K_orig
    
    # Try Marlin repacking
    if check_marlin_available():
        try:
            w_marlin = repack_for_marlin(w_packed, K_padded, N)
            # Marlin expects scales in [num_groups, N] layout
            layer._int4_marlin_weights = w_marlin
            layer._int4_marlin_scales = scales.t().contiguous()  # [num_groups, N]
        except Exception as e:
            print(f"[Antigravity v21.0] Marlin repack failed for layer: {e}", file=sys.stderr)
    
    # Keep original weight tensor data intact to ensure C++ kernel shape validation succeeds in vLLM V1.
    original_size_mb = weight.data.numel() * weight.data.element_size() / (1024 * 1024)
    layer.weight.is_mocked_empty = False
    
    int4_size_mb = w_packed.numel() * 4 / (1024 * 1024)  # INT32
    saved_mb = original_size_mb - int4_size_mb - scales.numel() * 2 / (1024 * 1024)
    
    return saved_mb
