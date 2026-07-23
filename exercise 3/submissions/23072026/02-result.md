# Kết Quả Thử Nghiệm Slot 02 (23/07/2026)

- **Mã thử nghiệm**: `Slot 02`
- **File Compose**: `02-docker-compose.yml`
- **Cấu hình**: Image v11 Golden Run Combo (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic + `VLLM_MAX_MODEL_LEN=8192` + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32]` + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`
- **Mục đích**: **GOLDEN RUN CHỐT SỔ ĐỢT CHẠY V2**: Áp dụng toàn bộ phát hiện đột phá (MaxLen=8K + Capture Sizes [1..32] + Warmup 5) trên Image v11 để đạt đỉnh điểm ERS.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
