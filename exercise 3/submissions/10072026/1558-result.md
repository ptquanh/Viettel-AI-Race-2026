# Kết quả Benchmark - 15:58 10/07/2026 (STT 69 - Ghost Strategy v3: Slot 9 Conservative Tweak)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v3` + biến môi trường: `VLLM_MAX_NUM_SEQS=64`, `VLLM_MAX_NUM_BATCHED_TOKENS=2048`, `VLLM_ENABLE_CHUNKED_PREFILL=1`.
- **Mục đích**: Phương án an toàn (Conservative) với `--max-num-seqs 64` (mức giảm nhẹ hơn). Nếu Slot 6 (Seqs 48) hoặc Slot 7 (Seqs 32) làm hàng đợi nghẽn quá nhiều gây tăng TTFT và tụt passed_slo nghiêm trọng, thì Slot 9 sẽ là phương án bảo toàn TTFT tốt nhất mà vẫn kéo nhẹ TPOT xuống vùng ~37ms.

## Chỉ số đo được

- **Score (Điểm số)**: **15.47** (Passed SLO: 84/120)
- **erc**: 0.7
- **ers**: 15.47
- **penalty**: 1
- **ttft_p50_ms**: 692 ms
- **ttft_p95_ms**: 10137 ms
- **tbt_median_ms (TPOT)**: 59 ms
- **failed_count**: 0

### Nhận xét & Phân tích

- Thử nghiệm Conservative này (`--max-num-seqs 64`) cho kết quả tương tự Seqs 48:
  - TPOT vẫn bị giữ nguyên ở mức **59ms**.
  - TTFT P50 là **692ms** (so với 637ms của Seqs 48).
- Rút ra kết luận quan trọng cho Ghost Strategy v3:
  - Bất kỳ cấu hình nào sử dụng **BF16 KV Cache** thông thường trên vLLM v0.22.1 (kể cả khi giảm max-num-seqs về 64, 48 hay 32) đều không vượt qua được ngưỡng cản TPOT 50-60ms do sự kết hợp giữa bandwidth đọc cache và scheduling overhead.
  - Điều này giải thích tại sao baseline ban đầu của BTC (STT 4) đạt TPOT 51ms dù max-num-seqs ở mức mặc định (86+).
  - Tối ưu hóa ở mức concurrency (batch size) không có tác dụng làm giảm TPOT cho mô hình này trên MiG H200 nếu không đổi kiểu biểu diễn KV cache (quantization).
