# Kết Quả Thử Nghiệm 0852 (Slot 04 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0852`
- **File Compose**: `0852-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 08:52
- **Cấu hình**: Image v9 (CUDA Graph Dynamic Config) + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL_DECODE_ONLY` + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16]` + `VLLM_MAX_CUDAGRAPH_CAPTURE_SIZE=16` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `59.93`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `59.93`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `50 ms`
- **TTFT P95**: `74 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `6`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Image v9 + `FULL_DECODE_ONLY` + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16]`**:
   - Điểm ERS đạt **59.93đ** (TTFT P50=50ms, TTFT P95=74ms, Failed=6).
   - So với Slot 3 (`[1,2,4,8,16,32]`): Điểm giảm nhẹ 0.47đ, TTFT P50 tăng nhẹ từ 48ms lên 50ms.
2. **Đánh giá về Capture Size = 32**:
   - Việc loại bỏ batch size 32 khỏi danh sách CUDA graph capture sizes buộc các batch lớn hơn 16 phải fallback về eager mode hoặc padding không tối ưu.
   - Workload Poisson 70 conversations vẫn xuất hiện các đợt burst với batch size > 16. Do đó, việc giữ capture size 32 (như ở Slot 3) mang lại hiệu năng ổn định hơn.
3. **Bài học & Định hướng**:
   - Mốc capture sizes tốt nhất là `[1,2,4,8,16,32]` (Slot 3).
   - Tiến tới Slot 5 (`05-docker-compose.yml`): thử nghiệm `VLLM_CUDAGRAPH_MODE=FULL` (capture cả prefill và decode) để đánh giá khả năng chịu tải VRAM và hiệu năng prefill.
