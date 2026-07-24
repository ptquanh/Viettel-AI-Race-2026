# Kết Quả Thử Nghiệm 2108 (Slot 12 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2108`
- **File Compose**: `2108-docker-compose.yml` (Slot 12)
- **Thời gian chấm**: 24/07/2026 (21:08)
- **Thay đổi**: Golden Config baseline re-test (`GPU_MEM=0.95` + `spawn` + `FLASHINFER`)

## Kết Quả Chấm Điểm

- **Điểm số**: `59.7400` (Cải thiện +1.17đ so với 58.57đ của Slot 20:23)
- **TTFT P50**: 52ms (Giảm 7ms từ 59ms của Slot 20:23)
- **TTFT P95**: 82ms
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Diễn biến theo thời gian**:
  1. Loại bỏ `MALLOC_TRIM_THRESHOLD_=0` giúp TTFT P50 ngay lập tức kéo giảm 7ms (từ 59ms về 52ms), điểm phục hồi từ 58.57đ lên **59.74đ**.
  2. Khung giờ 21:00 - 21:15 thường có đợt nộp bài tập trung của các đội khác (đầu giờ tròn), tạo ra nhiễu nhẹ.
- **Kết luận**:
  - Tiếp tục chuẩn bị cho các đợt Golden Run đêm khuya (22:00 - 23:45) khi lượng nộp của hệ thống đạt mức thấp nhất.
