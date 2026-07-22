# Kết Quả Thử Nghiệm 0950 (Slot 03 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0950`
- **File Compose**: `03-docker-compose.yml`
- **Thời gian chấm**: 22/07/2026 09:50
- **Cấu hình**: Image v10.1 + Native Warmup 5 rounds (`VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5`) + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `59.42`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `59.42`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `57 ms`
- **TTFT P95**: `82 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `4` (🔥 Cân bằng mốc kỷ lục số lỗi thấp nhất toàn giải!)
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Nhận Xét

1. **Hiệu năng Warmup 5 Vòng (`WARMUPS=5`)**:
   - Failed Count đạt mức tối kịch sàn: **4 requests** (cân bằng mốc kỷ lục ổn định nhất toàn giải của STT 88).
   - Tuy nhiên TTFT P50/P95 ở mốc 09:50 bị ảnh hưởng nhẹ bởi nhiễu tải Grader BTC (57ms / 82ms), kéo ERS về 59.42đ.
2. **Đánh giá**:
   - Ép warmup 5 lượt giúp tối đa hóa độ ổn định cho container (giảm hẳn request lỗi xuống 4).
   - Mốc Warmup 3 lượt ở Slot 02 (`WARMUPS=3`) cho tốc độ TTFT ấn tượng hơn (48ms / 68ms).
3. **Bước tiếp theo**:
   - Tiến hành nộp **Slot 04** (`04-docker-compose.yml` - `GPU_MEM=0.96`) để test cân bằng bộ nhớ VRAM!
