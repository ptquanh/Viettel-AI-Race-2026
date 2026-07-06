# Kết quả Benchmark - 16:52 06/07/2026 (Slot 6 - quantization fp8 Test)

- **Cấu hình**: Baseline mới (STT19: `--enable-chunked-prefill` + `--no-enable-log-requests`) + `--quantization=fp8` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem flag tối ưu `--quantization=fp8` có hoạt động ổn định trên phiên bản vLLM `v0.22.1` của BTC và cải thiện TTFT/TPOT hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **18.99** (ERS = 18.99, Accuracy Drop = 1%, Penalty = 1)
- **Số lượng passed SLO:** **85 / 120** (Tăng từ 84)
- **TTFT P50:** **569 ms** (Cải thiện cực mạnh từ 677 ms, giảm ~16%)
- **TTFT P95:** **8520 ms** (Cải thiện cực mạnh từ 10090 ms, giảm ~15.5%)
- **TPOT Median (tbt_median):** **51 ms** (Cải thiện mạnh từ 59 ms, giảm ~13.5%)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **1%** (Cực kỳ an toàn, f(Δ) = 1.0, không bị phạt)

### Nhận xét & Phân tích:

1. **Thành công vượt bậc (+3.02 điểm):** Điểm số vọt từ **15.97 → 18.99**. Đây là đòn bẩy hiệu năng lớn nhất từ đầu giải đấu đến nay.
2. **Quantization FP8 hoạt động hoàn hảo:**
   - Việc chuyển model weights sang FP8 giúp giảm 50% kích thước mô hình lưu trong VRAM, giải phóng băng thông truyền tải GPU trong mỗi bước prefill và decode.
   - Kết quả là TTFT P50/P95 giảm cực sâu (TTFT P50 xuống còn 569ms, P95 xuống còn 8520ms).
   - TPOT (TBT) giảm từ 59ms xuống còn 51ms. Do TPOT đã tiến sát ngưỡng 45ms, một số request đã bắt đầu có TPOT < 45ms và đóng góp điểm cộng ERS thực tế!
3. **Độ chính xác được bảo toàn:** Trái ngược với FP8 KV Cache (STT17 bị tụt tới 9% accuracy), FP8 Weight Quantization chỉ làm sụt giảm **1%** accuracy (nằm trong biên độ biến động ngẫu nhiên), bảo đảm không bị phạt điểm.
4. **Kết luận:** **`--quantization=fp8` trở thành cấu hình mặc định (Baseline mới) từ thời điểm này.**

---
