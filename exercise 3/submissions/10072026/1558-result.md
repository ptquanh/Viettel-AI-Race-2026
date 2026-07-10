# Kết quả Benchmark - 15:58 10/07/2026 (STT 69 - Ghost Strategy v3: Slot 9 Conservative Tweak)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v3` + biến môi trường: `VLLM_MAX_NUM_SEQS=64`, `VLLM_MAX_NUM_BATCHED_TOKENS=2048`, `VLLM_ENABLE_CHUNKED_PREFILL=1`.
- **Mục đích**: Phương án an toàn (Conservative) với `--max-num-seqs 64` (mức giảm nhẹ hơn). Nếu Slot 6 (Seqs 48) hoặc Slot 7 (Seqs 32) làm hàng đợi nghẽn quá nhiều gây tăng TTFT và tụt passed_slo nghiêm trọng, thì Slot 9 sẽ là phương án bảo toàn TTFT tốt nhất mà vẫn kéo nhẹ TPOT xuống vùng ~37ms.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
