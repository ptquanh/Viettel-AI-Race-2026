# Kết quả Benchmark - 23:02 10/07/2026 (STT 74 - TurboQuant FP8-INT4 Hybrid KV Cache 🔥 - Đổi tên từ 2251)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v4` + `--kv-cache-dtype turboquant_k8v4` + `--quantization fp8`
- **Mục đích**: Chạy thử nghiệm cờ nén lai FP8 Keys + 4-bit Values của TurboQuant để kiểm tra sự ổn định accuracy và so sánh throughput/TPOT với bản 4-bit thuần.

## Chỉ số đo được

- **Score (Điểm số)**: **Fail (Chấm điểm thất bại)**
- **Chi tiết lỗi**: `protocol aborted: primer: 120/120 transport errors (> 10%) — contestant server unscoreable`

### Nhận xét & Phân tích

- Thử nghiệm cờ nén lai `turboquant_k8v4` thất bại hoàn toàn do gặp 120/120 lỗi truyền tải (transport errors) khi bắt đầu nhận request chấm điểm.
- Khác với cờ `turboquant_4bit_nc` bị crash ngay từ lúc init model (exited 1), container sử dụng `turboquant_k8v4` đã vượt qua bước kiểm tra Pod Ready (API Server mở port 8000 thành công). Tuy nhiên, khi Grader gửi request đầu tiên (primer) đến để đo đạc, server đã không thể xử lý hoặc bị deadlock/crash ngầm trong engine core, dẫn đến việc không có kết nối phản hồi.
- Điều này củng cố nhận định: Cả họ tối ưu hóa TurboQuant trên bản dựng vLLM này của portal đều không chạy ổn định trên phần cứng hoặc đang bị lỗi tương thích nghiêm trọng với vLLM V1 engine tự động kích hoạt.
