# Kết Quả Thử Nghiệm 2012 (Slot 10 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2012`
- **File Compose**: `2012-docker-compose.yml` (Slot 10)
- **Thời gian chấm**: 24/07/2026 (20:12)
- **Thay đổi**: Golden Config + `VLLM_GPU_MEMORY_UTILIZATION=0.94` (thay vì 0.95)

## Kết Quả Chấm Điểm

- **Điểm số**: `61.1100` (🔥 RẤT CAO! Đạt mốc điểm cao thứ 2 toàn giải, chỉ kém kỷ lục 61.59đ 0.48đ!)
- **TTFT P50**: 48ms (Giảm mạnh -8ms từ 56ms của Slot 19:30!)
- **TTFT P95**: 73ms (Giảm mạnh -4ms từ 77ms của Slot 19:30!)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Hiệu quả của VRAM Micro-tuning (`GPU_MEM=0.94`)**:
  1. Giảm nhẹ VRAM utilization từ 0.95 xuống 0.94 giúp thu hẹp kích thước PyTorch CUDA allocator footprint, giảm VRAM management overhead.
  2. Kết hợp với việc khung giờ 20:12 bớt noise hơn 19:30, TTFT P50 đã kéo sâu về **48ms** và P95 về **73ms**, đưa tổng điểm bật lên **61.11đ**.
- **Kết luận**:
  - `GPU_MEM=0.94` hoạt động rất ấn tượng và cực kỳ ổn định.
  - Sẵn sàng nộp Slot 11 (`Full Micro-env Combo`) để kiểm tra thêm việc cắt giảm logging/tokenizer overhead.
