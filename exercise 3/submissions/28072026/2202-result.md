# Kết quả Benchmark - 22:02 28/07/2026 (Slot 09 - Image v20.0 CUTLASS FP8 + GPU_MEM=0.94)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Thử nghiệm `GPU_MEM=0.94` nhằm giảm overhead GPU memory allocator).
- **Mục đích**: Đo đạc tác động của việc hạ GPU memory reservation xuống 94%.

## Kết quả thử nghiệm Slot 2202

- **Điểm chung cuộc (ERS)**: `57.4100`
- **F_delta**: `1.0`
- **Penalty**: `1.0`
- **Accuracy Drop**: `0%`
- **TTFT P50**: `61ms`
- **TTFT P95**: `85ms`
- **TPOT (TBT Median)**: `4ms`
- **Số request lỗi**: `5 / 420`
- **Tokens per sec**: `0.0524`

### Đánh giá

Trễ TTFT P95 (85ms) tăng nhẹ do nhiễu tải hệ thống khung 22:00, khiến điểm ERS tạm thời ở mức 57.41đ.
