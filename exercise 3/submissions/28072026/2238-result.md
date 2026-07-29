# Kết quả Benchmark - 22:38 28/07/2026 (Slot 14 - Image v20.0 CUTLASS FP8 + Golden Combo Sweep)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Cấu hình tổng hợp Golden Combo: `GPU_MEM=0.94` + Capture `[1..32]`).
- **Mục đích**: Tinh chỉnh tổng hợp cho đợt nộp đêm muộn.

## Kết quả thử nghiệm Slot 2238

- **Điểm chung cuộc (ERS)**: `57.7900`
- **F_delta**: `1.0`
- **Penalty**: `1.0`
- **Accuracy Drop**: `0%`
- **TTFT P50**: `59ms`
- **TTFT P95**: `86ms`
- **TPOT (TBT Median)**: `4ms`
- **Số request lỗi**: `5 / 420`
- **Tokens per sec**: `0.0523`

### Đánh giá

Bị ảnh hưởng bởi nhiễu tải máy chủ BTC giờ cao điểm đêm muộn (22:38), khiến trễ TTFT P95 tạm thời tăng lên 86ms.
