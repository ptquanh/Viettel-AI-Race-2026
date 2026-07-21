# Kết Quả Thử Nghiệm 1507 (Slot 09 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1507`
- **File Compose**: `09-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 15:07
- **Cấu hình**: Image v9 + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL` + `OMP_NUM_THREADS=3` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `59.23`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `59.23`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `54 ms`
- **TTFT P95**: `83 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng FULL Mode + CPU OpenMP Threads (`OMP_NUM_THREADS=3`)**:
   - Điểm ERS đạt **59.23đ** (tăng 0.93đ so với Slot 08 58.30đ).
   - TTFT P50 giảm từ 60ms xuống **54 ms**, TTFT P95 ở mức **83 ms**.
   - Failed Count: **7 requests**.
2. **Đánh giá & Nhận xét**:
   - `OMP_NUM_THREADS=3` (tối đa hóa 3 CPU cores của container) giúp TTFT P50 cải thiện 6ms so với `OMP_NUM_THREADS=2` lúc 14:34 (Slot 08).
   - Tuy nhiên, `OMP_NUM_THREADS=2` ở Slot 05 vẫn cho kết quả tốt hơn (47ms), nguyên nhân là `OMP_NUM_THREADS=3` có thể làm tăng tranh chấp CPU giữa các thread OpenMP toán học và asyncio serving loop của vLLM dưới tải lớn, dẫn đến Failed Count bị tăng lên 7 requests.
3. **Bước tiếp theo**:
   - Chuyển sang Slot 10 (`10-docker-compose.yml`): Golden v9 Combo (Re-run `FULL` mode của Slot 05) để xác định baseline chuẩn cho buổi tối.
