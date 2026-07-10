# Kết quả Benchmark - 17:00 10/07/2026 (STT 70 - INT4 KV Cache per-token-head 🔥)

- **Cấu hình**: Image `vllm-v0.22.1-hijack-v4` + `--kv-cache-dtype int4_per_token_head` + `--quantization fp8`
- **Mục đích**: Test INT4 KV cache quantization built-in vLLM v0.22.1. Đây là kỹ thuật mà top teams CHẮC CHẮN đang dùng. Giảm KV bandwidth 4x → TPOT từ 51ms → ~19ms lý thuyết.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**

### Dự đoán lý thuyết (nếu kernel hoạt động đúng)
- KV reads/step: 120 × 30k × 3KB = 10.8 GB (thay vì 43 GB)
- TPOT: 10.8/685 + 3 = ~19ms → s_tpot = 1.00
- TTFT: Giữ nguyên ~611ms (không giảm max-num-seqs)
- Passed SLO: ~85/120 (tương tự baseline)
- **Dự kiến: ~75-85 điểm** (nếu accuracy OK)
