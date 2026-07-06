# Kết quả Benchmark - 17:48 06/07/2026 (Slot 8 - OMP_NUM_THREADS=1 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `OMP_NUM_THREADS=1` env var (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc giới hạn CPU Thread limit có giúp ổn định hiệu năng, giảm contention trên 3 CPU cores hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **17.33** (ERS = 17.33, Accuracy Drop = 0%, Penalty = 1)
- **Số lượng passed SLO:** **83 / 120** (Giảm từ 85)
- **TTFT P50:** **624 ms** (Tệ hơn từ 569 ms)
- **TTFT P95:** **8995 ms** (Tệ hơn từ 8520 ms)
- **TPOT Median (tbt_median):** **50 ms** (Cải thiện siêu nhẹ từ 51 ms)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **0%** (An toàn tuyệt đối)

### Nhận xét & Phân tích:

1. **Hiệu năng suy giảm (-1.66 điểm):** Điểm số giảm từ 18.99 xuống 17.33. Số lượng request vượt qua SLO giảm xuống còn 83.
2. **Ảnh hưởng của CPU Threading:** Việc ép `OMP_NUM_THREADS=1` giới hạn các tính toán CPU của vLLM (như tokenizer, sequence scheduling, tensor conversion) chạy đơn luồng. Điều này tăng gánh nặng xử lý và làm chậm TTFT (TTFT P50 tăng lên 624ms).
3. **Mặc dù TPOT giảm nhẹ:** tbt_median giảm 1ms xuống còn 50ms nhờ giảm CPU contention khi decode, nhưng mức tăng TTFT quá lớn đã làm sập điểm số tổng.
4. **Kết luận:** **CẤM DÙNG `OMP_NUM_THREADS=1`**. Nên để hệ thống vLLM tự quản lý tài nguyên luồng của OpenMP.

---
