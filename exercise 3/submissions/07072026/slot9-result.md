# Kết quả Benchmark - Slot 9 07/07/2026 (Slot 9b Combo Test)

- **Cấu hình**: Baseline mới + `--max-num-batched-tokens=24576` + `--max-num-seqs=96` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Áp dụng bài học từ Slot 6 (TPOT giảm kỷ lục còn 32ms nhờ batched tokens lớn, nhưng TTFT nổ tung do nghẽn hàng đợi prefill). Bằng cách hạ `max_num_batched_tokens` xuống `24576` kết hợp giới hạn concurrency tối đa `max-num-seqs=96` (thay vì mặc định ~256), ta hy vọng kìm hãm hàng đợi prefill để cứu TTFT P50/P95 trong khi vẫn duy trì được TPOT cực thấp.

## Chỉ số đo được

TBD

---
