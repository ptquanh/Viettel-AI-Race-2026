import os
import sys
import asyncio

print("[Antigravity Phase 2 v11] Modern vLLM Engine + Native Zero-Penalty Startup Warmup Initialized", file=sys.stderr)

try:
    import vllm.model_executor.models.lfm as lfm_module
    print("[Antigravity Phase 3 v14] Bound hooks to vllm.model_executor.models.lfm!", file=sys.stderr)
except Exception as e:
    print(f"[Antigravity Phase 3 v14] LFM hook binding status: {e}", file=sys.stderr)

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
            
            # Chỉ kích hoạt Fused Kernel khi hoàn toàn là Decode
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
            
            # GỌI FUSED KERNEL TRITON SIÊU TỐC
            y = fused_lfm_short_conv_update(
                BCx[:num_decodes],
                conv_state,
                conv_weights,
                self.conv.bias,
                state_indices
            )
            
            output[:num_decodes], _ = self.out_proj(y)
        except Exception as patch_e:
            # Fallback nếu kernel của chúng ta bị lỗi runtime
            import sys
            print(f"[Antigravity v14] Fused Kernel Failed: {patch_e}, fallback to orig!", file=sys.stderr)
            return _orig_forward_cuda(self, hidden_states, output)

    ShortConv.forward_cuda = _patched_forward_cuda
    print("[Antigravity Phase 3 v14] Successfully patched ShortConv.forward_cuda with FUSED TRITON KERNEL!", file=sys.stderr)
except Exception as e:
    print(f"[Antigravity Phase 3 v14] Error patching ShortConv: {e}", file=sys.stderr)

try:
    from vllm.engine.async_llm_engine import AsyncLLMEngine
    from vllm.inputs import TextPrompt
    from vllm.sampling_params import SamplingParams
    
    _orig_from_engine_args = AsyncLLMEngine.from_engine_args

    @classmethod
    def _patched_from_engine_args(cls, engine_args, **kwargs):
        engine = _orig_from_engine_args(engine_args, **kwargs)
        print("[Antigravity Phase 2 v11] Modern Engine initialized! Executing Native Zero-Penalty JIT Warmup...", file=sys.stderr)
        
        async def _run_native_warmup():
            try:
                prompt = TextPrompt(prompt="Xin chào, hãy kích hoạt CUDA Graphs và FlashInfer memory pool ngay lập tức.")
                params = SamplingParams(max_tokens=16, temperature=0.0)
                warmup_rounds = int(os.getenv("VLLM_CUDAGRAPH_NUM_OF_WARMUPS", "3"))
                for i in range(warmup_rounds):
                    results_generator = engine.generate(prompt, params, request_id=f"native_warmup_v11_{i}")
                    async for _ in results_generator:
                        pass
                print(f"[Antigravity Phase 2 v11] Native Zero-Penalty Warmup COMPLETE ({warmup_rounds} rounds)!", file=sys.stderr)
            except Exception as w_err:
                print(f"[Antigravity Phase 2 v11] Native Warmup Warning (non-fatal): {w_err}", file=sys.stderr)
                
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(_run_native_warmup())
            else:
                loop.run_until_complete(_run_native_warmup())
        except Exception as l_err:
            print(f"[Antigravity Phase 2 v11] Asyncio Loop execution note: {l_err}", file=sys.stderr)
            
        return engine

    AsyncLLMEngine.from_engine_args = _patched_from_engine_args
    print("[Antigravity Phase 2 v11] Successfully installed AsyncLLMEngine native warmup patch!", file=sys.stderr)

except Exception as hook_err:
    print(f"[Antigravity Phase 2 v11] Native Warmup Hook Error: {hook_err}", file=sys.stderr)
