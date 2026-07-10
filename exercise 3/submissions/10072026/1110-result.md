# Kết quả Benchmark - 08:45 10/07/2026 (STT 63 - FlashInfer Attention Backend via Hijack)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-flashinfer` + STT 21 config + `VLLM_ATTENTION_BACKEND=FLASHINFER`.
- **Mục đích**: Thử nghiệm FlashInfer attention backend thay vì FlashAttention mặc định. FlashInfer có thể hiệu quả hơn cho decode batched với long context, giảm TPOT.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
