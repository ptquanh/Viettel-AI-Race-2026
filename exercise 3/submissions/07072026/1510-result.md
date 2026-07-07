# Kết quả Benchmark - 15:10 07/07/2026 (Slot 10 - Disable Prefix Caching Test)

- **Cấu hình**: Baseline mới (STT21) + `--no-enable-prefix-caching` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Kiểm tra xem liệu prefix caching (Radix tree) có đang gây ra CPU overhead lớn cho 3 nhân CPU yếu của MiG H200 hay không.

## Chỉ số đo được

- **Kết quả**: **Thất bại (Timeout)**
- **Lỗi**: `job exceeded max duration of 2700s with no terminal callback`

### Nhận xét & Phân tích:

1. **Prefix Caching là bắt buộc (P0):** Việc tắt prefix caching khiến toàn bộ 120 requests phải xử lý prefill lại từ đầu đối với prompt siêu dài (20k-42k tokens), dẫn đến tổng khối lượng tính toán cực kỳ khổng lồ (~3.6 triệu tokens prefill). Không có bộ đệm KV Cache dùng chung, GPU liên tục bị nghẽn prefill và quá thời gian xử lý cho phép (2700s).
2. **Kết luận:** **CẤM TẮT prefix caching** dưới mọi hình thức.

---
