# Kết quả Benchmark - 15/07/2026 (STT 103 - slot 0831 - OMP=2)

- **Cấu hình**: Seqs=24, Chunk=16384, **OMP_NUM_THREADS=2** (giảm 1 thread so với baseline 3), Warmup=ON, Custom Kernel=ON.
- **Mục đích**: Đánh giá xem việc giảm số thread từ 3 xuống 2 có giúp giảm tải context switching cho CPU 3 cores hay không.

## Chỉ số đo được

- **Điểm số**: **42.02**
- **Số request vượt qua SLO**: 52/120 (passed_slo)
- **TTFT P50**: **3638 ms** (cải thiện rõ rệt so với 4268ms ở OMP=3)
- **TTFT P95**: **6418 ms**
- **TPOT Median**: **22 ms**
- **Accuracy drop**: 0 (GPQA)

## Phân tích kết quả

1. **TTFT cải thiện lớn, passed_slo tăng vượt trội**:
   - TTFT P50 giảm từ **4268 ms xuống còn 3638 ms** (giảm ~630ms, tương đương cải thiện 15%).
   - Số lượng passed_slo vọt từ **20 lên 52/120** (tăng gấp 2.6 lần!).
   - Điều này xác nhận việc giảm CPU threads giúp giảm tranh chấp tài nguyên (thread context switching) trên CPU 3 cores, đẩy nhanh tiến độ xử lý prefill của vLLM.
2. **TPOT tăng nhẹ và điểm số thay đổi**:
   - TPOT Median tăng nhẹ lên **22 ms** (so với 21ms ở OMP=3).
   - Điểm số tổng đạt **42.02** (thấp hơn chút ít so với 42.27 do TPOT bị ảnh hưởng nhỏ).
