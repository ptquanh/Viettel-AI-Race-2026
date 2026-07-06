# Kết quả Benchmark - 20:04 06/07/2026 (Slot 10 - max-num-seqs=256 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--max-num-seqs=256` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc nâng giới hạn request xử lý đồng thời lên 256 có giúp tận dụng năng lực tính toán tốt hơn khi weights đã được lượng tử hóa FP8 hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **17.82** (ERS = 17.82, Accuracy Drop = 4%, Penalty = 1)
- **Số lượng passed SLO:** **85 / 120** (Bằng với baseline)
- **TTFT P50:** **618 ms** (Tệ hơn so với 569 ms)
- **TTFT P95:** **8390 ms** (Cải thiện nhẹ từ 8520 ms)
- **TPOT Median (tbt_median):** **51 ms** (Bằng với baseline)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **4%** (Không bị phạt điểm)

### Nhận xét & Phân tích:
1. **Hiệu năng giảm nhẹ (-1.17 điểm):** Điểm số giảm xuống 17.82. Mặc dù số lượng passed SLO vẫn giữ ở mức 85, nhưng trễ TTFT trung bình (P50) bị kéo dài từ 569ms lên 618ms.
2. **Ảnh hưởng của Concurrency quá cao:** Nâng `max-num-seqs` lên 256 khiến scheduler của vLLM phải xử lý cùng lúc quá nhiều sequence trong hàng đợi. Việc này làm tăng chi phí quản lý bộ nhớ đệm (caching overhead) và tăng CPU contention cho khâu scheduling, làm TTFT trung bình tăng.
3. **Độ chính xác GPQA Diamond:** Sụt giảm 4% (nằm trong biên độ biến động ngẫu nhiên, không bị phạt điểm).
4. **Kết luận:** **KHÔNG DÙNG `--max-num-seqs=256`**.

---
