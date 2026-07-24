# Kết Quả Thử Nghiệm 0925 (Slot 02 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0925`
- **File Compose**: `03-docker-compose.yml` (Slot 02 theo plan mới)
- **Thời gian chấm**: 24/07/2026 (09:25)
- **Thay đổi**: Image v14 + FP8 + FlashInfer + BlockSize 32 + MaxLen 8K + OMP=1 (Merge Best Config)

## Kết Quả Chấm Điểm

- **Điểm số**: `59.9900` (Suýt soát mốc 60đ ban ngày!)
- **TTFT P50**: 54ms (Giảm 5ms so với mốc 59ms của Slot 11 hôm qua!)
- **TTFT P95**: 75ms (Giảm 4ms so với mốc 79ms!)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 4 (Mốc kỷ lục ít lỗi nhất!)
- **Penalty**: 1
- **Accuracy Drop**: 0% (Chính xác tuyệt đối 100%)

## Phân Tích & Kết Luận

- **Hiệu quả của Merge Best Config**: Kết hợp Fused Kernel `v14` với bộ cờ CLI chuẩn từ mốc 61.24đ (FlashInfer + BlockSize 32 + OMP=1) đã cải thiện rõ rệt TTFT P50 (từ 59ms -> 54ms) và trễ đuôi P95 (từ 79ms -> 75ms).
- **Độ ổn định tuyệt đối**: Số lượng request thất bại giảm xuống còn 4/420, khẳng định container vô cùng vững chắc.
- **Kết luận**: Khóa cấu hình này làm Baseline chính thức cho ngày 24/07. Chuyển sang Slot 03 (Thử nghiệm `VLLM_COMPILATION_LEVEL=2`).
