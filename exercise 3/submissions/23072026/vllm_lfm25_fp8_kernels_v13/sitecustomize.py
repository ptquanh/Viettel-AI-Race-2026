import os
import sys
import torch
from torch.profiler import profile, record_function, ProfilerActivity

if os.environ.get("VLLM_ENABLE_CUSTOM_PROFILER") == "1":
    print("[Antigravity Phase 3 v13] Injecting PyTorch Profiler into LFM...", file=sys.stderr)
    try:
        sys.path.insert(0, '/patch')
        import vllm.model_executor.models.lfm as lfm_module
        
        original_forward = lfm_module.LFMForCausalLM.forward
        
        # Biến toàn cục để theo dõi số bước
        profile_step = 0
        prof = None
        
        def profiled_forward(self, *args, **kwargs):
            global profile_step, prof
            
            # Chỉ profile bước decode thứ 10 đến 15 để tránh warmup
            if profile_step == 10:
                print("[Antigravity v13] BẮT ĐẦU PROFILING DECODE STEP...", file=sys.stderr)
                prof = profile(
                    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
                    record_shapes=True,
                    with_stack=True
                )
                prof.start()
                
            if 10 <= profile_step < 15 and prof is not None:
                with record_function(f"decode_step_{profile_step}"):
                    res = original_forward(self, *args, **kwargs)
            else:
                res = original_forward(self, *args, **kwargs)
                
            if profile_step == 15 and prof is not None:
                prof.stop()
                print("[Antigravity v13] KẾT THÚC PROFILING. ĐANG IN KẾT QUẢ:", file=sys.stderr)
                print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=30), file=sys.stderr)
                
            profile_step += 1
            return res
            
        lfm_module.LFMForCausalLM.forward = profiled_forward
        print("[Antigravity Phase 3 v13] Profiler hook successfully injected into LFM forward!", file=sys.stderr)
    except Exception as e:
        print(f"[Antigravity Phase 3 v13] Error injecting Profiler: {e}", file=sys.stderr)
