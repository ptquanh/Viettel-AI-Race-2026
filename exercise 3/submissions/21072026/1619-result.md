# Kết Quả Thử Nghiệm 1619 (Slot 12 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1619`
- **File Compose**: `12-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 16:19
- **Cấu hình**: Image v9 + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.94` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL` + `OMP_NUM_THREADS=2` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `60.37`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `60.37`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `48 ms`
- **TTFT P95**: `76 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Micro-tune VRAM (`GPU_MEMORY_UTILIZATION=0.94`)**:
   - Điểm ERS đạt **60.37đ** (tiếp tục vượt mốc 60đ ban ngày!).
   - TTFT P50 giảm sâu về **48 ms**, TTFT P95 kịch sàn ở mức **76 ms**.
   - Failed Count: **7 requests**.
2. **Đánh giá & Nhận xét**:
   - Giảm `GPU_MEMORY_UTILIZATION` từ 0.95 xuống 0.94 giúp giảm nhẹ trễ TTFT P50 (từ 50ms xuống 48ms) do giảm overhead quản lý bộ nhớ VRAM manager.
   - Tuy nhiên, việc giảm dung lượng VRAM làm hẹp KV Cache pool nhẹ, khiến số request bị drop/fail tăng từ 5 lên 7 requests dưới tải Poisson.
   - Khẳng định: `GPU_MEM=0.95` vẫn duy trì sự cân bằng tối ưu nhất giữa TTFT và Failed count (chỉ 5 failed requests).
3. **Bước tiếp theo**:
   - Chuyển sang Slot 13 (`13-docker-compose.yml`): Micro-tune VRAM `GPU_MEMORY_UTILIZATION=0.96` để đánh giá chiều ngược lại.
