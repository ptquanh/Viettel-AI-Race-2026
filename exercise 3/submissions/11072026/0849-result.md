# Kết quả Benchmark - 08:49 11/07/2026 (STT 79 - Prefix Warmup (Turn-1) + FP8 + gpu-mem=0.97 (hijack-v5) 🔥)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v5` + `--quantization fp8` + `--max-num-seqs 256` + Warmup prefix enable + `--gpu-memory-utilization 0.97`
- **Mục đích**: Tương tự STT 78 nhưng tăng gpu-memory-utilization lên 0.97 để mở rộng giới hạn KV cache pool, đề phòng prefix cache bị evict sớm.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
