# Kết quả Benchmark - 22:47 06/07/2026 (Slot 14 - gpu-memory-utilization 0.98 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--gpu-memory-utilization=0.98` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc tăng giới hạn sử dụng GPU memory lên 0.98 (tối đa hóa không gian KV Cache) có giúp cải thiện hiệu năng của RadixAttention và giảm trễ do tránh recomputation hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **18.24** (ERS = 18.24, Accuracy Drop = 0%, Penalty = 1)
- **Số lượng passed SLO:** **85 / 120** (Bằng với baseline)
- **TTFT P50:** **614 ms** (Tệ hơn so với 569 ms)
- **TTFT P95:** **8603 ms** (Tệ hơn so với 8520 ms)
- **TPOT Median (tbt_median):** **51 ms** (Bằng với baseline)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **0%** (An toàn tuyệt đối)

### Nhận xét & Phân tích:

1. **Hiệu năng giảm nhẹ (-0.75 điểm):** Điểm số giảm xuống 18.24. TTFT P50 tăng từ 569ms lên 614ms, TTFT P95 tăng từ 8520ms lên 8603ms.
2. **Quá giới hạn phân bổ bộ nhớ GPU (Memory overhead):** Đặt `--gpu-memory-utilization=0.98` ép vLLM chiếm dụng hầu hết VRAM. Điều này làm giảm không gian bộ nhớ tạm thời dành cho các thao tác runtime của PyTorch kernel hoặc CUDA execution workspace, gây ra overhead nhỏ trong khâu phân bổ bộ nhớ hoặc dọn dẹp phân mảnh bộ nhớ động, làm tăng nhẹ trễ TTFT.
3. **Kết luận:** Mức **`0.95`** là giá trị tối ưu tốt nhất cho `--gpu-memory-utilization` trong bài toán này. **KHÔNG DÙNG `--gpu-memory-utilization=0.98`**.

---
