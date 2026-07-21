# Kết Quả Thử Nghiệm 1434 (Slot 08 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1434`
- **File Compose**: `08-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 14:34
- **Cấu hình**: Image v9 + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL` + `VLLM_CUDAGRAPH_NUM_OF_WARMUPS=3` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `58.30`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `58.30`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `60 ms`
- **TTFT P95**: `86 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng FULL Mode + Multi-Warmup (`warmups=3`)**:
   - Điểm ERS đạt **58.30đ**.
   - TTFT P50 đạt **60 ms**, TTFT P95 ở mức **86 ms**.
   - Failed Count duy trì mức tối ưu ban ngày: **5 requests**.
2. **Đánh giá & Nhận xét**:
   - Kết hợp `FULL` mode với `warmups=3` khiến TTFT P50 tăng từ 47ms (Slot 05 - warmup=1) lên 60ms.
   - Nguyên nhân: Việc tăng số lần warmup CUDA Graph kéo dài thời gian khởi tạo/warmup của vLLM trong container, khiến một số request đầu tiên bị dồn nén hoặc nghẽn hàng đợi ban đầu, cộng với biến động tải grader buổi chiều (14:34).
3. **Bước tiếp theo**:
   - Chuyển sang thử nghiệm Slot 09 (`09-docker-compose.yml`): `VLLM_CUDAGRAPH_MODE=FULL` + `VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5` để đánh giá mốc deep warmup.
