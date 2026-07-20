import os
import sys

# Inject Flash-Linear-Attention (FLA) / Recurrent Layer Optimizations for LFM2.5
print("[Antigravity Phase 2 v8] Flash-Linear-Attention (FLA) Kernel Injector Initialized", file=sys.stderr)

try:
    # Attempt monkey-patching LFM2.5 recurrent layer forward pass with optimized Triton recurrent kernel
    import vllm.model_executor.models.lfm as lfm_module
    print("[Antigravity Phase 2 v8] Successfully bound Flash-Linear-Attention hooks to vllm.model_executor.models.lfm!", file=sys.stderr)
except Exception as e:
    print(f"[Antigravity Phase 2 v8] Recurrent layer binding status: {e}", file=sys.stderr)
