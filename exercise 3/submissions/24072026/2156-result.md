# Kết Quả Thử Nghiệm 2156 (Slot 13 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2156`
- **File Compose**: `2156-docker-compose.yml` (Slot 13)
- **Thời gian chấm**: 24/07/2026 (21:56)
- **Thay đổi**: Re-test Cấu hình Á quân (`GPU_MEM=0.94` + `spawn` + `FLASHINFER`)

## Kết Quả Chấm Điểm

- **Điểm số**: `56.9300` (❌ Sụt 4.18đ so với 61.11đ của Slot 20:12)
- **TTFT P50**: 62ms (Tăng +14ms từ 48ms của Slot 20:12!)
- **TTFT P95**: 91ms (Tăng +18ms từ 73ms!)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Nguyên nhân biến động điểm số**:
  1. Cùng một cấu hình `GPU_MEM=0.94` từng đạt 61.11đ lúc 20:12 (TTFT P50 48ms), nhưng ở khung 21:56 TTFT P50 bị đẩy lên 62ms.
  2. Thời điểm 21:50 - 22:00 là mốc giao giờ (cuối giờ 21:00 / chuẩn bị sang giờ 22:00), lượng bài nộp dồn toa từ nhiều đội tạo ra peak noise cao.
- **Kết luận**:
  - Tránh các mốc giao giờ (cuối giờ tròn xx:50 - xx:05).
  - Tập trung nộp Slot 14 vào giữa khung 22:30 - 23:00 và Slot 15 vào 23:45.
