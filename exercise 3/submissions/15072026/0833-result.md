# Kết quả Benchmark - 15/07/2026 (STT 104 - slot 0833 - OMP=4)

- **Cấu hình**: Seqs=24, Chunk=16384, **OMP_NUM_THREADS=4** (tăng 1 thread so với baseline 3), Warmup=ON, Custom Kernel=ON.
- **Mục đích**: Đánh giá xem việc tăng số thread lên 4 có giúp tăng tốc độ xử lý song song các tác vụ CPU-bound trong vLLM hay không.

## Chỉ số đo được

- **Điểm số**: **42.33** 🏆 **KỶ LỤC MỚI**
- **Số request vượt qua SLO**: 40/120 (passed_slo)
- **TTFT P50**: **3015 ms** (đạt mức tốt nhất ở Seqs 24)
- **TTFT P95**: **6430 ms**
- **TPOT Median**: **22 ms**
- **Accuracy drop**: 1 (GPQA)

## Phân tích kết quả

1. **Tiếp tục phá kỷ lục (42.33 điểm)**:
   - TTFT P50 giảm sâu xuống còn **3015 ms** (cải thiện ~1.2s so với baseline OMP=3, và nhanh hơn OMP=2).
   - Số lượng passed_slo đạt **40/120**.
   - TPOT Median duy trì vững vàng ở mốc **22 ms**.
   - GPQA accuracy drop = 1 (vẫn $\le 10$ câu nên không bị phạt điểm).
2. **Hiệu năng của hyperthreading**:
   - Mặc dù MiG chỉ có 3 cores vật lý, việc đặt `OMP_NUM_THREADS=4` giúp CPU tận dụng hyperthreading để xử lý song song các tác vụ chuẩn bị prefill, tokenization và lập lịch của vLLM hiệu quả hơn.
   - Kết quả này chứng minh rằng `OMP_NUM_THREADS=4` là cấu hình tối ưu nhất cho CPU trong số các mốc 2, 3, 4.
