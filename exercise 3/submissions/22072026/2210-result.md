# Kết Quả Thử Nghiệm 2210 (Slot 11 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2210`
- **File Compose**: `2210-docker-compose.yml` (Slot 11)
- **Thời gian chấm**: 22/07/2026 22:10
- **Cấu hình**: Image v11 Modern Engine (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic (`VLLM_QUANTIZATION=fp8`) + Warmup 5 rounds (`VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5`) + `OMP_NUM_THREADS=1` + `VLLM_MAX_MODEL_LEN=32768` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `55.13`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `55.13`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `67 ms`
- **TTFT P95**: `92 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `6`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Phục Hồi Kỷ Khương FP8 Dynamic**:
   - Sau thất bại ở Slot 10 (BF16 TPOT 6ms), việc khôi phục `VLLM_QUANTIZATION=fp8` đã kéo TPOT ngay lập tức trở lại mốc **4ms**.
   - Điểm ERS tăng từ 46.83đ lên **55.13đ** (+8.30đ).
2. **Nhận Xét Về Max Model Len 32K**:
   - Ở mốc `VLLM_MAX_MODEL_LEN=32768`, vLLM V1 engine phải pre-capture các CUDA graph stride buckets rất lớn cho 32K context, đẩy TTFT P50 lên 67ms và P95 lên 92ms.
