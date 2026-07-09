# Kết quả Benchmark - 10:01 09/07/2026 (STT 56 - Modern vLLM v0.22.1 Hijack + VRAM 0.95 Patch)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack` + các tham số tối ưu hóa (max-model-len=43008, memory=0.95, max-cudagraph=8192, quantization=fp8).
- **Mục đích**: Bản vá giảm VRAM utilization từ 0.98 xuống 0.95 để vượt qua lỗi khởi tạo GPU Worker.

## Chỉ số đo được

**Chấm điểm thất bại**

```
spawn contestant container: wait for pod ready: contestant pod failed: container "inference" exited 1 (Error): ckages/vllm/v1/engine/async_llm.py", line 217, in from_vllm_config
(APIServer pid=1)     return cls(
(APIServer pid=1)            ^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/async_llm.py", line 146, in __init__
(APIServer pid=1)     self.engine_core = EngineCoreClient.make_async_mp_client(
(APIServer pid=1)                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/traci
... [truncated] ...
ib/python3.12/dist-packages/vllm/v1/engine/core_client.py", line 131, in make_async_mp_client
(APIServer pid=1)     return AsyncMPClient(*client_args)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
(APIServer pid=1)     return func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core_client.py", line 932, in __init__
(APIServer pid=1)     super().__init__(
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core_client.py", line 567, in __init__
(APIServer pid=1)     with launch_core_engines(
(APIServer pid=1)          ^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 144, in __exit__
(APIServer pid=1)     next(self.gen)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 1150, in launch_core_engines
(APIServer pid=1)     wait_for_engine_startup(
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 1209, in wait_for_engine_startup
(APIServer pid=1)     raise RuntimeError(
(APIServer pid=1) RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
```

## Phân tích lỗi

Mặc dù đã hạ `gpu-memory-utilization` xuống `0.95`, engine core vẫn lỗi khởi tạo. Lỗi này có thể do:

1. `--max-cudagraph-capture-size 8192` vẫn quá lớn đối với bộ nhớ đệm pre-allocated của CUDA Graphs trên GPU MiG H200.
2. Hoặc một tham số tối ưu hóa khác (`--max-num-batched-tokens 8192` hay `--max-model-len 43008`) xung đột với cấu hình của vLLM v1 engine mới.

---

_Kết luận: Cần bật `VLLM_LOGGING_LEVEL=DEBUG` để xuất log chi tiết của worker process lỗi, đồng thời hạ memory về `0.92` và gỡ bỏ cờ giới hạn CUDA Graph capture thủ công._
