# Kết quả Benchmark - 11:45 11/07/2026 (STT 81 - FP8 weights + Chunked Prefill (chunk 4096) 🔥)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--quantization fp8` + `--enable-chunked-prefill=True` + `--max-num-batched-tokens=4096` + `OMP_NUM_THREADS=3`
- **Mục đích**: Kết hợp weights FP8 với Chunked Prefill kích thước lớn (4096 tokens). Kích thước chunk lớn giúp giảm 8 lần số bước lập lịch (scheduling overhead) so với chunk size 512, giảm nghẽn CPU 3 cores trong khi vẫn bảo vệ luồng decode.

## Chỉ số đo được

**Chấm điểm thất bại (Fail)**

### Lỗi khởi động:
`api_server.py: error: argument --enable-chunked-prefill/--no-enable-chunked-prefill: ignored explicit argument 'True'`

### Phân tích nguyên nhân:
1. **Lỗi cú pháp argument**: Tham số `--enable-chunked-prefill` trong vLLM là cờ boolean (`store_true`). Việc truyền `--enable-chunked-prefill=True` (hoặc có giá trị đi kèm) khiến parser của vLLM báo lỗi cú pháp và container lập tức thoát (exit code 2).
2. **Khắc phục**: Đối với các cờ boolean dạng này, chỉ cần truyền `--enable-chunked-prefill` mà không đi kèm `=True`.

### Giải pháp sửa đổi trong tương lai:
Sửa đổi các tệp cấu hình docker-compose để truyền đúng cờ `--enable-chunked-prefill` (không gán giá trị).
