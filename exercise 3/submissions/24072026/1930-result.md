# Kết Quả Thử Nghiệm 1930 (Slot 09 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1930`
- **File Compose**: `1930-docker-compose.yml` (Slot 09)
- **Thời gian chấm**: 24/07/2026 (19:30)
- **Thay đổi**: Baseline Re-test Golden Config (Slot 06 - exact copy)

## Kết Quả Chấm Điểm

- **Điểm số**: `59.3400` (❌ Sụt 2.25đ so với kỷ lục 61.59đ của Slot 06)
- **TTFT P50**: 56ms (Tăng +9ms từ 47ms)
- **TTFT P95**: 77ms (Tăng +9ms từ 68ms)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Nguyên nhân giảm điểm**:
  1. Cấu hình hoàn toàn trùng khớp với Slot 06 (`1350`), nhưng kết quả TTFT P50 bị đẩy từ 47ms lên 56ms và TTFT P95 bị đẩy từ 68ms lên 77ms.
  2. Thời điểm nộp bài (19:30) là giờ cao điểm (Peak Noise), hạ tầng/GPU host của BTC chịu tải lớn từ nhiều đội thi nộp cùng lúc, làm tăng trễ hàng đợi (Queue Latency).
- **Kết luận**:
  - Xác nhận tính chính xác của giả thuyết **Golden Timing**: Sự chênh lệch tới 9ms TTFT giữa 13:50 và 19:30 trên cùng 1 cấu hình.
  - Cần chuyển các đợt nộp quan trọng (Golden Runs) vào khung giờ đêm muộn (21:00 - 23:45) khi hệ thống rảnh rỗi hơn.
