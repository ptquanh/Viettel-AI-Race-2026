# Kết quả thử nghiệm Slot 11 (21:32) - Image v14 V1 Engine + Multi-step=4

## 1. Thông tin chung

- **Thời gian chấm**: 25/07/2026 21:32:00
- **Submission File**: `exercise 3/submissions/25072026/2132-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14`
- **Điểm số**: **56.6100đ**

## 2. Chi tiết chỉ số

- **ERS**: 56.61
- **Total Requests**: 420
- **Failed Requests**: 5
- **TTFT P50**: 62 ms
- **TTFT P95**: 91 ms
- **TBT (TPOT) Median**: 4 ms
- **Tokens/sec**: 0.0589

## 3. Phân tích & Đánh giá

1. **TPOT không đổi (vẫn 4ms)**: Kích hoạt `VLLM_USE_V1=1` kết hợp Multi-step Scheduling (`--num-scheduler-steps=4`) không làm giảm TPOT vượt qua ngưỡng 4ms trên môi trường benchmark của BTC.
2. **Overhead Prefill cao hơn**: V1 Engine làm TTFT P50 bị đẩy lên 62ms (P95=91ms) so với 45ms ở V0 Engine, khiến tổng điểm bị tụt xuống 56.61đ.
3. **Kết luận**: V1 Engine + Multi-step không hạ được TPOT 4ms nhưng lại làm xấu TTFT. Chiến lược tối ưu cho 4 slots còn lại (12-15) là 100% quay về **Champion Config V0 Engine (Image v14)** để săn timing giờ đêm.
