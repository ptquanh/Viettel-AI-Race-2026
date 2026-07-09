# Kết quả Benchmark - 09:15 09/07/2026 (STT 55 - Modern vLLM v0.22.1 Hijack + CUDA Graph Capture Optimized)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack` + các tham số tối ưu hóa (max-model-len=43008, memory=0.98, max-cudagraph-capture-size=45000, quantization=fp8).
- **Mục đích**: Tối ưu hóa tối đa VRAM và kích hoạt CUDA Graphs đầy đủ cho các request độ dài lớn (lên tới 45k tokens) nhằm giảm TPOT và TTFT.

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

Do log root cause bị cắt mất bởi hệ thống hiển thị của portal, nhưng dựa trên cấu trúc trace lỗi ở trên:

1. `Engine core initialization failed` xảy ra trong quá trình khởi tạo GPU worker của vLLM v1.
2. Nguyên nhân phổ biến nhất gây ra lỗi khởi tạo worker process trên hạ tầng ảo hóa k8s là **OOM VRAM** khi set `gpu-memory-utilization=0.98` hoặc xung đột thiết lập bộ nhớ đệm (do GPU MiG H200 18GB bị giới hạn nghiêm ngặt VRAM hoặc có CPU/host RAM overhead khi fork worker).

---

_Kết luận: Cần hạ `--gpu-memory-utilization` về lại mức an toàn `0.92` hoặc `0.90` để tránh lỗi khởi tạo GPU Worker._
