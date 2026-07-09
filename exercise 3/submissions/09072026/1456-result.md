# Kết quả Benchmark - 14:56 09/07/2026 (STT 58 - Modern vLLM v0.22.1 Hijack + 18.99 Baseline Restore & Prefill Interleaving)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack` + các tham số tối ưu hóa (max-model-len=262144, memory=0.95, quantization=fp8, enable-chunked-prefill).
- **Mục đích**: Khôi phục cấu hình tương tự như STT 21 (18.99 điểm) đi kèm với chunked-prefill ở mức mặc định (chunk=512) nhằm loại bỏ tình trạng prefill-decode blocking gây nghẽn latency giải mã.

## Chỉ số đo được

*   **Điểm số**: `17.76` (Passed SLO: `84/120`)
*   **TTFT P50**: `615 ms`
*   **TTFT P95**: `8910 ms`
*   **failed_count**: `0`
*   **warmup_count**: `0`
*   **accuracy_drop**: `0`
*   **tbt_median_ms**: `50 ms`

## Phân tích kết quả
Kết quả đã quay về đúng quỹ đạo của baseline tốt nhất (STT 21 đạt `18.99` và median các lượt verify dao động khoảng `17.05 - 18.09`). Lượt chạy này đã giải quyết triệt để lỗi OOM GPU Worker và sửa được lỗi sụt giảm TTFT nghiêm trọng do prefill blocking.

**Đánh giá chi tiết:**
*   **TTFT P50** đã giảm mạnh từ `1587 ms` xuống còn `615 ms` (giảm hơn một nửa!).
*   Số lượng request pass SLO phục hồi về `84/120` (so với `80/120` của lần trước).
*   Tuy nhiên, điểm số `17.76` vẫn thấp hơn đỉnh cao của STT 21 (`18.99`). Có vẻ như chunked prefill mặc định với block size `512` gây ra một chút overhead về scheduling khiến TTFT P95 tăng nhẹ từ ~8.3s lên `8.9s`.

---
*Kết luận: Cần thử nghiệm cấu hình tối ưu hóa tiếp theo (STT 59) bằng cách tinh chỉnh tham số để so sánh: hoặc tắt chunked-prefill để quay lại STT 21 gốc thuần túy, hoặc cấu hình MTP Speculative Decoding bằng thuật toán tương thích mới của Qwen3.5.*
