# Kết Quả Thử Nghiệm 2216 (Slot 14 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2216`
- **File Compose**: `2216-docker-compose.yml` (Slot 14)
- **Thời gian chấm**: 24/07/2026 (22:16)
- **Thay đổi**: Re-test Cấu hình Kỷ lục (`GPU_MEM=0.95` + `spawn` + `FLASHINFER`)

## Kết Quả Chấm Điểm

- **Điểm số**: `56.7800`
- **TTFT P50**: 63ms (Tăng +11ms từ 52ms của Slot 21:08)
- **TTFT P95**: 85ms
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 7
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Tải hệ thống vào đêm 24/07**: Mặc dù chạy lúc 22:16, lượng nộp dồn toa từ nhiều đội trên hệ thống BTC làm tăng trễ hàng đợi, khiến TTFT P50 vọt lên 63ms và làm số request lỗi tăng nhẹ lên 7.
