import os
import sys
import asyncio
import torch

print("[Antigravity Phase 7 v21.0] INT4 Online Quantization + Marlin/Triton GEMM Initialized", file=sys.stderr)

# ============================================================================
# 1. INT4 ONLINE QUANTIZATION HOOK (EAGER QUANTIZATION BEFORE PROFILE/CAPTURE)
# ============================================================================
try:
    from vllm.model_executor.layers.linear import (
        ColumnParallelLinear, 
        RowParallelLinear, 
        MergedColumnParallelLinear,
        QKVParallelLinear
    )
    import torch.nn.functional as F
    import sys

    # A. Hook F.linear for intercepted forward passes
    def make_int4_forward(orig_fwd, layer_class_name):
        def _patched_fwd(self, *args, **kwargs):
            # Fallback Lazy Quantization if Eager failed
            if not hasattr(self, "_is_int4"):
                import torch
                if not torch.cuda.is_current_stream_capturing():
                    from patch.int4_gemm import quantize_layer_to_int4
                    print(f"[Antigravity v21.0] Fallback Lazy Quantizing {layer_class_name}...", file=sys.stderr)
                    try:
                        quantize_layer_to_int4(self, group_size=128)
                        self._is_int4 = True
                    except Exception as e:
                        print(f"[Antigravity v21.0] Fallback Quantization failed: {e}", file=sys.stderr)
                        self._is_int4 = False
                else:
                    self._is_int4 = False

            if getattr(self, "_is_int4", False):
                from patch.int4_gemm import int4_linear_forward
                
                _real_linear = F.linear
                def _mock_linear(inp, weight, bias=None):
                    if weight is self.weight:
                        return int4_linear_forward(inp, self, bias)
                    return _real_linear(inp, weight, bias)
                
                F.linear = _mock_linear
                try:
                    return orig_fwd(self, *args, **kwargs)
                finally:
                    F.linear = _real_linear
            else:
                return orig_fwd(self, *args, **kwargs)
        return _patched_fwd

    for cls in [ColumnParallelLinear, RowParallelLinear, MergedColumnParallelLinear, QKVParallelLinear]:
        try:
            if hasattr(cls, "forward"):
                orig_fwd = getattr(cls, "forward")
                setattr(cls, "forward", make_int4_forward(orig_fwd, cls.__name__))
        except Exception as e:
            print(f"[Antigravity v21.0] Error patching {cls.__name__}: {e}", file=sys.stderr)

    # B. Eager Quantization Hook (Before CUDA Graph Capture / Profile Run)
    def quantize_all_layers(model):
        if getattr(model, "_is_quantized", False): return
        print("[Antigravity v21.0] Eagerly Quantizing weights to INT4...", file=sys.stderr)
        from patch.int4_gemm import quantize_layer_to_int4
        
        quant_count = 0
        total_saved_mb = 0
        for name, module in model.named_modules():
            if isinstance(module, (ColumnParallelLinear, RowParallelLinear, MergedColumnParallelLinear, QKVParallelLinear)):
                if hasattr(module, "weight") and module.weight is not None and module.weight.dim() == 2 and module.weight.size(0) >= 128:
                    try:
                        saved_mb = quantize_layer_to_int4(module, group_size=128)
                        total_saved_mb += saved_mb
                        module._is_int4 = True
                        quant_count += 1
                    except Exception as e:
                        print(f"[Antigravity v21.0] Failed to quantize {name}: {e}", file=sys.stderr)
                        module._is_int4 = False
                        
        print(f"[Antigravity v21.0] Quantized {quant_count} layers. Saved ~{total_saved_mb:.2f} MB VRAM.", file=sys.stderr)
        model._is_quantized = True

    def _apply_eager_hooks(TargetClass):
        hooked = False
        if hasattr(TargetClass, "profile_run"):
            _orig_profile_run = TargetClass.profile_run
            def _patched_profile_run(self, *args, **kwargs):
                quantize_all_layers(self.model)
                return _orig_profile_run(self, *args, **kwargs)
            TargetClass.profile_run = _patched_profile_run
            print(f"[Antigravity v21.0] Hooked {TargetClass.__name__}.profile_run for Eager Quantization", file=sys.stderr)
            hooked = True
        
        if hasattr(TargetClass, "capture_model"):
            _orig_capture_model = TargetClass.capture_model
            def _patched_capture_model(self, *args, **kwargs):
                quantize_all_layers(self.model)
                return _orig_capture_model(self, *args, **kwargs)
            TargetClass.capture_model = _patched_capture_model
            print(f"[Antigravity v21.0] Hooked {TargetClass.__name__}.capture_model for Eager Quantization", file=sys.stderr)
            hooked = True
        return hooked

    # Try hooking ModelRunner, if it fails try Worker
    hooked_any = False
    try:
        from vllm.worker.model_runner import ModelRunner
        hooked_any = _apply_eager_hooks(ModelRunner) or hooked_any
    except Exception:
        pass

    try:
        from vllm.v1.worker.gpu_model_runner import GPUModelRunner
        hooked_any = _apply_eager_hooks(GPUModelRunner) or hooked_any
    except Exception:
        pass
        
    try:
        from vllm.worker.worker import Worker
        hooked_any = _apply_eager_hooks(Worker) or hooked_any
    except Exception:
        pass
            
    if not hooked_any:
        print("[Antigravity v21.0] Warning: Could not hook Eager Quantization. Falling back to Lazy Quantization.", file=sys.stderr)

