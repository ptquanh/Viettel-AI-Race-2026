# Kết quả Benchmark - 11:45 11/07/2026 (STT 81 - FP8 weights + Chunked Prefill (chunk 4096) 🔥)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--quantization fp8` + `--enable-chunked-prefill=True` + `--max-num-batched-tokens=4096` + `OMP_NUM_THREADS=3`
- **Mục đích**: Kết hợp weights FP8 với Chunked Prefill kích thước lớn (4096 tokens). Kích thước chunk lớn giúp giảm 8 lần số bước lập lịch (scheduling overhead) so với chunk size 512, giảm nghẽn CPU 3 cores trong khi vẫn bảo vệ luồng decode.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
