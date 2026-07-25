# Kết quả thử nghiệm Slot 08 (12:38) - Image v16 (Deep Fused Decode Kernels)

## 1. Thông tin chung

- **Thời gian chấm**: 25/07/2026 12:38:00
- **Submission File**: `exercise 3/submissions/25072026/08-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v16`
- **Điểm số**: **58.1200đ**

## 2. Chi tiết chỉ số

- **ERS**: 58.12
- **Total Requests**: 420
- **Failed Requests**: 7
- **TTFT P50**: 58 ms
- **TTFT P95**: 81 ms
- **TBT (TPOT) Median**: 4 ms
- **Tokens/sec**: 0.0595

## 3. Phân tích & Đánh giá

1. **TPOT vẫn kẹt ở 4ms**: Fused kernels cấp Triton Python/PyTorch chưa đủ để vượt qua giới hạn độ phân giải / hardware bottleneck (hoặc grader làm tròn TBT median = 4ms).
2. **Overhead & Noise**: Phức tạp hóa monkey-patch ở Python layer (RMSNorm + SiLU×Mul) tạo thêm CPU overhead trong đợt burst traffic lúc 12:38 PM, dẫn đến TTFT P50 bị đẩy lên 58ms và 7 requests rớt (fails).
3. **Kết luận**: **Image v14 FP8 Native (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14`) vẫn là động cơ ổn định và nhanh nhất (62.67đ)**. Loại bỏ v16, quay lại 100% Champion Config v14 cho các Golden Slots đêm nay.
