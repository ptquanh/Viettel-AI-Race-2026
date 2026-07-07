# Kết quả Benchmark - Slot 7 07/07/2026 (compilation-config Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--compilation-config='{"cudagraph_mode":"FULL","max_cudagraph_capture_size":256}'` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Ép vLLM thế hệ mới (v1 engine) sử dụng chế độ FULL CUDA graph cho decode với kích thước capture tối đa là 256 (lớn hơn output size 200 tokens của benchmark), giúp giảm thiểu tối đa overhead kernel launch trên CPU.

## Chỉ số đo được

TBD

---
