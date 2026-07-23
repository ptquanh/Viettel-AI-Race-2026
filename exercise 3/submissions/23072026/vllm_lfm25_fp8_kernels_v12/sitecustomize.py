import os
import sys
import asyncio

print("[Antigravity Phase 2 v11] Modern vLLM Engine + Native Zero-Penalty Startup Warmup Initialized", file=sys.stderr)

try:
    import vllm.model_executor.models.lfm as lfm_module
    print("[Antigravity Phase 2 v11] Bound hooks to vllm.model_executor.models.lfm!", file=sys.stderr)
except Exception as e:
    print(f"[Antigravity Phase 2 v11] LFM hook binding status: {e}", file=sys.stderr)

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
