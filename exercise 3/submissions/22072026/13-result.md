# Kết Quả Thử Nghiệm Slot 13 (22/07/2026)

- **Mã thử nghiệm**: `Slot 13`
- **File Compose**: `13-docker-compose.yml`
- **Cấu hình**: Image v11 Modern Engine (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32]` + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`
- **Mục đích**: Tinh chỉnh các kích thước batch CUDA Graph capture cụ thể cho phân phối nhịp Poisson nhằm giảm trễ TTFT P50 khi xử lý các batch ngẫu nhiên.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
