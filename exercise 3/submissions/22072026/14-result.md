# Kết Quả Thử Nghiệm Slot 14 (22/07/2026)

- **Mã thử nghiệm**: `Slot 14`
- **File Compose**: `14-docker-compose.yml`
- **Cấu hình**: Image v11 Modern Engine (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic + `VLLM_MAX_NUM_SEQS=48` + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`
- **Mục đích**: Tăng giới hạn request đồng thời lên 48 để giảm trễ hàng đợi scheduler trong các thời điểm lượng request đến dồn dập (Poisson burst).

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
