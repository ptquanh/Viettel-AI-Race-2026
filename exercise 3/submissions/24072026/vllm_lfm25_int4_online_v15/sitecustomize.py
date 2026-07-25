import os
import sys
import asyncio

print("[Antigravity Phase 3 v15] Modern vLLM Engine + Fused ShortConv + Online INT4 (torchao) Initialized", file=sys.stderr)

# --- 1. TORCHAO ONLINE INT4 QUANTIZATION HOOK ---
try:
    if os.getenv("VLLM_ENABLE_TORCHAO_INT4", "1") == "1":
        import vllm.model_executor.model_loader as model_loader
        _orig_get_model = model_loader.get_model
        
        def _patched_get_model(*args, **kwargs):
            model = _orig_get_model(*args, **kwargs)
            print("[Antigravity Phase 3 v15] Model loaded! Applying torchao int4_weight_only quantization...", file=sys.stderr)
            try:
                import torchao
                from torchao.quantization import int4_weight_only
                group_size = int(os.getenv("TORCHAO_GROUP_SIZE", "128"))
                torchao.quantize_(model, int4_weight_only(group_size=group_size))
                print(f"[Antigravity Phase 3 v15] torchao INT4 quantization COMPLETE (group_size={group_size})!", file=sys.stderr)
            except Exception as q_err:
                print(f"[Antigravity Phase 3 v15] torchao INT4 quantization Warning: {q_err}", file=sys.stderr)
            return model
            
        model_loader.get_model = _patched_get_model
        print("[Antigravity Phase 3 v15] Successfully installed torchao INT4 model loader patch!", file=sys.stderr)
except Exception as t_err:
    print(f"[Antigravity Phase 3 v15] torchao Hook Error: {t_err}", file=sys.stderr)

# --- 2. FUSED SHORT CONV TRITON KERNEL PATCH ---
try:
    from vllm.model_executor.layers.mamba.short_conv import ShortConv
    from patch.fused_short_conv import fused_lfm_short_conv_update

    _orig_forward_cuda = ShortConv.forward_cuda

    def _patched_forward_cuda(self, hidden_states, output):
        try:
            from vllm.forward_context import get_forward_context
            from vllm.model_executor.layers.mamba.mamba_utils import is_conv_state_dim_first
            import torch
            
            forward_context = get_forward_context()
            attn_metadata_raw = forward_context.attn_metadata
            
            if attn_metadata_raw is None:
                return _orig_forward_cuda(self, hidden_states, output)
                
            attn_metadata = attn_metadata_raw[self.prefix]
            
            num_prefills = attn_metadata.num_prefills
            num_decodes = attn_metadata.num_decode_tokens
            
            if num_prefills > 0 or num_decodes == 0:
                return _orig_forward_cuda(self, hidden_states, output)

            conv_state = (
                self.kv_cache[0]
                if is_conv_state_dim_first()
                else self.kv_cache[0].transpose(-1, -2)
            )
            
            BCx, _ = self.in_proj(hidden_states)
            
            conv_weights = self.conv.weight.view(
                self.conv.weight.size(0), self.conv.weight.size(2)
            )
            
            state_indices = attn_metadata.state_indices_tensor_d
            
            y = fused_lfm_short_conv_update(
                BCx[:num_decodes],
                conv_state,
                conv_weights,
                self.conv.bias,
                state_indices
            )
            
            output[:num_decodes], _ = self.out_proj(y)
        except Exception as patch_e:
            print(f"[Antigravity v15] Fused Kernel Failed: {patch_e}, fallback to orig!", file=sys.stderr)
            return _orig_forward_cuda(self, hidden_states, output)

    ShortConv.forward_cuda = _patched_forward_cuda
    print("[Antigravity Phase 3 v15] Successfully patched ShortConv.forward_cuda with FUSED TRITON KERNEL!", file=sys.stderr)
except Exception as e:
    print(f"[Antigravity Phase 3 v15] Error patching ShortConv: {e}", file=sys.stderr)

# --- 3. ASYNC LLM ENGINE NATIVE WARMUP ---
try:
    from vllm.engine.async_llm_engine import AsyncLLMEngine
    from vllm.inputs import TextPrompt
    from vllm.sampling_params import SamplingParams
    
    _orig_from_engine_args = AsyncLLMEngine.from_engine_args

    @classmethod
    def _patched_from_engine_args(cls, engine_args, **kwargs):
        engine = _orig_from_engine_args(engine_args, **kwargs)
        print("[Antigravity Phase 3 v15] Modern Engine initialized! Executing Native Zero-Penalty JIT Warmup...", file=sys.stderr)
        
        async def _run_native_warmup():
            try:
                prompt = TextPrompt(prompt="Xin chào, hãy kích hoạt CUDA Graphs và FlashInfer memory pool ngay lập tức.")
                params = SamplingParams(max_tokens=16, temperature=0.0)
                warmup_rounds = int(os.getenv("VLLM_CUDAGRAPH_NUM_OF_WARMUPS", "3"))
                for i in range(warmup_rounds):
                    results_generator = engine.generate(prompt, params, request_id=f"native_warmup_v15_{i}")
                    async for _ in results_generator:
                        pass
                print(f"[Antigravity Phase 3 v15] Native Zero-Penalty Warmup COMPLETE ({warmup_rounds} rounds)!", file=sys.stderr)
            except Exception as w_err:
                print(f"[Antigravity Phase 3 v15] Native Warmup Warning (non-fatal): {w_err}", file=sys.stderr)
                
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(_run_native_warmup())
            else:
                loop.run_until_complete(_run_native_warmup())
        except Exception as l_err:
            print(f"[Antigravity Phase 3 v15] Asyncio Loop execution note: {l_err}", file=sys.stderr)
            
        return engine

    AsyncLLMEngine.from_engine_args = _patched_from_engine_args
    print("[Antigravity Phase 3 v15] Successfully installed AsyncLLMEngine native warmup patch!", file=sys.stderr)

except Exception as hook_err:
    print(f"[Antigravity Phase 3 v15] Native Warmup Hook Error: {hook_err}", file=sys.stderr)
