# Kết quả Benchmark - 15:30 11/07/2026 (STT 89 - FP8 weights + Custom FP8 KV + Chunk 4096 + Warmup)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup` + `--quantization fp8` + `--kv-cache-dtype fp8` + `--enable-chunked-prefill` (hijacked) + Warmup.
- **Mục đích**: Loại bỏ TTFT 2036ms của STT 83 bằng cách JIT compile Triton kernels thông qua 1 request warmup ban đầu, kết hợp giữ TPOT 31ms.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
