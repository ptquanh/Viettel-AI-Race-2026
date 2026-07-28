import sys
import importlib
import importlib.abc
import importlib.util

# -----------------------------------------------------------------------------
# [Antigravity v22.0] Bulletproof Post-Import Hooking for vLLM
# Prevents premature CUDA initialization crashes by waiting for natural imports.
# -----------------------------------------------------------------------------

def apply_linear_patches(module):
    try:
        import torch
        import torch.nn.functional as F
        
        def make_int4_forward(orig_fwd, layer_class_name):
            def _patched_fwd(self, *args, **kwargs):
                if getattr(self, "_is_int4", False):
                    from patch.int4_gemm import int4_linear_forward
                    _real_linear = F.linear
                    def _mock_linear(inp, weight, bias=None):
                        if getattr(weight, "is_mocked_empty", False) or weight is getattr(self, "weight", None):
                            return int4_linear_forward(inp, self, bias)
                        return _real_linear(inp, weight, bias)
                    
                    F.linear = _mock_linear
                    
                    # Also patch batch invariant linear if enabled
                    import vllm.model_executor.layers.batch_invariant as bi
                    _real_bi = getattr(bi, "linear_batch_invariant", None)
                    if _real_bi is not None:
                        def _mock_bi(inp, weight, bias=None):
                            if getattr(weight, "is_mocked_empty", False) or weight is getattr(self, "weight", None):
                                return int4_linear_forward(inp, self, bias)
                            return _real_bi(inp, weight, bias)
                        bi.linear_batch_invariant = _mock_bi
                        
                    try:
                        return orig_fwd(self, *args, **kwargs)
                    finally:
                        F.linear = _real_linear
                        if _real_bi is not None:
                            bi.linear_batch_invariant = _real_bi
                else:
                    if not torch.cuda.is_current_stream_capturing():
                        try:
                            from patch.int4_gemm import quantize_layer_to_int4
                            saved_mb = quantize_layer_to_int4(self, group_size=128)
                            self._is_int4 = True
                        except Exception as e:
                            print(f"[Antigravity] Lazy Quantization failed for {layer_class_name}: {e}", file=sys.stderr)
                            self._is_int4 = False
                    else:
                        self._is_int4 = False
                    return orig_fwd(self, *args, **kwargs)
            return _patched_fwd

        patched_count = 0
        for cls_name in ["ColumnParallelLinear", "RowParallelLinear", "MergedColumnParallelLinear", "QKVParallelLinear"]:
            if hasattr(module, cls_name):
                cls = getattr(module, cls_name)
                if hasattr(cls, "forward"):
                    orig_fwd = getattr(cls, "forward")
                    setattr(cls, "forward", make_int4_forward(orig_fwd, cls_name))
                    patched_count += 1
        print(f"[Antigravity v22.0] Successfully patched {patched_count} linear classes via meta_path", file=sys.stderr)
    except Exception as e:
        print(f"[Antigravity v22.0] Failed to patch linear classes: {e}", file=sys.stderr)

def apply_runner_patches(module):
    try:
        def _safe_quantize(self_obj):
            try:
                model_obj = getattr(self_obj, "model", None)
                if model_obj is None and hasattr(self_obj, "model_executor"):
                    model_obj = getattr(self_obj.model_executor, "model", None)
                if model_obj is not None:
                    if getattr(model_obj, "_is_quantized", False): return
                    print("[Antigravity v22.0] Eagerly Quantizing weights to INT4...", file=sys.stderr)
                    from patch.int4_gemm import quantize_layer_to_int4
                    
                    quant_count = 0
                    total_saved_mb = 0
                    for name, mod in model_obj.named_modules():
                        cls_name = mod.__class__.__name__
                        if cls_name in ["ColumnParallelLinear", "RowParallelLinear", "MergedColumnParallelLinear", "QKVParallelLinear"]:
                            if hasattr(mod, "weight") and mod.weight is not None and mod.weight.dim() == 2 and mod.weight.size(0) >= 128:
                                try:
                                    saved_mb = quantize_layer_to_int4(mod, group_size=128)
                                    total_saved_mb += saved_mb
                                    mod._is_int4 = True
                                    quant_count += 1
                                except Exception as e:
                                    print(f"[Antigravity] Failed to quantize {name}: {e}", file=sys.stderr)
                                    mod._is_int4 = False
                    
                    print(f"[Antigravity v22.0] Eagerly Quantized {quant_count} layers. Saved ~{total_saved_mb:.2f} MB VRAM.", file=sys.stderr)
                    model_obj._is_quantized = True
                else:
                    print("[Antigravity v22.0] Warning: Could not find model object in runner.", file=sys.stderr)
            except Exception as e:
                print(f"[Antigravity v22.0] Eager Quantization Exception: {e}", file=sys.stderr)

        TargetClass = getattr(module, "GPUModelRunner", getattr(module, "ModelRunner", None))
        if TargetClass is not None:
            if hasattr(TargetClass, "profile_run"):
                _orig_profile_run = TargetClass.profile_run
                def _patched_profile_run(self, *args, **kwargs):
                    _safe_quantize(self)
                    return _orig_profile_run(self, *args, **kwargs)
                TargetClass.profile_run = _patched_profile_run
                print(f"[Antigravity v22.0] Hooked {TargetClass.__name__}.profile_run", file=sys.stderr)
            
            if hasattr(TargetClass, "capture_model"):
                _orig_capture_model = TargetClass.capture_model
                def _patched_capture_model(self, *args, **kwargs):
                    _safe_quantize(self)
                    return _orig_capture_model(self, *args, **kwargs)
                TargetClass.capture_model = _patched_capture_model
                print(f"[Antigravity v22.0] Hooked {TargetClass.__name__}.capture_model", file=sys.stderr)
    except Exception as e:
        print(f"[Antigravity v22.0] Failed to patch runner classes: {e}", file=sys.stderr)

class VllmHookLoader(importlib.abc.Loader):
    def __init__(self, real_loader):
        self.real_loader = real_loader

    def create_module(self, spec):
        if hasattr(self.real_loader, 'create_module'):
            return self.real_loader.create_module(spec)
        return None

    def exec_module(self, module):
        self.real_loader.exec_module(module)
        if module.__name__ == 'vllm.model_executor.layers.linear':
            apply_linear_patches(module)
        elif module.__name__ in ('vllm.v1.worker.gpu_model_runner', 'vllm.worker.model_runner'):
            apply_runner_patches(module)

class VllmHookFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname in ('vllm.model_executor.layers.linear', 'vllm.v1.worker.gpu_model_runner', 'vllm.worker.model_runner'):
            sys.meta_path.remove(self)
            try:
                spec = importlib.util.find_spec(fullname)
            finally:
                sys.meta_path.insert(0, self)
                
            if spec and spec.loader:
                spec.loader = VllmHookLoader(spec.loader)
            return spec
        return None

if not any(isinstance(f, VllmHookFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, VllmHookFinder())
