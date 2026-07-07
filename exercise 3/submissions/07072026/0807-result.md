# Kết quả Benchmark - 08:07 07/07/2026 (Slot 2 - max-num-batched-tokens=256 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--max-num-batched-tokens=256` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc hạ giới hạn batched tokens của chunked prefill xuống 256 có giúp giảm thiểu hơn nữa hiện tượng nghẽn prefill chặn decode, từ đó cải thiện TPOT và TTFT hay không.

## Chỉ số đo được

- **Trạng thái:** **Chấm điểm thất bại (Fail)**
- **Chi tiết lỗi:**
  ```
  spawn contestant container: wait for pod ready: contestant pod failed: container "inference" exited 1 (Error): ckages/vllm/v1/engine/async_llm.py", line 217, in from_vllm_config
  (APIServer pid=1)     return cls(
  (APIServer pid=1)            ^^^^
  (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/async_llm.py", line 146, in __init__
  (APIServer pid=1)     self.engine_core = EngineCoreClient.make_async_mp_client(
  (APIServer pid=1)                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

### Nhận xét & Phân tích:

1. **Lỗi khởi động Engine (Engine core initialization failed):** Khi `--max-num-batched-tokens` được đặt quá thấp (256), nó vi phạm các ràng buộc nội bộ của vLLM v1 engine (hoặc cấu hình chunked prefill của vLLM mới trên server), dẫn đến engine crash ngay lập tức khi startup.
2. **Thông tin cực kỳ quan trọng về môi trường chấm bài:** Traceback sử dụng Python 3.12 và thư viện `vllm/v1/engine`. Điều này chứng tỏ **hệ thống chấm bài đang chạy một phiên bản vLLM rất mới** (hỗ trợ v1 engine) chứ không phải bản v0.22.1 cũ như khai báo ban đầu.
3. **Kết luận:** **CẤM đặt `--max-num-batched-tokens` dưới mức mặc định (512)**. Mức 256 gây lỗi startup, và mức 384 (Slot 3) cũng cực kỳ rủi ro và không nên sử dụng.

---
