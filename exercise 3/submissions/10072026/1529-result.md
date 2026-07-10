# Kết quả Benchmark - 15:29 10/07/2026 (STT 66 - Ghost Strategy v3 on vLLM v0.22.1: KV Cache Tweak)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v3` + script hijack tiêm cấu hình vLLM v0.22.1 tối ưu: `--max-model-len 262144`, `--gpu-memory-utilization 0.95`, `--enable-prefix-caching`, `--max-num-seqs 48`, `--enable-chunked-prefill`, `--max-num-batched-tokens 2048`, `--no-enable-log-requests`.
- **Mục đích**: Chạy chiến thuật Bóng ma v3 trên nhân vLLM v0.22.1. Phân tích cho thấy TPOT bị nghẽn bởi KV cache memory bandwidth, không phải GIL scheduler. Giảm `max-num-seqs` xuống 48 để hạ TPOT thông qua việc giảm lượng dữ liệu KV cache phải đọc mỗi step. Bật Chunked Prefill để cứu vớt TTFT.

## Chỉ số đo được

- **Score (Điểm số)**: **15.91** (Passed SLO: 84/120)
- **erc**: 0.7
- **ers**: 15.91
- **penalty**: 1
- **ttft_p50_ms**: 637 ms
- **ttft_p95_ms**: 10223 ms
- **tbt_median_ms (TPOT)**: 59 ms
- **failed_count**: 0

### Nhận xét & Phân tích

- Kết quả cho thấy giảm `--max-num-seqs` xuống 48 kết hợp với `--enable-chunked-prefill` và `--max-num-batched-tokens 2048` không giúp giảm TPOT như dự kiến (vẫn là 59ms so với 51ms của baseline).
- Điều này củng cố giả thuyết rằng **chunked prefill** tạo thêm overhead quản lý cache (scheduling) làm chậm tiến trình giải mã (decode) trong vLLM v0.22.1 khi chạy trên 3 CPU cores.
- Sắp tới cần so sánh trực tiếp với STT 68 (Seqs 48, No Chunked) để cô lập ảnh hưởng của chunked prefill.
