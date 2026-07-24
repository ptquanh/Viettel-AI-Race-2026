# Kết Quả Thử Nghiệm 1200 (Slot 05 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1200`
- **File Compose**: `1200-docker-compose.yml` (Slot 05)
- **Thời gian chấm**: 24/07/2026 (12:00)
- **Thay đổi**: Best v14 + Expandable Segments + thêm Capture Size 24: `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,24,32]`

## Kết Quả Chấm Điểm

- **Điểm số**: `60.0200` (Giảm -0.85đ so với Slot 04 60.87đ)
- **TTFT P50**: 54ms (Tăng 3ms từ 51ms)
- **TTFT P95**: 76ms (Tăng 6ms từ 70ms)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 6 (Tăng 1 lỗi)
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Capture Size 24 Kém Tối Ưu**: Thêm mốc size 24 làm tăng số lượng CUDA Graph buckets cần quản lý và warmup, dẫn đến overhead phân nhánh nhỏ khi dispatch graph kernel.
- TTFT P50 tăng từ 51ms lên 54ms và TTFT P95 tăng từ 70ms lên 76ms.
- **Kết luận**: Khẳng định bộ `CAPTURE_SIZES=[1,2,4,8,16,32]` (bội số của 2) là tối ưu nhất. Khôi phục về bộ cũ cho các slot tiếp theo.
