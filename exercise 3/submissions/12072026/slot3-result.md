# Kết quả Benchmark - 12/07/2026 (STT TBD - Ghost v9.2: Warmup Ablation - Seqs 32 - Slot 3)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=32` + `quantization=fp8` + `kv-cache-dtype=fp8` + Warmup Disabled (`VLLM_WARMUP=0`) + Tắt Chunked Prefill.
- **Mục đích**: Nghiên cứu đối chứng (ablation study) khi tắt warmup. Thử nghiệm này giúp đánh giá chính xác tác động của Warmup JIT đến TTFT, đồng thời đóng vai trò là phương án dự phòng an toàn nếu cơ chế Warmup gặp trục trặc kỹ thuật hoặc gây lỗi runtime trên Portal.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
