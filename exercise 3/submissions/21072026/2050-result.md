# Kết Quả Thử Nghiệm 2050 (Slot 13 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2050`
- **File Compose**: `13-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 20:50
- **Cấu hình**: Image v9 + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.96` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL` + `OMP_NUM_THREADS=2` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `59.45`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `59.45`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `52 ms`
- **TTFT P95**: `82 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Micro-tune VRAM (`GPU_MEMORY_UTILIZATION=0.96`)**:
   - Điểm ERS đạt **59.45đ**.
   - TTFT P50 ở mức **52 ms**, TTFT P95 là **82 ms**.
   - Failed Count: **7 requests**.
2. **Đánh giá & Nhận xét**:
   - Tăng `GPU_MEMORY_UTILIZATION` từ 0.95 lên 0.96 làm tăng nhẹ overhead quản lý VRAM của PyTorch/vLLM manager (TTFT P50 tăng 5ms so với Slot 06/05 47ms).
   - Tổng hợp kết quả micro-tune VRAM ngày 21/07:
     - `GPU_MEM=0.94`: 60.37đ (P50 48ms, Fail 7)
     - `GPU_MEM=0.95`: **60.82đ** (P50 47ms, Fail 5 - **BEST BALANCED**)
     - `GPU_MEM=0.96`: 59.45đ (P50 52ms, Fail 7)
   - Khẳng định mốc **`GPU_MEMORY_UTILIZATION=0.95`** cùng **`OMP_NUM_THREADS=1`** (hoặc `OMP=2`) là tổ hợp tối ưu nhất toàn diện.
3. **Bước tiếp theo**:
   - Tiến hành lượt nộp **Slot 14 / Slot 15** cho khung giờ vàng tối muộn (sau 21:00) với Golden Combo: `FULL` mode + `GPU_MEM=0.95` + `OMP_NUM_THREADS=1` để chinh phục kỷ lục mới.
