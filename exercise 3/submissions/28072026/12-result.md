# Kết quả Benchmark - Slot 12 (Image v20.0 CUTLASS FP8 + FULL_DECODE_ONLY CUDA Graph)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Chuyển sang `VLLM_CUDAGRAPH_MODE=FULL_DECODE_ONLY` để giải phóng memory allocated cho prefill CUDA Graphs).
- **Mục đích**: Tối ưu hóa dung lượng VRAM thực sự cho prefill phase của các request context dài.

## Kết quả thử nghiệm Slot 12

**Trạng thái**: Đang chờ nộp & chấm điểm...
