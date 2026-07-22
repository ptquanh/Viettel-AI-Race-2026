# Kết Quả Thử Nghiệm 0933 (Slot 02 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0933`
- **File Compose**: `02-docker-compose.yml`
- **Thời gian chấm**: 22/07/2026 09:33
- **Cấu hình**: Image v10.1 (Native Python Zero-Penalty Startup Warmup) + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `60.72` (🔥 Rất gần mốc đỉnh 60.82đ ban ngày!)
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `60.72`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `48 ms`
- **TTFT P95**: **`68 ms`** (🔥 KỶ LỤC MỚI: Trễ P95 thấp nhất toàn giải từ trước tới nay!)
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Đột Phá của Image v10.1 (Native Python Warmup)**:
   - Điểm ERS tăng vọt từ 51.40đ lên **60.72đ** (tăng +9.32đ!).
   - TTFT P95 thiết lập **KỶ LỤC MỚI TOÀN GIẢI: 68ms** (vượt qua kỷ lục 69ms của Slot 06 hôm qua).
   - TTFT P50 đạt mốc cực sâu **48ms**.
2. **Khẳng định tính đúng đắn của giải pháp Native Warmup**:
   - Việc chuyển warmup vào hàm `AsyncLLMEngine.from_engine_args` trong `sitecustomize.py` đã loại bỏ hoàn toàn `socat` overhead, đồng thời thực hiện warm-up sạch sẽ 100% CUDA Graphs và FlashInfer memory pool trước khi `uvicorn` mở port 8000.
3. **Bước tiếp theo**:
   - Tiến hành nộp **Slot 03** (`03-docker-compose.yml` - Warmups=5) để test warmup 5 rounds trực tiếp trong bộ nhớ Python!
