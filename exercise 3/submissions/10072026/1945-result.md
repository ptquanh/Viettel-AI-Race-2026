# Kết quả Benchmark - 17:01 10/07/2026 (STT 71 - INT8 KV Cache per-token-head)

- **Cấu hình**: Image `vllm-v0.22.1-hijack-v4` + `--kv-cache-dtype int8_per_token_head` + `--quantization fp8`
- **Mục đích**: Fallback nếu INT4 gây accuracy drop > 10%. INT8 giảm 2x KV bandwidth, kỳ vọng TPOT ~30ms.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
