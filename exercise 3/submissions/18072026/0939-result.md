# Kết quả Benchmark - 09:39 18/07/2026 (STT 34 - Slot 4 - Custom Image + Enforce Eager - Seqs=32 + FP8 + Warmup + Custom Kernels + Enforce Eager)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--enforce-eager` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đo lường hiệu năng của chế độ Eager Mode thuần túy (tắt hoàn toàn CUDA Graphs) trên nền Custom Image để đánh giá hiệu quả của CUDA Graphs.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **57.06** | Điểm số cuối cùng                                     |
| `ers`           | **57.06** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **5**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **62 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **89 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng sụt giảm rõ rệt**:
   - Điểm số **ERS giảm đáng kể xuống còn 57.06** (so với 59.51 của Custom Baseline và 60.91 của Compile L3).
   - Tắt CUDA Graphs qua `--enforce-eager` làm tăng mạnh độ trễ TTFT:
     - **TTFT P50 tăng từ 50ms lên 62ms** (+24%).
     - **TTFT P95 tăng từ 86ms lên 89ms** (+3.5%).
   - Kết quả này khẳng định vai trò cực kỳ quan trọng của **CUDA Graphs** trong vLLM: giúp giảm thiểu đáng kể overhead lập lịch kernel của CPU, đặc biệt đối với mô hình nhỏ như LFM2.5 (1.2B) khi mà overhead CPU chiếm tỷ trọng lớn trong tổng thời gian xử lý.

2. **Độ ổn định**:
   - Số lượng request thất bại giảm nhẹ còn **5 requests** (so với 6/7 ở các slot trước). Điều này cho thấy chế độ Eager thuần có thể ổn định hơn một chút trong việc cấp phát bộ nhớ GPU vì không phải lưu trữ các graph tĩnh của CUDA Graphs, giảm thiểu khả năng xảy ra lỗi cấp phát đột ngột khi bộ nhớ bão hòa. Tuy nhiên, mức cải thiện nhỏ này không đủ bù đắp tổn thất lớn về mặt latency.
