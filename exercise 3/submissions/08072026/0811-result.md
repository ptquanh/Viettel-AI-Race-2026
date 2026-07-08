# Kết quả Benchmark - 08:11 08/07/2026 (STT 44 - Aphrodite FP8 Test)

- **Cấu hình**: `aphroditeorg/aphrodite:latest` + `--model=/model` + `--quantization=fp8` + `--enable-prefix-caching` + `--enable-chunked-prefill`.
- **Mục đích**: Thử nghiệm Aphrodite Engine (một fork tối ưu của vLLM) chạy mô hình lượng hóa FP8.

## Chỉ số đo được

- **Kết quả**: **Thất bại (Chấm điểm thất bại - Startup Timeout)**
- **Lỗi**: `spawn contestant container: wait for pod ready: timed out waiting for contestant pod to be ready: context deadline exceeded`

### Nhận xét & Phân tích:
1. **Lỗi pull image timeout:** Do image `aphroditeorg/aphrodite:latest` quá nặng (~15GB), quá trình tải xuống và giải nén trên hạ tầng chấm thi bị quá hạn (timed out).
2. **Khả năng tương thích:** Tương tự như SGLang, các image engine ngoài vLLM có dung lượng rất lớn và không được cached sẵn trên các node của BTC, gây tỷ lệ lỗi pull timeout cực cao.

---
