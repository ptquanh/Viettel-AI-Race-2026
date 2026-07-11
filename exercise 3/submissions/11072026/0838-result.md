# Kết quả Benchmark - 08:38 11/07/2026 (STT 78 - Prefix Warmup (Turn-1) + FP8 weights (hijack-v5) 🔥)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v5` + `--quantization fp8` + `--max-num-seqs 256` + Warmup prefix enable.
- **Mục đích**: Kích hoạt Prefix Cache Warmup via hijack v5. Warmup toàn bộ 20 requests của turn 1. TTFT có thể giảm sâu từ 600ms xuống 50ms cho batch 1. Khả năng tăng đột biến số request qua SLO.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
