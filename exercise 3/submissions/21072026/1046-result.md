# Kết Quả Thử Nghiệm 1046 (Slot 07 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1046`
- **File Compose**: `07-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 10:46
- **Cấu hình**: Image v9 + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_NUM_OF_WARMUPS=3` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `59.00`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `59.00`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `55 ms`
- **TTFT P95**: `90 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Multi-Warmup (`NUM_OF_WARMUPS=3`)**:
   - Điểm ERS đạt **59.00đ**.
   - TTFT P50 đạt **55 ms**, TTFT P95 ở mức **90 ms**.
   - Failed Count tăng nhẹ lên **7 requests**.
2. **Đánh giá & Nhận xét**:
   - Tăng số lần warmup CUDA graph (`warmups=3`) trên mode mặc định chưa mang lại hiệu quả rõ rệt khi nộp ban ngày (TTFT P50 55ms so với 47-48ms của Slot 03/05).
   - Sự kết hợp giữa `warmups=3` và `cudagraph_mode` mới (sẽ thử ở COMBO A - Slot 09) hứa hẹn cho kết quả tốt hơn.
3. **Bước tiếp theo**:
   - Tiến hành thử nghiệm Slot 08 (`08-docker-compose.yml`): `VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5` để đánh giá mốc deep warmup.
