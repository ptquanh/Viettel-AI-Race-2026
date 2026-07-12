# Kết quả Benchmark - 12/07/2026 (STT TBD - Ghost v9.1: Concurrency Tweak - Seqs 24 - Slot 2)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=24` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + Tắt Chunked Prefill.
- **Mục đích**: Tinh chỉnh giới hạn concurrency từ 32 xuống 24 để tối ưu hóa thêm tốc độ decode, nỗ lực đưa TPOT xuống mức vật lý cực hạn (< 15ms) trên GPU trong khi vẫn đủ năng lực xử lý một đợt 20 requests/5 giây.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
