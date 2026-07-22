# Kết Quả Thử Nghiệm Slot 12 (22/07/2026)

- **Mã thử nghiệm**: `Slot 12`
- **File Compose**: `12-docker-compose.yml`
- **Cấu hình**: Image v11 Modern Engine (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic + `VLLM_MAX_MODEL_LEN=8192` + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`
- **Mục đích**: Giới hạn Max Model Len về 8192 (khớp với workload trace max 4700 tokens) để thu hẹp CUDA Graph memory strides và tăng tốc độ warmup JIT trên engine vLLM V1.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
