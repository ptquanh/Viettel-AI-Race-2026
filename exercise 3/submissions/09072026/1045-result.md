# Kết quả Benchmark - 10:45 09/07/2026 (STT 57 - Modern vLLM v0.22.1 Hijack + VRAM 0.92 & DEBUG logs Patch)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack` + các tham số tối ưu hóa (max-model-len=43008, memory=0.92, quantization=fp8, debug-enabled).
- **Mục đích**: Bản vá giảm VRAM utilization xuống mức an toàn tuyệt đối 0.92, gỡ bỏ cấu hình giới hạn CUDA Graph capture thủ công, và bật DEBUG logs để chẩn đoán chính xác exception nếu tiếp tục crash.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
