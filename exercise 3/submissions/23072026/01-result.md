# Kết Quả Thử Nghiệm Slot 01 (23/07/2026)

- **Mã thử nghiệm**: `Slot 01`
- **File Compose**: `01-docker-compose.yml`
- **Cấu hình**: Image v11 Modern Engine (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic + **`VLLM_MAX_MODEL_LEN=8192`** + **`VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32]`** + Warmup 5 rounds (`VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5`) + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`
- **Mục đích**: **KẾT HỢP DÙNG COMBO 2 ĐÒN BẨY ĐỘT PHÁ TỐT NHẤT**: Giới hạn MaxLen=8K (từ Slot 12: 58.68đ) + Tinh chỉnh CUDA Graph Capture Sizes [1..32] (từ Slot 13: 57.62đ) để ép TTFT P95 xuống dưới 75ms và chinh phục mốc 60+ điểm trên Image v11!

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
