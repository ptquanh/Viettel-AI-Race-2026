# Kết quả Benchmark - 21:23 09/07/2026 (STT 60 - Modern vLLM v0.22.1 Hijack + 0.96 Memory & Muted Logging)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack` + các tham số tối ưu hóa (max-model-len=262144, memory=0.96, quantization=fp8).
- **Mục đích**: 
  1. Giảm thiểu tối đa logging overhead của Docker (đặt `VLLM_LOGGING_LEVEL=WARNING` để triệt tiêu toàn bộ CPU/IO ghi log đĩa).
  2. Nâng bộ nhớ sử dụng GPU lên `0.96` nhằm mở rộng tối đa dung lượng KV Cache Radix pool để đạt cache-hit rate tốt hơn trên context dài.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
