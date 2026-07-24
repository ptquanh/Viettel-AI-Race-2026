# Kết Quả Thử Nghiệm 1607 (Slot 08 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1607`
- **File Compose**: `1607-docker-compose.yml` (Slot 08)
- **Thời gian chấm**: 24/07/2026 (16:07)
- **Thay đổi**: Best Slot 06 (`spawn`) + `WARMUPS=1` + `max_split_size_mb:128`

## Kết Quả Chấm Điểm

- **Điểm số**: `55.5300` (❌ Sụt 6.06đ so với kỷ lục 61.59đ của Slot 06)
- **TTFT P50**: 69ms (Tăng vọt +22ms từ 47ms!)
- **TTFT P95**: 96ms (Tăng vọt +28ms từ 68ms!)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Nguyên nhân giảm điểm**:
  1. `VLLM_CUDAGRAPH_NUM_OF_WARMUPS=1`: Giảm warmup xuống 1 lần khiến quá trình CUDA Graph capture bị thiếu ngữ cảnh (cold capture), khiến vLLM phải liên tục JIT re-compile hoặc fallback khi các request thực tế đến, gây tăng mạnh trễ TTFT P50 lên 69ms.
  2. `max_split_size_mb:128`: Giới hạn kích thước chia nhỏ block bộ nhớ của PyTorch Allocator tạo ra overhead phân mảnh/cấp phát nhỏ lẻ không tương thích với CUDA Graph stride buffers.
- **Kết luận**: Khẳng định **bắt buộc giữ `VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5`** và **chỉ dùng `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` đơn biến**.
