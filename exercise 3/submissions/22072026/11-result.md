# Kết Quả Thử Nghiệm Slot 11 (22/07/2026)

- **Mã thử nghiệm**: `Slot 11`
- **File Compose**: `11-docker-compose.yml`
- **Cấu hình**: Image v11 Modern Engine Base (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v11`) + FP8 Dynamic (`VLLM_QUANTIZATION=fp8`) + Warmup 5 rounds (`VLLM_CUDAGRAPH_NUM_OF_WARMUPS=5`) + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`
- **Mục đích**: Tái lập FP8 Dynamic trên nền **Image v11 Modern Engine** (vLLM v0.25+) sau khi xác nhận BF16 thất bại ở Slot 10. Tối ưu hoá 5 vòng Warmup JIT để hạ số request lỗi xuống kịch sàn và nâng điểm ERS trên engine mới.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
