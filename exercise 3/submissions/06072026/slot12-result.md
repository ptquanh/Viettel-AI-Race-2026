# Kết quả Benchmark - Slot 12 06/07/2026 (gpu-memory-utilization 0.90 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--gpu-memory-utilization=0.90` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc hạ thấp giới hạn sử dụng GPU memory xuống 0.90 khi đi kèm quantization weights có cải thiện độ ổn định hoặc trễ do tránh phân mảnh bộ nhớ hay không.


## Chỉ số đo được

TBD

---
