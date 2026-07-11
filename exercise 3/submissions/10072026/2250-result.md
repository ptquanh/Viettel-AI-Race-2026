# Kết quả Benchmark - 22:50 10/07/2026 (STT 73 - TurboQuant 4-bit KV Cache 🔥)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v4` + `--kv-cache-dtype turboquant_4bit_nc` + `--quantization fp8`
- **Mục đích**: Chạy thử nghiệm cờ nén INT4 KV cache thực tế được hỗ trợ trên portal của BTC (`turboquant_4bit_nc` có MSE tuning và Norm Correction để ổn định độ chính xác).

## Chỉ số đo được

- **Score (Điểm số)**: **Fail (Chấm điểm thất bại)**
- **Chi tiết lỗi**:
  ```
  spawn contestant container: wait for pod ready: contestant pod failed: container "inference" exited 1 (Error): ckages/vllm/v1/engine/async_llm.py", line 217, in from_vllm_config
  (APIServer pid=1)     return cls(
  (APIServer pid=1)            ^^^^
  (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/async_llm.py", line 146, in __init__
  (APIServer pid=1)     self.engine_core = EngineCoreClient.make_async_mp_client(
  (APIServer pid=1)                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  ...
  (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 1209, in wait_for_engine_startup
  (APIServer pid=1)     raise RuntimeError(
  (APIServer pid=1) RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
  ```

### Nhận xét & Phân tích

- Thử nghiệm cờ `turboquant_4bit_nc` thất bại do crash ngay khi khởi động vLLM Engine Core.
- Đáng chú ý, log trace chỉ ra vLLM đang cố khởi động bằng backend **vLLM V1** mới (`vllm/v1/engine/async_llm.py`). Engine V1 này chưa hoàn thiện và cực kỳ nhạy cảm với các cờ tối ưu hóa sâu hoặc các cấu hình GPU phân mảnh.
- Lỗi `Engine core initialization failed` xảy ra khi tiến trình Engine Core ngầm (GPU worker) gặp lỗi không thể load model/kernel hoặc crash trước khi thiết lập kết nối IPC với API Server.
- Khẳng định: Bản vLLM trên portal hiện tại đang cố kích hoạt V1 engine, và engine này không tương thích với cờ nén KV `turboquant_4bit_nc` dưới cấu hình tài nguyên của portal (3 CPU Cores / MiG H200).
