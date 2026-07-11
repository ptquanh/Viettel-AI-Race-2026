# Kết quả Benchmark - 23:18 10/07/2026 (STT 75 - TurboQuant 3-bit Key / 4-bit Value Hybrid KV Cache 🔥 - Đổi tên từ 2255)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v4` + `--kv-cache-dtype turboquant_k3v4_nc` + `--quantization fp8`
- **Mục đích**: Chạy thử nghiệm cờ nén cực cao của TurboQuant (`turboquant_k3v4_nc`) sử dụng 3-bit cho Key và 4-bit cho Value kèm Norm Correction. Nhắm tới TPOT tối thiểu (~15ms) thông qua việc cắt giảm tối đa băng thông KV cache đọc từ HBM GPU.

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

- Thử nghiệm cờ nén cao `turboquant_k3v4_nc` cũng thất bại với lỗi y hệt STT 73 (`RuntimeError: Engine core initialization failed`).
- Lỗi này khẳng định chắc chắn rằng khi sử dụng bất kỳ cờ nén dạng `turboquant_*_nc` (có cơ chế Norm Correction cần dùng thêm tensor scale động và kernel chuyên biệt), vLLM V1 engine ngầm định trên portal đều gặp crash ngay lập tức tại thời điểm cấp phát/khởi tạo GPU worker core.
- Kết luận kỹ thuật: **Không thể sử dụng các cờ TurboQuant dạng \_nc (Norm Correction)** hoặc có lẽ là toàn bộ các cờ nén KV cache nâng cao trên bản dựng vLLM V1 hiện tại của Grader portal.
