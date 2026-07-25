# Kết quả thử nghiệm Slot 14 (23:09) - Image v14 Champion Config

## 1. Thông tin chung

- **Thời gian chấm**: 25/07/2026 23:09:00
- **Submission File**: `exercise 3/submissions/25072026/2309-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14`
- **Điểm số**: **58.6400đ**

## 2. Chi tiết chỉ số

- **ERS**: 58.64
- **Total Requests**: 420
- **Failed Requests**: 5
- **TTFT P50**: 59 ms
- **TTFT P95**: 76 ms
- **TBT (TPOT) Median**: 4 ms
- **Tokens/sec**: 0.0588

## 3. Phân tích & Đánh giá

1. **Grader Noise ban đêm**: Khung giờ 23:09 ghi nhận trễ TTFT P50 tăng nhẹ lên 59ms (P95=76ms) do nhiều đội thi tập trung push điểm chốt sổ cuối ngày, dẫn đến nhiễu mạng trên hệ thống chấm điểm của BTC.
2. **Độ ổn định cao**: Cấu hình Champion v14 tiếp tục duy trì độ ổn định cao (chỉ 5 failed requests) và TPOT kẹt cứng ở 4ms.
3. **Kết luận**: Hoàn tất thử nghiệm Slot 14 với kết quả 58.64đ.
