# Kết quả thử nghiệm Slot 13 (22:19) - Image v14 Champion Config

## 1. Thông tin chung

- **Thời gian chấm**: 25/07/2026 22:19:00
- **Submission File**: `exercise 3/submissions/25072026/2219-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14`
- **Điểm số**: **59.6700đ**

## 2. Chi tiết chỉ số

- **ERS**: 59.67
- **Total Requests**: 420
- **Failed Requests**: 5
- **TTFT P50**: 56 ms
- **TTFT P95**: 73 ms
- **TBT (TPOT) Median**: 4 ms
- **Tokens/sec**: 0.0588

## 3. Phân tích & Đánh giá

1. **Duy trì mốc ~60đ ổn định**: Nộp liên tiếp sau Slot 12 (22:19 vs 22:18), điểm số duy trì mức ổn định **59.67đ**.
2. **Nhiễu hệ thống do nộp dồn**: TTFT P50 tăng nhẹ lên 56ms (so với 50ms ở 22:18) do hai lượt nộp quá gần nhau làm grader chịu tải dồn.
3. **Chiến lược tiếp theo**: Giãn khoảng cách giữa các lượt nộp còn lại (Slots 14 và 15) sau 23:00 để hạ TTFT P50 về mức kỷ lục <45ms.
