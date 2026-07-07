# Kết quả Benchmark - Slot 10 07/07/2026 (Disable Prefix Caching Test)

- **Cấu hình**: Baseline mới (STT21) + `--no-enable-prefix-caching` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Kiểm tra xem liệu prefix caching (Radix tree) có đang gây ra CPU overhead lớn cho 3 nhân CPU yếu của MiG H200 hay không. Nếu bật thêm cờ `--no-enable-prefix-caching` mà điểm số cải thiện, chứng tỏ việc quản lý cache đang là cổ chai của CPU.

## Chỉ số đo được

TBD

---
