# Kết Quả Thử Nghiệm 2344 (Slot 14 - 20/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2344`
- **File Compose**: `2344-docker-compose.yml`
- **Thời gian chấm**: 20/07/2026 23:44
- **Cấu hình**: FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.96` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + Image v7 Lean (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `60.46`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `60.46`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `51 ms`
- **TTFT P95**: `74 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **GPU Memory Utilization 0.96 so với 0.95 (Slot 13 - 61.24đ)**:
   - Đẩy VRAM util lên 0.96 làm tăng nhẹ TTFT P50 từ 44ms (Slot 13) lên 51ms.
   - Nguyên nhân: Cấp phát thêm VRAM cho KV cache làm tăng nhẹ overhead khởi tạo PyTorch / CUDA graph allocator memory management.
2. **Khẳng định VRAM Utilization 0.95 là sweet-spot tối ưu**: Mốc 0.95 cho hiệu năng cao nhất trên hạ tầng MiG H200 18GB VRAM của BTC.
