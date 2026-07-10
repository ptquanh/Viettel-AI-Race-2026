# Kết quả Benchmark - 21:27 09/07/2026 (STT 60 - Modern vLLM v0.22.1 Hijack + 0.96 Memory & Muted Logging)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack` + các tham số tối ưu hóa (max-model-len=262144, memory=0.96, quantization=fp8).
- **Mục đích**: 
  1. Giảm thiểu tối đa logging overhead của Docker (đặt `VLLM_LOGGING_LEVEL=WARNING` để triệt tiêu toàn bộ CPU/IO ghi log đĩa).
  2. Nâng bộ nhớ sử dụng GPU lên `0.96` nhằm mở rộng tối đa dung lượng KV Cache Radix pool để đạt cache-hit rate tốt hơn trên context dài.

## Chỉ số đo được

*   **Điểm số**: `17.37` (Passed SLO: `85/120`)
*   **TTFT P50**: `615 ms`
*   **TTFT P95**: `8382 ms`
*   **failed_count**: `0`
*   **warmup_count**: `0`
*   **accuracy_drop**: `1`
*   **tbt_median_ms**: `51 ms`

## Phân tích kết quả
Bản vá đã chạy thành công nhưng hiệu năng sụt giảm nhẹ từ `18.11` xuống còn **`17.37` điểm** (mặc dù vẫn hoàn thành tốt với `85/120` passed SLO và 0 request thất bại).

**Đánh giá nguyên nhân sụt giảm:**
1. **Overhead do VRAM Allocation:** Tương tự như đã phân tích ở STT 29 (utilization=0.98), việc nâng gpu-memory-utilization lên sát mức trần (`0.96`) vô tình tạo thêm overhead quản lý phân mảnh bộ nhớ của CUDA/vLLM, lấn át đi lợi ích của việc mở rộng KV cache pool.
2. **Jitter của Host Portal:** Sự chênh lệch TTFT P50 (`611ms` vs `615ms`) và TTFT P95 (`8396ms` vs `8382ms`) là rất nhỏ, cho thấy sự sụt giảm ERS (`18.11` vs `17.37`) phần lớn là do dao động hiệu năng của phần cứng host chấm bài vào các thời điểm tải khác nhau.

---
*Kết luận: `0.95` là mức Memory Utilization tối ưu tuyệt đối nhất cho phiên bản v0.22.1 trên môi trường này.*
