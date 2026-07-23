# Kết Quả Thử Nghiệm 0958 (Slot 03 - 23/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0958`
- **File Compose**: `0958-docker-compose.yml` (Slot 03)
- **Thời gian chấm**: 23/07/2026 09:58
- **Cấu hình**: Image v12 Mới (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v12`) + FP8 Dynamic (`VLLM_QUANTIZATION=fp8`) + `VLLM_MAX_MODEL_LEN=8192` + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32]` + Warmup 5 rounds (`VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5`) + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `58.79`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `58.79`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `58 ms`
- **TTFT P95**: `82 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu Quả Image v12 Mới**:
   - Điểm số đạt **58.79đ**, đánh dấu việc Engine v12 đã chạy ổn định và chính xác trên môi trường BTC. (Kỷ lục cũ là 61.24đ ở cấu hình Lean v7).
   - TTFT P50 (58ms) rất mượt. Accuracy drop = 0%, failed count = 5 không tăng.
2. **Hướng Đi Tiếp Theo**:
   - TPOT vẫn là 4ms, xác nhận base engine dù cập nhật phiên bản cũng không thể phá mốc này nếu chạy Vanilla Decoding.
   - Sẵn sàng kích hoạt **Speculative Decoding** trên Image v12 ở Slot 04!
