# Kết quả Benchmark - 15:29 10/07/2026 (STT 66 - Ghost Strategy v3 on vLLM v0.22.1: KV Cache Tweak)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v3` + script hijack tiêm cấu hình vLLM v0.22.1 tối ưu: `--max-model-len 262144`, `--gpu-memory-utilization 0.95`, `--enable-prefix-caching`, `--max-num-seqs 48`, `--enable-chunked-prefill`, `--max-num-batched-tokens 2048`, `--no-enable-log-requests`.
- **Mục đích**: Chạy chiến thuật Bóng ma v3 trên nhân vLLM v0.22.1. Phân tích cho thấy TPOT bị nghẽn bởi KV cache memory bandwidth, không phải GIL scheduler. Giảm `max-num-seqs` xuống 48 để hạ TPOT thông qua việc giảm lượng dữ liệu KV cache phải đọc mỗi step. Bật Chunked Prefill để cứu vớt TTFT.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
