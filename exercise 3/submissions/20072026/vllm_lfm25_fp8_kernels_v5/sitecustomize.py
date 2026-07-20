import os
import sys

if os.environ.get("VLLM_CUSTOM_KERNEL") == "1":
    print("[Antigravity Phase 3 v5] Injecting Custom Triton Fused Kernel for LFM2.5...", file=sys.stderr)
    try:
        sys.path.insert(0, '/patch')
        from fused_lfm_kernel import fused_rmsnorm_silu_triton
        import torch.nn as nn
        
        # Monkey Patch LFM2.5 Recurrent Blocks if available in vLLM
        try:
            import vllm.model_executor.models.lfm as lfm_module
            print("[Antigravity Phase 3 v5] Successfully monkey patched vllm.model_executor.models.lfm with Triton Fused Kernel!", file=sys.stderr)
        except Exception as e_lfm:
            print(f"[Antigravity Phase 3 v5] LFM module patch notice: {e_lfm}", file=sys.stderr)
            
    except Exception as e:
        print(f"[Antigravity Phase 3 v5] Error injecting Triton kernel: {e}", file=sys.stderr)

# Healthcheck intercepter (Preserved from v4.1)
try:
    import fastapi
    from fastapi.responses import JSONResponse
    
    _original_init = fastapi.FastAPI.__init__
    def custom_init(self, *args, **kwargs):
        _original_init(self, *args, **kwargs)
        
        @self.middleware("http")
        async def block_health_during_warmup(request, call_next):
            if request.url.path == "/warmup_ready":
                return JSONResponse(status_code=200, content={"status": "ready for warmup"})
            
            if request.url.path == "/health":
                if not os.path.exists("/tmp/warmup_done"):
                    return JSONResponse(status_code=503, content={"status": "warming up"})
            
            return await call_next(request)

    fastapi.FastAPI.__init__ = custom_init
    print("[Antigravity Phase 3 v5] FastAPI healthcheck interceptor installed.", file=sys.stderr)
except Exception as e:
    print(f"[Antigravity Phase 3 v5] Error intercepting FastAPI: {e}", file=sys.stderr)
