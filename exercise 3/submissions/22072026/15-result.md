# Kết Quả Thử Nghiệm Slot 15 (22/07/2026)

- **Mã thử nghiệm**: `Slot 15`
- **File Compose**: `15-docker-compose.yml`
- **Cấu hình**: Image v11 Golden Run (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`
- **Mục đích**: Chạy Golden Run chốt sổ ngày 22/07 vào khung giờ vàng đêm muộn (22:30 - 23:59) khi nhiễu host BTC ở mức cực thấp để săn điểm kỷ lục mới.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
