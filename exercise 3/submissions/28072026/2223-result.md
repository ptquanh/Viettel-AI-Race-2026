# Kết quả Benchmark - 22:23 28/07/2026 (Slot 12 - Image v20.0 CUTLASS FP8 + FULL_DECODE_ONLY Graph)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Đặt `VLLM_CUDAGRAPH_MODE=FULL_DECODE_ONLY`).
- **Mục đích**: Giải phóng VRAM prefill graphs nhằm tối ưu hóa trễ prefill cho các request context dài.

## Kết quả thử nghiệm Slot 2223

- **Điểm chung cuộc (ERS)**: `60.5200`
- **F_delta**: `1.0`
- **Penalty**: `1.0`
- **Accuracy Drop**: `0%`
- **TTFT P50**: `52ms`
- **TTFT P95**: `72ms`
- **TPOT (TBT Median)**: `4ms`
- **Số request lỗi**: `5 / 420`
- **Tokens per sec**: `0.0524`

### Đánh giá

Đạt **60.52đ**, trễ TTFT P50 giữ mức 52ms cực tốt và P95 ở 72ms.
