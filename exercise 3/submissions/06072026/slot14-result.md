# Kết quả Benchmark - Slot 14 06/07/2026 (gpu-memory-utilization 0.98 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--gpu-memory-utilization=0.98` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc tăng giới hạn sử dụng GPU memory lên 0.98 khi đi kèm quantization weights có giúp tăng dung lượng KV Cache và tăng throughput hay không.


## Chỉ số đo được

TBD

---
