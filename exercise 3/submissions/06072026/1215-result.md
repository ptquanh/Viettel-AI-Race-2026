# Kết quả Benchmark - 12:15 06/07/2026 (Slot 2 - FP8 KV Cache Test)

- **Cấu hình**: Baseline mới (STT16: `--enable-chunked-prefill`) + `--kv-cache-dtype=fp8` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem flag tối ưu `--kv-cache-dtype=fp8` có hoạt động ổn định trên vLLM `v0.22.1` của BTC và cải thiện TTFT/TPOT hay không.

## Chỉ số đo được

TBD

---
