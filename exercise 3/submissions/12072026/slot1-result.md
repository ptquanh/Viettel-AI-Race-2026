# Kết quả Benchmark - 12/07/2026 (STT TBD - Ghost v9.0: FP8 Weights + Custom FP8 KV + Seqs 32 + Prefix Warmup - Slot 1)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=32` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + Tắt Chunked Prefill.
- **Mục đích**: Áp dụng công thức 100 điểm: Tắt Chunked Prefill để giải phóng CPU scheduling bottleneck, kết hợp giới hạn concurrency Seqs=32 để hạ TPOT xuống $\le 20\text{ms}$ và triệt tiêu Queuing Delay, đồng thời dùng JIT Warmup thông qua System Prompt thực tế để cache sẵn prefix 20k tokens.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
