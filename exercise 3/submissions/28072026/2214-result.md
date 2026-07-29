# Kết quả Benchmark - 22:14 28/07/2026 (Slot 11 - Image v20.0 CUTLASS FP8 + Seqs=48)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Thử nghiệm `VLLM_MAX_NUM_SEQS=48`).
- **Mục đích**: Kiểm tra khả năng xử lý đồng thời tối đa khi mở rộng hàng đợi scheduler.

## Kết quả thử nghiệm Slot 2214

- **Điểm chung cuộc (ERS)**: `60.5100`
- **F_delta**: `1.0`
- **Penalty**: `1.0`
- **Accuracy Drop**: `0%`
- **TTFT P50**: `53ms`
- **TTFT P95**: `73ms`
- **TPOT (TBT Median)**: `4ms`
- **Số request lỗi**: `5 / 420`
- **Tokens per sec**: `0.0524`

### Đánh giá

Đạt điểm số ổn định **60.51đ**, duy trì trễ TTFT P50 ở mức 53ms và TPOT 4ms.
