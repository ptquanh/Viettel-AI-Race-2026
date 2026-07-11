# Kết quả Benchmark - 12:03 11/07/2026 (STT 83 - FP8 weights + Custom INT8 KV + Chunk 4096)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-int8` + `--quantization fp8` + `--kv-cache-dtype int8_per_token_head` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096`
- **Mục đích**: Kiểm tra song song lượng tử hóa INT8 KV Cache (per-token-head) kết hợp với Chunked Prefill 4096 để xem có giải quyết được nghẽn CPU và nghẽn băng thông bộ nhớ cùng lúc hay không.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
