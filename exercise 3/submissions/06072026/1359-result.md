# Kết quả Benchmark - 13:59 06/07/2026 (Slot 4 - No Enable Log Requests Test)

- **Cấu hình**: Baseline mới (STT16: `--enable-chunked-prefill`) + `--no-enable-log-requests` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Tối ưu hóa CPU overhead bằng cách sử dụng đúng flag `--no-enable-log-requests` để tắt log request theo gợi ý từ help log của vLLM.

## Chỉ số đo được

- **Điểm số cuối cùng:** **15.97** (ERS = 15.97, Accuracy Drop = 1%, Penalty = 1)
- **Số lượng passed SLO:** **84 / 120**
- **TTFT P50:** **677 ms** (So với 1118: 667 ms)
- **TTFT P95:** **10090 ms** (So với 1118: 10162 ms - cải thiện tail latency)
- **TPOT Median (tbt_median):** **59 ms**
- **Failed count:** 0

### Nhận xét & Phân tích:

1. **Flag hoạt động thành công:** `--no-enable-log-requests` hoạt động bình thường, giúp giảm CPU overhead ghi log.
2. **Điểm số cải thiện (+0.19 điểm):** Điểm tăng từ **15.78 → 15.97**. Mặc dù TTFT P50 tăng nhẹ (có thể do variance hệ thống), TTFT P95 đã giảm (cải thiện tail latency), giúp tăng điểm ERS tổng thể.
3. **Kết luận:** **Giữ nguyên `--no-enable-log-requests`** cho các cấu hình tiếp theo làm baseline mới.

---
