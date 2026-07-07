# Kết quả Benchmark - 08:17 07/07/2026 (Slot 3 - swap-space=0 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--swap-space=0` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc tắt hoàn toàn CPU swap memory (mặc định là 4GB) có giúp giảm thiểu overhead quản lý và đồng bộ trang nhớ giữa RAM CPU và GPU, từ đó cải thiện độ trễ hay không.

## Chỉ số đo được

- **Trạng thái:** **Chấm điểm thất bại (Fail)**
- **Chi tiết lỗi:**
  ```
  api_server.py: error: unrecognized arguments: --swap-space=0
  ```

### Nhận xét & Phân tích:

1. **Tham số đã bị gỡ bỏ (Unrecognized argument):** Tham số `--swap-space` đã bị loại bỏ hoàn toàn trong các phiên bản mới của vLLM trên hệ thống chấm bài.
2. **Xác nhận phiên bản vLLM mới:** Các cờ lỗi cho thấy hệ thống đang chạy vLLM thế hệ mới (hỗ trợ các config mới như `--performance-mode`, `--attention-config`).
3. **Kết luận:** **CẤM DÙNG `--swap-space`**. Bỏ qua toàn bộ các thử nghiệm liên quan đến swap space (Slot 3 & 4 cũ).

---
