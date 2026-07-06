# Kết quả Benchmark - 13:36 06/07/2026 (Slot 3 - Disable Log Requests Test - THẤT BẠI)

- **Cấu hình**: Baseline mới (STT16: `--enable-chunked-prefill`) + `--disable-log-requests` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem flag `--disable-log-requests` có giúp giảm CPU overhead từ việc ghi log hay không.

## Chỉ số đo được

**Chấm điểm thất bại**

- Container "inference" exited 2 (Error)
- Log lỗi: `api_server.py: error: unrecognized arguments: --disable-log-requests`

### Phát hiện quan trọng từ help log:

Trong log lỗi vLLM của BTC có xuất hiện các flag khả dụng sau:

- `--no-enable-log-requests` (để tắt log request)
- `--disable-log-stats` (để tắt log thống kê định kỳ)

Do đó, flag `--disable-log-requests` không tồn tại ở phiên bản này, mà thay vào đó phải dùng `--no-enable-log-requests`.

---
