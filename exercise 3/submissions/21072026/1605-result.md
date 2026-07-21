# Kết Quả Thử Nghiệm 1605 (Slot 11 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1605`
- **File Compose**: `11-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 16:05
- **Cấu hình**: Image v9 + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL` + `OMP_NUM_THREADS=1` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `60.45`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `60.45`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `50 ms`
- **TTFT P95**: `77 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Micro-tune Threading (`OMP_NUM_THREADS=1`)**:
   - Điểm ERS đạt **60.45đ** (điểm cao thứ 2 ban ngày, vượt mốc 60 điểm!).
   - TTFT P50 giảm sâu về **50 ms**, TTFT P95 ấn tượng ở mức **77 ms**.
   - Failed Count đạt mức tối ưu tuyệt đối: **5 requests**.
2. **Đánh giá & Nhận xét**:
   - Việc giảm `OMP_NUM_THREADS` xuống `1` đã thành công loại bỏ tranh chấp CPU giữa OpenMP math workers và asyncio serving loop của vLLM. 2 CPU cores rảnh rỗi giúp phục vụ request I/O cực mượt.
   - Xác nhận `OMP_NUM_THREADS=1` trên `FULL` mode là ứng viên sáng giá hàng đầu cho lượt nộp Golden buổi tối!
3. **Bước tiếp theo**:
   - Chuyển sang Slot 12 (`12-docker-compose.yml`): Micro-tune VRAM `GPU_MEMORY_UTILIZATION=0.94` trên nền `FULL` mode.
