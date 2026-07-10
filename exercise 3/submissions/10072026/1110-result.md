# Kết quả Benchmark - 08:45 10/07/2026 (STT 63 - FlashInfer Attention Backend via Hijack)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-flashinfer` + STT 21 config + `VLLM_ATTENTION_BACKEND=FLASHINFER`.
- **Mục đích**: Thử nghiệm FlashInfer attention backend thay vì FlashAttention mặc định. FlashInfer có thể hiệu quả hơn cho decode batched với long context, giảm TPOT.

- **Điểm số**: `17.73` (Passed SLO: `85/120`)
- **TTFT P50**: `655 ms`
- **TTFT P95**: `8345 ms`
- **failed_count**: `0`
- **warmup_count**: `0`
- **accuracy_drop**: `2%`
- **tbt_median_ms**: `51 ms`

## Phân tích kết quả

FlashInfer attention backend cho kết quả **17.73 điểm**, tương đối ổn định so với cấu hình gốc STT 21 (khoảng 17-18.99 điểm tùy theo jitter của host).

1. **TPOT (tbt_median_ms):** Vẫn giữ ở mức `51 ms`, không có sự cải thiện so với FlashAttention mặc định. Điều này cho thấy sự nghẽn cổ chai TPOT không nằm ở backend attention computation (đối với model Qwen3.5-2B nhỏ này), mà thực sự nằm ở GIL scheduler của vLLM v0.22.1 trên 3 CPU cores.
2. **TTFT P95:** Đạt `8345 ms`, tương đương với STT 21 gốc.
3. **Độ chính xác:** Sụt giảm 2% ($\Delta = 2 \le 10$), do đó không bị phạt điểm ($f(2) = 1.0$).

**Kết luận:** FlashInfer hoạt động ổn định nhưng không giải quyết được bài toán TPOT 51ms. Cần tiếp tục hướng đi chuyển đổi sang vLLM v0.5.2 (Ghost Strategy v2).
