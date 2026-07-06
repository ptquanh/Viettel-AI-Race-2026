# Kết quả Benchmark - 11:18 06/07/2026 (Slot 1 - Chunked Prefill Test)

- **Cấu hình**: Baseline + `--enable-chunked-prefill` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem flag tối ưu `--enable-chunked-prefill` có hoạt động ổn định trên phiên bản vLLM `v0.22.1` của BTC và cải thiện TTFT hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **15.78** (ERS = 15.78, Accuracy Drop = 0, Penalty = 1)
- **Số lượng passed SLO:** **84 / 120**
- **TTFT P50:** **667 ms** (Baseline: 670 ms)
- **TTFT P95:** **10162 ms** (Baseline: 10058 ms)
- **TPOT Median (tbt_median):** **59 ms**
- **Failed count:** 0

### Nhận xét & Phân tích:

1. **Flag hoạt động thành công:** `--enable-chunked-prefill` tương thích tốt với vLLM v0.22.1 trên môi trường BTC (không bị lỗi exited 2).
2. **Điểm số cải thiện (+0.52 điểm):** Điểm tăng từ **15.26 → 15.78**. Dù số request pass SLO vẫn giữ nguyên là 84, việc xen kẽ prefill và decode đã giúp cải thiện độ trễ trung bình của các request ngắn (thể hiện qua TTFT P50 giảm nhẹ và độ ổn định decode tốt hơn).
3. **Độ trễ TPOT (TBT) rất lớn:** Median TPOT = **59 ms** là khá cao (vượt qua Ceiling của TPOT là 45ms).
   - Do `s_tpot` dùng công thức: `clamp((45 - TPOT) / 25, 0, 1)²`.
   - Vì TPOT median = 59ms (> 45ms ceiling), nên phần lớn request có `s_tpot` gần hoặc bằng **0**!
   - Đây chính là cơ hội cực lớn: Nếu tối ưu được TPOT xuống dưới 45ms, điểm số của 84 request thành công sẽ tăng vọt!

---
