#!/usr/bin/env python3
"""
Phase 3: Decode-Priority Scheduler Patch for vLLM v0.26.0+

PURPOSE:
    Patch vLLM's scheduler to aggressively prioritize decode requests.
    When decode (token generation) requests are active, the prefill token budget 
    per step is capped to a configurable limit via DECODE_PREFILL_CAP env var.

MECHANISM:
    - Automatically locates scheduler.py anywhere in vLLM package
    - Wraps Scheduler.schedule() method at module load time
    - When running requests exist (decode), temporarily reduces max_num_batched_tokens
    - This makes each scheduler step faster → lower TPOT
"""

import os
import sys
import site
import shutil
import re

def find_vllm():
    """Find vLLM installation path."""
    for sp in site.getsitepackages():
        p = os.path.join(sp, 'vllm')
        if os.path.isdir(p):
            return p
    # Fallback search common paths
    for pyver in ['3.12', '3.11', '3.10']:
        p = f'/usr/local/lib/python{pyver}/dist-packages/vllm'
        if os.path.isdir(p):
            return p
    raise FileNotFoundError("vLLM not found in any site-packages")


def find_scheduler_file(vllm_path):
    """Dynamically search for scheduler.py containing 'class Scheduler'."""
    candidates = []
    for root, dirs, files in os.walk(vllm_path):
        for f in files:
            if f == 'scheduler.py':
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        if 'class Scheduler' in content:
                            candidates.append(full_path)
                except Exception as e:
                    print(f"Warning reading {full_path}: {e}")
    
    if not candidates:
        return None
    
    # Prefer v1 scheduler if multiple found
    for c in candidates:
        if 'v1' in c:
            return c
    return candidates[0]


def patch_scheduler(vllm_path):
    """
    Inject decode-priority scheduling into vLLM scheduler.
    Appends a monkey-patch at the end of scheduler.py that wraps Scheduler.schedule().
    """
    sched_path = find_scheduler_file(vllm_path)
    
    if not sched_path or not os.path.exists(sched_path):
        print(f"❌ Scheduler file containing 'class Scheduler' not found in {vllm_path}")
        sys.exit(1)
    
    print(f"🎯 Target scheduler file found: {sched_path}")
    
    # Backup original
    shutil.copy2(sched_path, sched_path + '.orig')
    
    with open(sched_path, 'r', encoding='utf-8') as f:
        src = f.read()
    
    # Check if already patched
    if '_DECODE_PREFILL_CAP' in src:
        print("✅ Scheduler already patched (skipping)")
        return
    
    patch_code = '''

# ============================================================
# PHASE 3: DECODE-PRIORITY SCHEDULER PATCH
# Controlled by env var DECODE_PREFILL_CAP (default: 0 = disabled)
# ============================================================
import os as _dp_os
import functools as _dp_functools

_DECODE_PREFILL_CAP = int(_dp_os.environ.get("DECODE_PREFILL_CAP", "0"))

if _DECODE_PREFILL_CAP > 0:
    _dp_original_schedule = Scheduler.schedule

    @_dp_functools.wraps(_dp_original_schedule)
    def _dp_wrapped_schedule(self, *args, **kwargs):
        """Decode-priority wrapper: cap prefill tokens when decode is active."""
        _num_running = 0
        for _attr_name in ('running', 'running_reqs_data', 'running_queue', 'running_reqs'):
            _attr_val = getattr(self, _attr_name, None)
            if _attr_val is not None and hasattr(_attr_val, '__len__'):
                _num_running = len(_attr_val)
                break
        
        if _num_running > 0 and hasattr(self, 'max_num_batched_tokens'):
            _orig_budget = self.max_num_batched_tokens
            _new_budget = min(_orig_budget, _num_running + _DECODE_PREFILL_CAP)
            self.max_num_batched_tokens = _new_budget
            try:
                return _dp_original_schedule(self, *args, **kwargs)
            finally:
                self.max_num_batched_tokens = _orig_budget
        
        return _dp_original_schedule(self, *args, **kwargs)

    Scheduler.schedule = _dp_wrapped_schedule
    print(f"[PHASE3] ✅ Decode-priority scheduler ACTIVE: prefill_cap={_DECODE_PREFILL_CAP}")
else:
    print("[PHASE3] ℹ️  Decode-priority scheduler DISABLED (DECODE_PREFILL_CAP=0)")
# ============================================================
# END PHASE 3 PATCH
# ============================================================
'''
    
    src += patch_code
    
    with open(sched_path, 'w', encoding='utf-8') as f:
        f.write(src)
    
    print(f"✅ Scheduler patched successfully at {sched_path}")


def main():
    print("=" * 60)
    print("PHASE 3: Decode-Priority Scheduler Patch")
    print("=" * 60)
    
    vllm_path = find_vllm()
    print(f"📁 vLLM found at: {vllm_path}")
    
    patch_scheduler(vllm_path)
    
    print("")
    print("🎉 Phase 3 patching complete!")


if __name__ == '__main__':
    main()
