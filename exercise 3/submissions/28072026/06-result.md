# Kết quả Benchmark - Slot 06 (v22.2 linear_batch_invariant Hook Fix)

- **Cấu hình**: Image `vllm-lfm25:v22.2-int4-marlin` (Bổ sung Hook cho `linear_batch_invariant` để tránh C++ Exception khi vLLM V1 truyền unquantized empty tensor).
- **Mục đích**: Xác minh khắc phục triệt me lỗi Engine Core Initialization crash, đánh giá hiệu năng TPOT và TTFT thực tế của INT4 Marlin online quantization.

## Kết quả thử nghiệm Slot 06

**Trạng thái**: Đang chờ nộp & chấm điểm...
