# Kết Quả Thử Nghiệm 2236 (Slot 13 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2236`
- **File Compose**: `2236-docker-compose.yml` (Slot 13)
- **Thời gian chấm**: 22/07/2026 22:36
- **Cấu hình**: Image v11 Modern Engine (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic (`VLLM_QUANTIZATION=fp8`) + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32]` + Warmup 5 rounds (`VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5`) + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `57.62`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `57.62`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `61 ms`
- **TTFT P95**: `89 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu Quả CUDA Graph Capture Sizes [1..32]**:
   - Điểm ERS đạt **57.62đ** (tốt hơn mốc 55.13đ của Slot 11 với default capture sizes).
   - Tuy nhiên, so với Slot 12 (MaxLen=8192, 58.68đ), việc giới hạn capture sizes đơn thuần chưa tối ưu triệt để bằng việc cắt giảm `MAX_MODEL_LEN` trực tiếp trên vLLM V1 scheduler.
2. **Hướng Đi Tốt Nhất**:
   - Kết hợp **`VLLM_MAX_MODEL_LEN=8192` + Capture Sizes micro-tuning** ở các slot tiếp theo!
