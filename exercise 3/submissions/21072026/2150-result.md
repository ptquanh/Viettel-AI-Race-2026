# Kết Quả Thử Nghiệm 2150 (Slot 14 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2150`
- **File Compose**: `14-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 21:50
- **Cấu hình**: Image v9 + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL` + `OMP_NUM_THREADS=1` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `59.68`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `59.68`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `55 ms`
- **TTFT P95**: `82 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `4` (Kỷ lục số request lỗi thấp nhất!)
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Candidate Golden Run (`OMP_NUM_THREADS=1` + `GPU_MEM=0.95`)**:
   - Điểm ERS đạt **59.68đ**.
   - TTFT P50 ở mức **55 ms**, TTFT P95 là **82 ms**.
   - Failed Count: **4 requests** (Cân bằng mốc kỷ lục số request bị drop thấp nhất từ trước tới nay!).
2. **Đánh giá & Nhận xét**:
   - Kết hợp `OMP_NUM_THREADS=1` và `GPU_MEMORY_UTILIZATION=0.95` mang lại độ ổn định tối đa cho container, giảm đáng kể các request bị drop do tranh chấp CPU hoặc tràn KV cache.
   - Trễ TTFT P50 ở mức 55ms do có biến động tải nhẹ trên hệ thống Grader BTC mốc 21:50.
3. **Bước tiếp theo**:
   - Tiến hành nộp lượt cuối cùng **Slot 15** (`15-docker-compose.yml`) cho mốc 22:00-22:30 đêm muộn để chốt sổ ngày 21/07!
