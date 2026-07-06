# Kết quả Benchmark - 20:48 06/07/2026 (Slot 12 - gpu-memory-utilization 0.90 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--gpu-memory-utilization=0.90` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc hạ thấp giới hạn sử dụng GPU memory xuống 0.90 khi đi kèm quantization weights có cải thiện độ ổn định hoặc trễ do tránh phân mảnh bộ nhớ hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **17.58** (ERS = 17.58, Accuracy Drop = 0%, Penalty = 1)
- **Số lượng passed SLO:** **84 / 120** (Giảm từ 85)
- **TTFT P50:** **627 ms** (Tệ hơn so với 569 ms)
- **TTFT P95:** **8739 ms** (Tệ hơn so với 8520 ms)
- **TPOT Median (tbt_median):** **51 ms** (Bằng với baseline)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **0%** (An toàn tuyệt đối)

### Nhận xét & Phân tích:

1. **Hiệu năng suy giảm (-1.41 điểm):** Điểm số giảm xuống 17.58. Số lượng passed SLO giảm xuống còn 84.
2. **Ảnh hưởng của việc thu hẹp VRAM cho KV Cache:** Khi hạ `--gpu-memory-utilization` xuống 0.90, vLLM có ít bộ nhớ hơn cho KV Cache block pool. Điều này dẫn đến tỉ lệ cache hit thấp hơn khi chạy trace gồm nhiều phiên hội thoại dài song song, đẩy TTFT trung bình lên do phải tái tính toán nhiều hơn.
3. **Kết luận:** **CẤM HẠ `--gpu-memory-utilization` xuống 0.90**.

---
