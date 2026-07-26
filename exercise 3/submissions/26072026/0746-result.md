# Kết quả thử nghiệm Slot 01 (07:46) - Ngày 26/07 - vLLM V1 Engine Standalone

## 1. Thông tin chung

- **Thời gian chấm**: 26/07/2026 07:46:00
- **Submission File**: `exercise 3/submissions/26072026/0746-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14`
- **Điểm số**: **58.1900đ**

## 2. Chi tiết chỉ số

- **ERS**: 58.19
- **Total Requests**: 420
- **Failed Requests**: 6
- **TTFT P50**: 59 ms
- **TTFT P95**: 81 ms
- **TBT (TPOT) Median**: 4 ms
- **Tokens/sec**: 0.0578

## 3. Phân tích & Đánh giá

1. **V1 Engine Standalone không giảm được TPOT**: Việc chỉ kích hoạt `VLLM_USE_V1=1` (không kèm Speculative) hoàn toàn vô dụng trong việc giảm TPOT. Điểm TPOT vẫn bị kẹt cứng ở 4ms. Điểm tổng tụt xuống 58.19đ (so với mốc 60-62đ của V0 Engine) do V1 Engine làm tăng nhẹ TTFT P50 lên 59ms và gây thêm lỗi (6 failed requests).
2. **Kết luận**: Đòn bẩy thử nghiệm số 2 (dùng V1 Engine Standalone để giảm trễ) đã chính thức thất bại. Scheduler C++ của V1 Engine không đủ sức bẻ gãy overhead nếu không có Speculative Decoding hỗ trợ.

## 4. Hành động tiếp theo

Tiến hành nộp Slot 02 ngay lập tức với vũ khí mạnh hơn: **N-Gram Speculative Decoding + V1 Engine** (`02-docker-compose.yml`) để xem V1 Engine có phát huy sức mạnh khi chạy chế độ đoán trước token hay không.
