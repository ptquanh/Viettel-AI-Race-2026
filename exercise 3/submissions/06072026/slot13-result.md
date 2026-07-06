# Kết quả Benchmark - Slot 13 06/07/2026 (gpu-memory-utilization 0.92 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--gpu-memory-utilization=0.92` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc hạ thấp giới hạn sử dụng GPU memory xuống 0.92 khi đi kèm quantization weights có cải thiện độ ổn định hoặc trễ do tránh phân mảnh bộ nhớ hay không.


## Chỉ số đo được

TBD

---
