# Kết quả Benchmark - Slot 09 (Image v20.0 CUTLASS FP8 + GPU_MEM=0.94 Sweet-Spot Tuning)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Tinh chỉnh `VLLM_GPU_MEMORY_UTILIZATION=0.94` nhằm giảm overhead quản lý VRAM block allocator, kết hợp CUDA Graph Capture `[1..48]`).
- **Mục đích**: Ép trễ TTFT P95 từ 74ms xuống mốc ~61ms (tương tự slot kỷ lục 62.67đ của ngày 25/07), hướng tới phá mốc 61-63+ ERS trong ngày 28/07.

## Kết quả thử nghiệm Slot 09

**Trạng thái**: Đang chờ nộp & chấm điểm...
