# Kết quả Benchmark - 12:45 07/07/2026 (Slot 9 - Combo max-num-batched-tokens=24576 + max-num-seqs=96)

- **Cấu hình**: Baseline mới + `--max-num-batched-tokens=24576` + `--max-num-seqs=96` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Tối ưu TPOT bằng batched tokens lớn (24k) để giảm prefill overhead trong khi kìm TTFT P50 bằng giới hạn concurrency tối đa xuống 96.

## Chỉ số đo được

- **Kết quả**: **Thất bại (Chấm điểm thất bại)**
- **Lỗi**: `protocol aborted: primer: 119/120 transport errors (> 10%) — contestant server unscoreable`

### Nhận xét & Phân tích:

1. **Lỗi crash hoặc OOM:** Việc kết hợp batched tokens cực lớn (24k) trên hệ thống giới hạn 18GB VRAM có thể đã dẫn tới lỗi tràn bộ nhớ (Out of Memory) của vLLM engine trong lúc xử lý tải benchmark song song, hoặc gây ra lỗi crash nội bộ của scheduler.
2. **Kết luận:** **CẤM DÙNG** kết hợp các cờ phân bổ batch lớn.

---
