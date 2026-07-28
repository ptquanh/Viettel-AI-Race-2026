# Kết quả Benchmark - Slot 10 (Image v20.0 CUTLASS FP8 + Seqs=24 Concurrency Tuning)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Điều chỉnh `VLLM_MAX_NUM_SEQS=24` nhằm giảm GPU context switching & tranh chấp compute).
- **Mục đích**: Kiểm tra giả thuyết thu hẹp hàng đợi giúp ép TTFT P50 giảm xuống mốc ~45ms.

## Kết quả thử nghiệm Slot 10

**Trạng thái**: Đang chờ nộp & chấm điểm...
