# Kết quả Benchmark - 07:53 11/07/2026 (STT 84 - Engine V0 + TurboQuant 4-bit KV Cache + FP8 weights 🔥)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v4` + `VLLM_USE_V1=0` + `turboquant_4bit_nc` + FP8 weights
- **Mục đích**: Ép vLLM dùng engine V0 bằng biến môi trường `VLLM_USE_V1=0` nhằm bypass lỗi crash khởi động của V1 engine đối với cờ nén KV `turboquant_4bit_nc`.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
