# Kết Quả Thử Nghiệm 1107 (Slot 04 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1107`
- **File Compose**: `1107-docker-compose.yml` (Slot 04)
- **Thời gian chấm**: 24/07/2026 (11:07)
- **Thay đổi**: Baseline v14 FP8 + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`

## Kết Quả Chấm Điểm

- **Điểm số**: `60.8700` (🔥 Đột phá mạnh mẽ +0.88đ so với Baseline 59.99đ ban ngày!)
- **TTFT P50**: 51ms (Giảm 3ms từ 54ms!)
- **TTFT P95**: 70ms (Giảm 5ms từ 75ms! - Tiệm cận kỷ lục 68ms)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Hiệu quả của Expandable Segments**: `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` giúp PyTorch Memory Allocator hạn chế tối đa tình trạng vỡ mảnh (memory fragmentation) khi cấp phát các dynamic activation tensors trùng lặp với CUDA Graph buffers.
- Nhờ đó, TTFT P50 giảm sâu xuống **51ms** và TTFT P95 giảm xuống kịch sàn **70ms**, đưa tổng điểm đạt **60.87đ** (Mốc điểm cao nhất ban ngày ngày 24/07!).
- **Kết luận**: Giữ nguyên `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` làm chuẩn cho tất cả các thử nghiệm tiếp theo.
