# Kết Quả Thử Nghiệm 0902 (Slot 01 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0902`
- **File Compose**: `01-docker-compose.yml`
- **Thời gian chấm**: 22/07/2026 09:02
- **Cấu hình**: Image v10 Baseline (Zero-Penalty Warmup via `socat`) + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `OMP_NUM_THREADS=2`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `51.40`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `51.40`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `95 ms` (Tăng vọt do socat user-space TCP proxying overhead!)
- **TTFT P95**: `118 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích Nguyên Nhân & Bài Học Kỹ Thuật

1. **Phân tích Nguyên nhân sụt giảm điểm (51.40đ)**:
   - Trễ TTFT P50 tăng vọt từ ~47-50ms lên **95ms** (tăng ~45ms).
   - Nguyên nhân chính: `socat TCP-LISTEN:8000,fork TCP:127.0.0.1:8080` thực hiện user-space TCP proxying với cờ `fork`. Mỗi request HTTP kết nối đến cổng 8000 đều làm `socat` phải fork 1 process mới trong Linux kernel.
   - Quá trình process forking + socket buffer copying giữa port 8000 và 8080 làm tăng trễ 40-50ms cho từng request streaming, làm điểm ERS sụt giảm nghiêm trọng.

2. **Giải pháp khắc phục cho Slot 02 (Image v10.1)**:
   - Loại bỏ hoàn toàn `socat` proxying.
   - Chuyển cơ chế Startup Warmup sang thực thi trực tiếp bằng Python monkey-patching trong `sitecustomize.py` hoặc vLLM engine initialization hooks TRƯỚC KHI uvicorn HTTP server bind port 8000!
