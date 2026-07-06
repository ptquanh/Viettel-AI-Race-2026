# Kết quả Benchmark - 17:27 06/07/2026 (Slot 7 - enforce-eager Test)

- **Cấu hình**: Baseline mới (STT19: `--enable-chunked-prefill` + `--no-enable-log-requests`) + `--enforce-eager` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem flag tối ưu `--enforce-eager` có hoạt động ổn định trên phiên bản vLLM `v0.22.1` của BTC và cải thiện TTFT/TPOT hay không.

## Chỉ số đo được

**Chấm điểm thất bại**

- Lỗi: `job exceeded max duration of 2700s with no terminal callback` (Quá thời gian chạy tối đa 45 phút).

### Nhận xét & Phân tích:

1. **Lỗi treo benchmark / Timeout:** Việc bật `--enforce-eager` tắt cơ chế CUDA Graphs của vLLM. Trong môi trường hạn chế CPU (chỉ có 3 cores CPU), việc chạy eager mode khiến CPU liên tục phải xếp hàng giải quyết kernel launch từ GPU, dẫn đến nghẽn cổ chai CPU-GPU (contention).
2. **Hệ quả:** Tốc độ suy luận (TTFT và TPOT) bị chậm đi hàng chục lần dưới tải đồng thời, làm cho thời gian chạy vượt quá giới hạn 45 phút của hệ thống bench.
3. **Kết luận:** **CẤM DÙNG `--enforce-eager`** trên môi trường này. CUDA Graphs là bắt buộc để bypass overhead của CPU.

---
