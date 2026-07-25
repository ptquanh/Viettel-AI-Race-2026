# Kết quả thử nghiệm Slot 09 (15:40) - Image v14 Champion Config Baseline

## 1. Thông tin chung

- **Thời gian chấm**: 25/07/2026 15:40:00
- **Submission File**: `exercise 3/submissions/25072026/09-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14`
- **Điểm số**: **59.8700đ**

## 2. Chi tiết chỉ số

- **ERS**: 59.87
- **Total Requests**: 420
- **Failed Requests**: 5
- **TTFT P50**: 55 ms
- **TTFT P95**: 77 ms
- **TBT (TPOT) Median**: 4 ms
- **Tokens/sec**: 0.0595

## 3. Phân tích & Đánh giá

1. **Phục hồi mức ~60 điểm**: Ngay khi quay lại Image v14 Champion Config (`GPU_MEM=0.94` + `SEQS=32` + `spawn`), hiệu năng lập tức bật từ 58.12đ lên 59.87đ (gần 60đ).
2. **Ảnh hưởng traffic chiều**: Mốc 15:40 PM vẫn là giờ làm việc cao điểm, host grader có nhiễu mạng làm TTFT P50 lên 55ms (so với 45ms lúc 10:12 AM).
3. **Chiến lược tiếp theo**: Giữ nguyên 100% Champion Config v14 cho các lượt nộp đêm (sau 19:30) khi traffic hạ nhiệt để đẩy TTFT P50 về <45ms và săn mốc 63-66 điểm.