except Exception as e:
    print(f"[Antigravity v21.0] INT4 Hook Init status: {e}", file=sys.stderr)


# ============================================================================
# 2. KHÔI PHỤC KERNEL TRITON SHORTCONV VƯƠNG MIỆN v18.0 (100% ACCURACY)
# ============================================================================
try:
    from vllm.model_executor.layers.mamba.short_conv import ShortConv
    from patch.fused_short_conv import fused_lfm_short_conv_update

    _orig_forward_cuda = ShortConv.forward_cuda

    def _patched_forward_cuda(self, hidden_states, output):
        try:
            from vllm.forward_context import get_forward_context
            from vllm.model_executor.layers.mamba.mamba_utils import is_conv_state_dim_first

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

            state_indices = attn_metadata.state_indices_tensor_d
            if state_indices is None or conv_state is None:
                return _orig_forward_cuda(self, hidden_states, output)

            BCx, _ = self.in_proj(hidden_states)

            if not hasattr(self, "_cached_conv_weight"):
                self._cached_conv_weight = self.conv.weight.view(
                    self.conv.weight.size(0), self.conv.weight.size(2)
                )

            y = fused_lfm_short_conv_update(
                BCx[:num_decodes],
                conv_state,
                self._cached_conv_weight,
                self.conv.bias,
                state_indices
            )

            output[:num_decodes], _ = self.out_proj(y)
        except Exception as patch_e:
            import sys
            print(f"[Antigravity v21.0] Triton Kernel Warning: {patch_e}, fallback to orig!", file=sys.stderr)
            return _orig_forward_cuda(self, hidden_states, output)

    ShortConv.forward_cuda = _patched_forward_cuda
    print("[Antigravity Phase 7 v21.0] Successfully patched ShortConv.forward_cuda with TRITON v18.0 KERNEL!", file=sys.stderr)
except Exception as e:
    print(f"[Antigravity Phase 7 v21.0] Error patching ShortConv: {e}", file=sys.stderr)


# ============================================================================
# 3. NATIVE ZERO-PENALTY WARMUP (10 ROUNDS)
# ============================================================================
try:
    from vllm.engine.async_llm_engine import AsyncLLMEngine
    from vllm.inputs import TextPrompt
    from vllm.sampling_params import SamplingParams

    _orig_from_engine_args = AsyncLLMEngine.from_engine_args

    @classmethod
    def _patched_from_engine_args(cls, engine_args, **kwargs):
        engine = _orig_from_engine_args(engine_args, **kwargs)
        print("[Antigravity Phase 7 v21.0] Modern Engine initialized! Executing Native Zero-Penalty JIT Warmup...", file=sys.stderr)

        async def _run_native_warmup():
            try:
                # First request will trigger the lazy INT4 quantization
                prompt = TextPrompt(prompt="Xin chào, hãy kích hoạt CUDA Graphs và FlashInfer memory pool ngay lập tức. Đây là một câu rất dài để test TTFT.")
                params = SamplingParams(max_tokens=16, temperature=0.0)
                warmup_rounds = int(os.getenv("VLLM_CUDAGRAPH_NUM_OF_WARMUPS", "10"))
                for i in range(warmup_rounds):
                    print(f"[Antigravity v21.0] Native Warmup Request {i+1}/{warmup_rounds}...", file=sys.stderr)
                    results_generator = engine.generate(prompt, params, request_id=f"native_warmup_v21_{i}")
                    async for _ in results_generator:
                        pass
                print(f"[Antigravity Phase 7 v21.0] Native Zero-Penalty Warmup COMPLETE ({warmup_rounds} rounds)!", file=sys.stderr)
            except Exception as w_err:
                print(f"[Antigravity Phase 7 v21.0] Native Warmup Warning (non-fatal): {w_err}", file=sys.stderr)

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(_run_native_warmup())
            else:
                loop.run_until_complete(_run_native_warmup())
        except Exception as l_err:
            print(f"[Antigravity Phase 7 v21.0] Asyncio Loop execution note: {l_err}", file=sys.stderr)

        return engine

    AsyncLLMEngine.from_engine_args = _patched_from_engine_args
    print("[Antigravity Phase 7 v21.0] Successfully installed AsyncLLMEngine native warmup patch!", file=sys.stderr)

except Exception as hook_err:
    print(f"[Antigravity Phase 7 v21.0] Native Warmup Hook Error: {hook_err}", file=sys.stderr)
