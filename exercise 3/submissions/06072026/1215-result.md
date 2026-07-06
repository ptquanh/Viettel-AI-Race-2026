# Kết quả Benchmark - 12:15 06/07/2026 (Slot 2 - FP8 KV Cache Test)

- **Cấu hình**: Baseline mới (STT16: `--enable-chunked-prefill`) + `--kv-cache-dtype=fp8` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem flag tối ưu `--kv-cache-dtype=fp8` có hoạt động ổn định trên vLLM `v0.22.1` của BTC và cải thiện TTFT/TPOT hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **10.24** (ERS = 10.24, Accuracy Drop = 9%, Penalty = 1)
- **Số lượng passed SLO:** **75 / 120** (Giảm từ 84)
- **TTFT P50:** **958 ms** (Tăng từ 667 ms)
- **TTFT P95:** **12363 ms** (Tăng từ 10162 ms)
- **TPOT Median (tbt_median):** **71 ms** (Tăng từ 59 ms)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **9%** (Gần chạm ngưỡng phạt 10%)

### Nhận xét & Phân tích:

1. **Hiệu năng suy giảm nghiêm trọng:** Bật `--kv-cache-dtype=fp8` làm điểm số giảm mạnh từ **15.78 → 10.24** (-5.54 điểm), số request pass SLO giảm từ 84 xuống 75.
2. **Độ trễ tăng cao:**
   - TTFT P50 tăng 43% (958ms vs 667ms).
   - TPOT (TBT) tăng 20% (71ms vs 59ms).
   - Nguyên nhân: Việc quantize/dequantize KV cache sang FP8 trong phiên bản vLLM `v0.22.1` trên phần cứng/phần mềm này gây ra overhead tính toán lớn hơn nhiều so với lượng băng thông bộ nhớ tiết kiệm được.
3. **Độ chính xác bị ảnh hưởng:** `accuracy_drop` lên tới 9% (rất nguy hiểm, chỉ cần sụt giảm thêm 1% nữa là sẽ bắt đầu bị phạt điểm theo hệ số f(Δ)).
4. **Kết luận:** **CẤM/TRÁNH sử dụng `--kv-cache-dtype=fp8`** cho các cấu hình tiếp theo.

---
