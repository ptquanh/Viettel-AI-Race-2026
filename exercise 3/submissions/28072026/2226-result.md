# Kết quả Benchmark - 22:26 28/07/2026 (Slot 13 - Image v20.0 CUTLASS FP8 + Warmup 5 Cycles)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Đặt `VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5`).
- **Mục đích**: Tinh chỉnh thời gian khởi chạy warmup cycles của CUDA Graph.

## Kết quả thử nghiệm Slot 2226

- **Điểm chung cuộc (ERS)**: `60.3500`
- **F_delta**: `1.0`
- **Penalty**: `1.0`
- **Accuracy Drop**: `0%`
- **TTFT P50**: `53ms`
- **TTFT P95**: `72ms`
- **TPOT (TBT Median)**: `4ms`
- **Số request lỗi**: `5 / 420`
- **Tokens per sec**: `0.0524`

### Đánh giá

Đạt điểm số ổn định **60.35đ**.
