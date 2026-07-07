# Kết quả Benchmark - Slot 6 07/07/2026 (max-num-batched-tokens=32768 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--max-num-batched-tokens=32768` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc tăng mạnh số lượng batched tokens cho chunked prefill lên 32k (gần với kích thước context thực tế 20k-42k) có giúp prefill hoàn thành trong 1-2 chunks, từ đó kéo giảm trễ TTFT P95 tail xuống dưới 3000ms hay không.

## Chỉ số đo được

TBD

---
