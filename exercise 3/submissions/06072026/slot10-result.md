# Kết quả Benchmark - Slot 10 06/07/2026 (max-model-len 65536 Test)

- **Cấu hình**: Baseline mới + `--max-model-len=65536` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc hạ giới hạn độ dài mô hình xuống 65k (vẫn lớn hơn mức 42k tokens thực tế) có cải thiện hiệu năng nhờ giảm overhead lưu metadata không.

## Chỉ số đo được

TBD

---
