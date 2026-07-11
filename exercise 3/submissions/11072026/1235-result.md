# Kết quả Benchmark - 12:35 11/07/2026 (STT 84 - FP8 weights + Custom FP8 KV + Chunk 4096)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8` + `--quantization fp8` + `--kv-cache-dtype fp8` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096`
- **Mục đích**: Kiểm tra song song lượng tử hóa FP8 KV Cache kết hợp với Chunked Prefill 4096 để giảm tải băng thông bộ nhớ và CPU scheduling overhead đồng thời.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
