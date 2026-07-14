# Kết quả Benchmark - 14/07/2026 (STT TBD - Ghost v9.3: Seqs 32 + Warmup + Custom Kernel - Slot 2)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=32` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + Tắt Chunked Prefill + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Nộp lại cấu hình của đợt chạy 0747 ngày 12/07 nhưng bổ sung biến môi trường `VLLM_CUSTOM_KERNEL=1` để kích hoạt Monkey Patch và Triton Kernel dequantize KV Cache tối ưu, khắc phục lỗi TPOT 56ms và TTFT 3.7s.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
