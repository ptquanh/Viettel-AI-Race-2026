# Kết quả Benchmark - 22:55 10/07/2026 (STT 75 - TurboQuant 3-bit Key / 4-bit Value Hybrid KV Cache 🔥)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v4` + `--kv-cache-dtype turboquant_k3v4_nc` + `--quantization fp8`
- **Mục đích**: Chạy thử nghiệm cờ nén cực cao của TurboQuant (`turboquant_k3v4_nc`) sử dụng 3-bit cho Key và 4-bit cho Value kèm Norm Correction. Nhắm tới TPOT tối thiểu (~15ms) thông qua việc cắt giảm tối đa băng thông KV cache đọc từ HBM GPU.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
