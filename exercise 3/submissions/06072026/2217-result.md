# Kết quả Benchmark - 22:17 06/07/2026 (Slot 13 - gpu-memory-utilization 0.92 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--gpu-memory-utilization=0.92` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc hạ thấp giới hạn sử dụng GPU memory xuống 0.92 khi đi kèm quantization weights có cải thiện độ ổn định hoặc trễ do tránh phân mảnh bộ nhớ hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **18.07** (ERS = 18.07, Accuracy Drop = 0%, Penalty = 1)
- **Số lượng passed SLO:** **85 / 120** (Bằng với baseline)
- **TTFT P50:** **609 ms** (Tệ hơn so với 569 ms)
- **TTFT P95:** **8488 ms** (Tương đương baseline 8520 ms)
- **TPOT Median (tbt_median):** **51 ms** (Bằng với baseline)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **0%** (An toàn tuyệt đối)

### Nhận xét & Phân tích:

1. **Hiệu năng giảm nhẹ (-0.92 điểm):** Điểm số giảm xuống 18.07. TTFT P50 tăng nhẹ từ 569ms lên 609ms.
2. **Khảo sát KV Cache Memory pool:** Tương tự như mốc 0.90, việc hạ xuống 0.92 làm co hẹp KV Cache block pool, tăng nhẹ số lần cache miss ở prefill phase của các request mới, khiến TTFT P50 tăng nhẹ. Tuy nhiên, nó khả quan hơn mốc 0.90 (17.58 điểm) do dung lượng cache lớn hơn một chút.
3. **Kết luận:** **KHÔNG DÙNG `--gpu-memory-utilization=0.92`**.

---
