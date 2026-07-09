# Kết quả Benchmark - 07:32 09/07/2026 (STT 55 - Custom LMDeploy AWQ v4 - Ghost Strategy)

- **Cấu hình**: Custom image `ptquanh/sandbox-runtime:lmd-bf16-v4` (Base `openmmlab/lmdeploy:v0.7.0-cu12` + Ghost Strategy + tokenizer files).
- **Cấu hình runtime**: `HIJACK_ENGINE=lmdeploy` + `LMDEPLOY_MODEL=/app/qwen_awq` + `LMDEPLOY_FORMAT=awq` + `LMDEPLOY_QUANT_POLICY=4` + `LMDEPLOY_CACHE_MAX=0.92` + `LMDEPLOY_SESSION_LEN=43008` + `LMDEPLOY_MAX_BATCH_SIZE=64` + `LMDEPLOY_PREFIX_CACHING=1` + `LMDEPLOY_PREFILL_TOKENS=8192`.
- **Mục đích**: Kiểm tra giải pháp "Ghost Strategy" di chuyển Python thật sang `python3_real` và gọi exec trực diện.

## Chỉ số đo được

**Chấm điểm thất bại**

```
spawn contestant container: wait for pod ready: contestant pod failed: container "inference" exited 1 (Error):
...
lmdeploy - WARNING - archs.py:48 - Fallback to pytorch engine because turbomind engine is not installed correctly.
...
lmdeploy.pytorch.engine.mp_engine.zmq_rpc.RPCServerDeadError: PyTorch ZMQ engine process is not alive.
```

---

## Phân tích lỗi

### ✅ Thành công:

1. **Ghost Strategy hoạt động hoàn hảo** - Không còn đệ quy, `python3_real` được gọi đúng.
2. **Tokenizer/preprocessor load thành công** - Không còn lỗi OSError.

### ❌ Thất bại:

1. **Turbomind C++ engine không khả dụng**: Khi `pip install -U lmdeploy` nâng cấp từ v0.7.0 lên v0.14.0, nó ghi đè package Python nhưng KHÔNG bao gồm các thư viện C++ Turbomind đã biên dịch sẵn trong base image. Turbomind cần được biên dịch riêng cho từng phiên bản CUDA/GPU.
2. **Fallback sang PyTorch engine → crash**: LMDeploy tự động fallback sang PyTorch engine, nhưng engine này crash (RPCServerDeadError) do worker process chết (có thể OOM hoặc CUDA mismatch).

### 🔧 Giải pháp tiếp theo:

- **Không nâng cấp lmdeploy** trong Dockerfile, giữ nguyên v0.7.0 có sẵn Turbomind.
- Hoặc: Dùng base image lmdeploy mới hơn đã tích hợp Turbomind cho Qwen3.5.
