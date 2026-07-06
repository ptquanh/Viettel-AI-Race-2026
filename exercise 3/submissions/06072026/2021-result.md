# Kết quả Benchmark - 20:21 06/07/2026 (Slot 11 - max-num-seqs=128 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--max-num-seqs=128` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc nâng giới hạn request xử lý đồng thời lên 128 có giúp tối ưu hóa luồng xử lý và giảm CPU scheduling overhead khi weights đã lượng tử hóa FP8 hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **17.71** (ERS = 17.71, Accuracy Drop = 0%, Penalty = 1)
- **Số lượng passed SLO:** **85 / 120** (Bằng với baseline)
- **TTFT P50:** **618 ms** (Tệ hơn so với 569 ms)
- **TTFT P95:** **8497 ms** (Tương đương baseline 8520 ms)
- **TPOT Median (tbt_median):** **51 ms** (Bằng với baseline)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **0%** (An toàn tuyệt đối)

### Nhận xét & Phân tích:

1. **Hiệu năng sụt giảm (-1.28 điểm):** Điểm số giảm xuống 17.71. TTFT P50 tăng từ 569ms lên 618ms.
2. **Ảnh hưởng của việc cấu hình cứng `max-num-seqs`:** Tương tự như mốc 256, việc đặt cứng `--max-num-seqs=128` làm hạn chế tính linh động của cơ chế scheduler động của vLLM, đồng thời kéo dài TTFT trung bình do giới hạn số lượng request song song được xếp hàng xử lý trong mỗi step.
3. **Kết luận:** **CẤM DÙNG `--max-num-seqs`**. Hãy để vLLM tự động lập lịch và tối ưu hóa luồng requests.

---
