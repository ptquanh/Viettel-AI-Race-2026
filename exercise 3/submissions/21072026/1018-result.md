# Kết Quả Thử Nghiệm 1018 (Slot 06 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1018`
- **File Compose**: `1018-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 10:18
- **Cấu hình**: Image v9 (CUDA Graph Dynamic Config) + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL` + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32]` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `58.86`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `58.86`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `60 ms`
- **TTFT P95**: `84 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Slot 06 (`1018`)**:
   - Điểm ERS đạt **58.86đ**.
   - TTFT P50 đạt **60 ms**, TTFT P95 đạt **84 ms**.
   - Failed Count duy trì **5 requests**.
2. **Đánh giá & Nguyên nhân**:
   - Mặc dù cấu hình kết hợp `FULL` mode + `capture_sizes=[1,2,4,8,16,32]`, nhưng kết quả bị ảnh hưởng do trễ TTFT tăng lên (từ 47ms ở Slot 05 lên 60ms).
   - Nguyên nhân chủ yếu do biến động tải (grader noise / host traffic) vào thời điểm 10:18 sáng (giờ cao điểm nhiều đội nộp).
3. **Bước tiếp theo**:
   - Chuyển sang thử nghiệm Slot 07 (`VLLM_CUDAGRAPH_NUM_OF_WARMUPS=3`) để đánh giá tác động của multi-warmup CUDA graph capture.
