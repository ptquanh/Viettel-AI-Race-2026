# Kết quả Benchmark - 14:01 11/07/2026 (STT 82 - FP8 weights + Chunked Prefill (chunk 4096) - Fixed 🔥)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--quantization fp8` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096` + `OMP_NUM_THREADS=3`
- **Mục đích**: Bản sửa lỗi cú pháp cho STT 81 (`1147`). Kết hợp weights FP8 với Chunked Prefill kích thước lớn (4096 tokens) để giảm scheduling overhead của CPU 3 cores và bảo vệ luồng decode.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
