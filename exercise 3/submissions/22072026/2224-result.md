# Kết Quả Thử Nghiệm 2224 (Slot 12 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2224`
- **File Compose**: `2224-docker-compose.yml` (Slot 12)
- **Thời gian chấm**: 22/07/2026 22:24
- **Cấu hình**: Image v11 Modern Engine (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic (`VLLM_QUANTIZATION=fp8`) + **`VLLM_MAX_MODEL_LEN=8192`** + Warmup 5 rounds (`VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5`) + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `58.68` (🔥 **BỨT PHÁ TRONG ĐÊM! Tăng vọt +3.55đ so với Slot 11!**)
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `58.68`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `59 ms` (giảm 8ms so với Slot 11!)
- **TTFT P95**: **`79 ms`** (🔥 giảm 13ms P95 so với 92ms của Slot 11!)
- **TPOT Median**: `4 ms`
- **Failed Count**: `5` (giảm 1 request lỗi!)
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận Cốt Lõi

1. **Hiệu Quả Đột Phá Của Giới Hạn `VLLM_MAX_MODEL_LEN=8192` Trên Image v11 (vLLM V1 Engine)**:
   - Workload trace thực tế của BTC có Max Context Length chỉ là **4700 tokens**.
   - Khi giới hạn `VLLM_MAX_MODEL_LEN=8192` (thay vì 32768 mặc định), vLLM V1 C++ Scheduler không còn phải pre-capture các CUDA graph memory stride buckets khổng lồ cho 32K context.
   - Kết quả: TTFT P50 giảm 8ms (67ms -> 59ms), TTFT P95 giảm 13ms (92ms -> 79ms), kéo điểm ERS tăng vọt **+3.55đ từ 55.13đ lên 58.68đ**!
2. **So Sánh Tương Quan Với vLLM v0.22.1 Cũ**:
   - Ở vLLM v0.22.1 cũ, MaxLen=8K từng làm suy giảm nhẹ điểm do bug PyTorch Dynamo JIT allocation.
   - Tuy nhiên trên **Image v11 (vLLM V1 engine mới)**, `VLLM_MAX_MODEL_LEN=8192` hoạt động hoàn hảo và là một **đòn bẩy tối ưu hóa then chốt**!
