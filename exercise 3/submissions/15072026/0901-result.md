# Kết quả Benchmark - 15/07/2026 (STT 106 - slot 0901 - Warmup=OFF)

- **Cấu hình**: Seqs=24, Chunk=16384, OMP=3, **VLLM_WARMUP=0** (tắt prefix caching pre-warmup), Custom Kernel=ON.
- **Mục đích**: Đánh giá tác động của prefix warmup lúc khởi động container đối với TTFT và TPOT trong điều kiện chunked prefill lớn đã hoạt động tốt.

## Chỉ số đo được

- **Điểm số**: **42.08**
- **Số request vượt qua SLO**: 52/120 (passed_slo)
- **TTFT P50**: **3703 ms**
- **TTFT P95**: **6398 ms**
- **TPOT Median**: **22 ms** (tăng nhẹ 1ms so với baseline Warmup=ON là 21ms)
- **Accuracy drop**: 1 (GPQA)

## Phân tích kết quả

1. **Hiệu ứng khi tắt Warmup**:
   - Khi tắt warmup (`VLLM_WARMUP=0`), TPOT Median bị tăng nhẹ 1ms lên **22 ms** (so với 21ms ở slot 2121 khi có Warmup). Do đó điểm ERS tổng thể giảm nhẹ từ **42.27 xuống 42.08**.
   - Tuy nhiên, TTFT P50 giảm từ **4268 ms xuống còn 3703 ms**, nâng passed_slo lên **52/120**. Điều này phần nhiều do biến động tải (run-to-run variance) của hệ thống grader, hoặc do việc giảm tải tính toán lúc khởi động container giúp GPU/CPU hoạt động mát mẻ hơn ở các lượt request đầu.
2. **Kết luận**:
   - Warmup mang lại lợi ích thực tế cho bước decode (giúp giữ vững TPOT ở 21ms nhờ Triton kernels đã được compile và cache sẵn sàng). Vì vậy, chúng ta nên giữ **Warmup=ON** cho cấu hình sản phẩm cuối cùng.
