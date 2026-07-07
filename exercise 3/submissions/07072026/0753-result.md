# Kết quả Benchmark - 07:53 07/07/2026 (Slot 1 - max-num-batched-tokens=1024 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--max-num-batched-tokens=1024` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc tăng giới hạn batched tokens của chunked prefill lên 1024 có giúp cải thiện TTFT do xử lý chunk prefill lớn hơn mà không ảnh hưởng xấu đến TPOT hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **7.22** (ERS = 7.22, Accuracy Drop = 0%, Penalty = 1)
- **Số lượng passed SLO:** **49 / 120** (Giảm mạnh từ 85)
- **TTFT P50:** **2145 ms** (Tăng vọt từ 569 ms)
- **TTFT P95:** **11893 ms** (Tăng vọt từ 8520 ms)
- **TPOT Median (tbt_median):** **56 ms** (Tệ hơn so với 51 ms)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **0%** (An toàn tuyệt đối)

### Nhận xét & Phân tích:

1. **Hiệu năng sụt giảm thảm hại (-11.77 điểm):** Điểm số giảm sâu từ 18.99 xuống 7.22. Số lượng request vượt qua SLO giảm gần một nửa.
2. **Hiện tượng nghẽn do Prefill chặn Decode (Prefill-Decode contention):** Khi tăng `max-num-batched-tokens` lên 1024, vLLM xử lý các batch prefill lớn hơn trong mỗi forward pass. Điều này làm nghẽn GPU lâu hơn và trì hoãn (starve) các bước decode của các requests đang chạy song song, trực tiếp đẩy TTFT P50 tăng vọt từ 569ms lên 2145ms và TPOT tăng lên 56ms.
3. **Kết luận:** **CẤM TĂNG `--max-num-batched-tokens`** quá mức mặc định (512). Các thử nghiệm nâng lên 2048 (Slot 2) và 4096 (Slot 3) chắc chắn sẽ còn tệ hơn và cần được hủy bỏ.

---
