# Kết Quả Thử Nghiệm 0046 (Slot 01 - 25/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0046`
- **File Compose**: `0046-docker-compose.yml` (Slot 01 ngày 25/07)
- **Thời gian chấm**: 25/07/2026 (00:46)
- **Thay đổi**: Golden Config (`GPU_MEM=0.94` + `spawn` + `FLASHINFER`) chuyển sang ngày mới 25/07

## Kết Quả Chấm Điểm

- **Điểm số**: `59.6600` (Khởi đầu ổn định cho ngày mới 25/07)
- **TTFT P50**: 55ms
- **TTFT P95**: 73ms (P95 cực kỳ ấn tượng)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Khởi đầu ngày 25/07**:
  1. Đợt nộp lúc 00:46 đạt 59.66đ với TTFT P95 chỉ 73ms và 5 request lỗi.
  2. Baseline FP8 trên Image v14 đã rất ổn định ở mức ~60đ.
- **Định hướng tiếp theo**: Tập trung triển khai **Image v15 (Online INT4 Quantization)** để phá vỡ giới hạn TPOT 4ms lên 3ms và đạt mục tiêu 70+ điểm.
