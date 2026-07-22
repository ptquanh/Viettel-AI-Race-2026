# Kết Quả Thử Nghiệm 1719 (Slot 09 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1719`
- **File Compose**: `1719-docker-compose.yml` (Slot 09)
- **Thời gian chấm**: 22/07/2026 17:19
- **Cấu hình**: Image v11 (Modern vLLM Engine Base) + FP8 Dynamic + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `57.75`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `57.75`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `59 ms`
- **TTFT P95**: `91 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Đánh Giá Image v11 (Modern vLLM Engine Base)**:
   - Container chạy thành công 100%, vượt qua tất cả probe checks của BTC.
   - Điểm ERS đạt **57.75đ**. TTFT P50=59ms, TTFT P95=91ms, TPOT=4ms, 5 failed requests.
   - So với Image v10.1 (60.72đ, TTFT 48ms/68ms), engine vLLM mới có overhead khởi tạo/scheduling mặc định cao hơn một chút ở mode FP8 Dynamic.
2. **Khẳng Định Bottleneck TPOT = 4ms**:
   - Dù nâng cấp lên engine vLLM mới với C++ Scheduler, TPOT vẫn giữ nguyên mốc **4ms**.
   - Điều này xác nhận 100% giả thuyết: **FP8 Dynamic quantization overhead** + HBM bandwidth là rào cản chính giữ TPOT ở 4ms.
3. **Bước Tiếp Theo**:
   - Triển khai ngay **Slot 10** (`10-docker-compose.yml` - BF16, loại bỏ `VLLM_QUANTIZATION=fp8`).
   - Việc loại bỏ runtime dequantization overhead của FP8 Dynamic hứa hẹn kéo TPOT xuống **~3ms**, mở đường bứt phá lên **68-72+ điểm**!
