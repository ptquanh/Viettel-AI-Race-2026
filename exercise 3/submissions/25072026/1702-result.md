# Kết quả thử nghiệm Slot 10 (17:02) - Speculative Decoding (Draft Model v17)

## 1. Thông tin chung

- **Thời gian chấm**: 25/07/2026 17:02:00
- **Submission File**: `exercise 3/submissions/25072026/1702-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-speculative-v17`
- **Điểm số**: **54.2400đ**

## 2. Chi tiết chỉ số

- **ERS**: 54.24
- **Total Requests**: 420
- **Failed Requests**: 6
- **TTFT P50**: 72 ms
- **TTFT P95**: 97 ms
- **TBT (TPOT) Median**: 4 ms
- **Tokens/sec**: 0.0592

## 3. Phân tích & Đánh giá

1. **TPOT không giảm (vẫn 4ms)**: Cơ chế Speculative Decoding với Draft Model `LFM2.5-350M-Instruct` không mang lại hiệu quả giảm TPOT do kiến trúc LFM2.5 (SSM) không đạt tỷ lệ chấp nhận (acceptance rate) kỳ vọng trên vLLM engine.
2. **Suy giảm TTFT & Tăng Failed**: Việc load thêm Draft Model tạo thêm áp lực overhead trong pha Prefill, làm TTFT P50 tăng từ 45ms lên 72ms (P95 lên 97ms) và 6 request bị timeout/failed.
3. **Kết luận**: Loại bỏ phương án Speculative Decoding đối với kiến trúc LFM. Chuyển sang thử nghiệm Multi-step Scheduling trên V1 Engine (Image v14) ở Slot 11.
