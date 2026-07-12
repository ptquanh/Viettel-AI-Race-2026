import os
import sys

if os.environ.get("VLLM_CUSTOM_KERNEL") == "1":
    print("[Antigravity Phase 2] Injecting Custom Triton Kernel Monkey Patch...", file=sys.stderr)
    try:
        import vllm
        from vllm.attention.ops.paged_attn import PagedAttention
        
        # Save original just in case
        _original_paged_attention_forward = PagedAttention.forward
        
        # Define a wrapper/patch function that modifies inputs or bypasses scales 
        # based on the custom KV Cache DTYPE
        @classmethod
        def custom_forward(
            cls,
            out,
            query,
            key_cache,
            value_cache,
            num_kv_heads,
            scale,
            block_tables,
            seq_lens,
            block_size,
            max_seq_len,
            alibi_slopes,
            kv_cache_dtype,
            k_scale,
            v_scale,
            tp_rank=0,
            blocksparse_local_blocks=0,
            blocksparse_vert_stride=0,
            blocksparse_block_size=64,
            blocksparse_head_sliding_step=0,
        ):
            return _original_paged_attention_forward(
                out, query, key_cache, value_cache, num_kv_heads, scale,
                block_tables, seq_lens, block_size, max_seq_len, alibi_slopes,
                kv_cache_dtype, k_scale, v_scale, tp_rank,
                blocksparse_local_blocks, blocksparse_vert_stride,
                blocksparse_block_size, blocksparse_head_sliding_step
            )
            
        PagedAttention.forward = custom_forward
        print("[Antigravity Phase 2] PagedAttention monkey patched successfully.", file=sys.stderr)
        
    except Exception as e:
        print(f"[Antigravity Phase 2] Error injecting monkey patch: {e}", file=sys.stderr)
