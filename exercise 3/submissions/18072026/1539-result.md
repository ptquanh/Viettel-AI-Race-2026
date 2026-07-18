# Kết quả Benchmark - 15:39 18/07/2026 (STT 44 - Slot 14 - Custom Image + Seqs=24 + Len=8192)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + **`VLLM_MAX_NUM_SEQS=24`** + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + **`--max-model-len=8192` (TỐI ƯU HÓA BỘ NHỚ)** + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá hiệu năng khi giảm concurrency (hàng đợi đồng thời) từ 32 xuống 24 trên nền đã tối ưu hóa chiều dài mô hình (Len=8192) để cải thiện TTFT và TPOT.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **60.07** | Điểm số cuối cùng                                     |
| `ers`           | **60.07** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **6**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **52 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **69 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu quả giảm Concurrency (`Seqs=24`) lên trễ đuôi**:
   - Khi giảm concurrency xuống 24, trễ đuôi **TTFT P95 đạt 69ms** (đây là trễ đuôi thấp nhất trong ngày 18/07, thấp hơn cả Slot 2 là 70ms và Slot 13 là 73ms). Điều này chứng minh rằng việc thu hẹp hàng đợi đồng thời giúp giảm thiểu đáng kể xung đột tài nguyên GPU khi Poisson burst đạt đỉnh.
   
2. **Ảnh hưởng lên Latency trung bình (TTFT P50)**:
   - **TTFT P50 vẫn ở mức 52ms** (so với 45ms của Slot 2 và 53ms của Slot 13). Việc giảm concurrency xuống quá mức (24) khiến hàng đợi lập lịch của vLLM bị nghẽn nhẹ khi các request Poisson Burst đến dồn dập, dẫn đến trễ trung bình P50 bị kéo dài hơn so với mốc ngọt `Seqs=32` của Slot 2.
   - **Failed requests tăng lên 6** (so với 5 của Slot 13).
   - **ERS đạt 60.07**: Cho thấy hiệu năng chung khá cân bằng so với Slot 13 (60.10) nhưng vẫn kém hơn một chút so với mốc ngọt của Slot 2 (60.91).

3. **Bài học rút ra**:
   - **Seqs=32 là điểm ngọt tối ưu (sweet-spot) của LFM2.5 trên MiG partition**.
     - Giảm xuống 24 làm nghẽn hàng đợi (TTFT P50 tăng lên 52ms).
     - Tăng lên 48 làm tranh chấp compute (TTFT P50 tăng lên 53ms).
   - Do đó, cấu hình concurrency `Seqs=32` của Slot 2 mang lại sự cân bằng tốt nhất giữa TTFT trung bình và trễ đuôi.
   - **Kết luận**: Cố định `VLLM_MAX_NUM_SEQS=32` cho cấu hình Golden Combo (Slot 15).
