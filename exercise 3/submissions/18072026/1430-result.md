# Kết quả Benchmark - 14:30 18/07/2026 (STT 43 - Slot 13 - Custom Image + Seqs=48 + Len=8192)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + **`VLLM_MAX_NUM_SEQS=48`** + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + **`--max-model-len=8192` (TỐI ƯU HÓA BỘ NHỚ)** + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá hiệu năng khi tăng concurrency (hàng đợi đồng thời) từ 32 lên 48 trên nền đã tối ưu hóa chiều dài mô hình (Len=8192) để giải phóng VRAM.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **60.10** | Điểm số cuối cùng                                     |
| `ers`           | **60.10** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **5**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **53 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **73 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu quả của việc giảm `--max-model-len=8192` đối với Concurrency**:
   - Khi tăng concurrency lên `Seqs=48` kết hợp với `Len=8192`, số request thất bại giảm từ 7 xuống còn **5**. Điều này chứng tỏ việc giới hạn chiều dài mô hình về đúng đặc tả workload thực tế giúp giải phóng bộ nhớ đáng kể, giảm thiểu preemption khi scheduler chạy với concurrency cao.
2. **Ảnh hưởng lên Latency (TTFT)**:
   - **TTFT P50 tăng lên 53ms** (so với 45ms của Slot 2). Lý do là vì concurrency tăng từ 32 lên 48 làm tăng độ tranh chấp tài nguyên tính toán (compute contention) trên MiG partition H200 (chỉ có 3 core CPU và GPU MiG nhỏ), khiến hàng đợi xử lý prefill của các request đơn lẻ bị kéo dài hơn.
   - **TTFT P95 cải thiện đạt 73ms** (so với 86ms của custom baseline không compile). So với Slot 2 (70ms), mức tăng trễ đuôi là rất ít.
   - **ERS đạt 60.10**: Thấp hơn Slot 2 (60.91) một chút do trễ P50 tăng, nhưng vẫn là mức điểm rất tốt (>60).

3. **Bài học rút ra**:
   - Tăng concurrency lên 48 giúp xử lý song song nhiều request hơn và giảm lỗi, nhưng lại làm chậm tốc độ phản hồi trung bình (TTFT P50) do quá tải compute.
   - Định hướng: Slot 14 với concurrency thấp hơn (`Seqs=24`) và tối ưu hóa bộ nhớ `Len=8192` hứa hẹn sẽ kéo giảm TTFT P50 xuống cực thấp.
