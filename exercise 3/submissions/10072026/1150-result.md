# Kết quả Benchmark - 11:50 10/07/2026 (STT 65 - Ghost Strategy v2: vLLM v0.5.2 + Online FP8)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-modern-hijack` + script hijack tiêm cấu hình vLLM v0.5.2 tối ưu: `--max-model-len 43008`, `--gpu-memory-utilization 0.93`, `--quantization fp8`, `--enable-chunked-prefill`, `--max-num-batched-tokens 2048`, `--enable-prefix-caching`, `--max-num-seqs 64`, `--disable-log-requests`, `--disable-log-stats`.
- **Mục đích**: Lần chạy đầu tiên sử dụng Chiến thuật Bóng ma v2 trên nhân vLLM v0.5.2 đời mới nhằm khai thác vòng lặp giải mã bằng C++ và Chunked Prefill tối ưu sâu để bứt phá khỏi giới hạn TPOT 51ms (ceilling 45ms), kích hoạt điểm TPOT.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
