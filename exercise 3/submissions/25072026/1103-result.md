# Kết Quả Thử Nghiệm Slot 06 (11:03 AM - 25/07/2026)

- **Điểm số**: **60.0200** (-2.65đ so với Slot 04 62.67đ)
- **Chỉ số chi tiết**:
  - ERS: 60.02
  - Final Score: 60.02
  - Total Count: 420
  - TTFT P50: 55 ms (+10ms)
  - TTFT P95: 74 ms (+13ms)
  - TPOT (TBT Median): 4 ms
  - Failed Count: 5
  - Warmup Count: 0
  - Accuracy Drop: 0%
  - Penalty: 1
  - Tokens/sec: 0.0600

- **Cấu hình**: Image v14 FP8 (VLLM_MAX_NUM_SEQS=28 + GPU_MEM=0.94 + spawn, Slot 06)
- **Phân tích nguyên nhân**:
  - Thu hẹp VLLM_MAX_NUM_SEQS từ 32 xuống 28 làm hẹp hàng đợi của vLLM Scheduler khi xảy ra Poisson request bursts, khiến TTFT P50/P95 bị đọng trễ (+10ms P50, +13ms P95).
- **Kết luận**: **KHẲNG ĐỊNH VLLM_MAX_NUM_SEQS=32 LÀ MỐC TỐI ƯU KỊCH SÀN!** Giữ cố định SEQS=32.
