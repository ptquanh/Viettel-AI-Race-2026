# Kết quả Benchmark - 18:57 07/07/2026 (Slot 11 - SGLang FP8 Test)

- **Cấu hình**: `lmsysorg/sglang:v0.4.6.post1` + `--model-path=/model` + `--quantization=fp8` + `--context-length=65536` + `--mem-fraction-static=0.88` + `--max-running-requests=64` + `--disable-cuda-graph` (SGLang FP8 + Radix Cache ON).
- **Mục đích**: Khảo sát hiệu năng của SGLang so với vLLM.

## Chỉ số đo được

- **Kết quả**: **Thất bại (Chấm điểm thất bại - Startup Timeout)**
- **Lỗi**: `spawn contestant container: wait for pod ready: timed out waiting for contestant pod to be ready: context deadline exceeded`

### Nhận xét & Phân tích:

1. **Lỗi pull image timeout:** Do dung lượng image `lmsysorg/sglang:v0.4.6.post1` quá lớn (~12-15GB), quá trình tải xuống (pull) trên hạ tầng kiểm thử của BTC đã bị quá thời hạn cho phép (timed out waiting for contestant pod to be ready).
2. **Kết luận:** Chuyển hướng quay về cấu hình vLLM STT21 tốt nhất để chạy verify 3 lần lấy median an toàn trước khi kết thúc ngày.

---
