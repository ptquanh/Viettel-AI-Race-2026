# Kết quả Benchmark - 10:16 15/07/2026 (STT 109 - Tối ưu Concurrency Seqs=32)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=32` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384`.
- **Mục đích**: Tối ưu Concurrency Seqs lên 32 để tìm điểm ngọt dung hòa giữa TTFT và TPOT.

## Chỉ số đo được

| Chỉ số          |   Giá trị   | Ý nghĩa                                             |
| :-------------- | :---------: | :-------------------------------------------------- |
| `final_score`   |  **31.19**  | Điểm số cuối cùng                                   |
| `ers`           |  **31.19**  | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           |  **0.475**  | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**    | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |   **57**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**   | Tổng số request benchmark                           |
| `failed_count`  |    **0**    | Số lượng request thất bại                           |
| `warmup_count`  |    **0**    | Số lượng request warmup                             |
| `accuracy_drop` |   **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **26 ms**  | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **2271 ms** | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **4898 ms** | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Phân tích hiệu năng**:
   - Ở Seqs=32, TPOT (`tbt_median_ms`) đạt **26ms**, tốt hơn nhiều so với 31ms ở Seqs=48 và Seqs=64, chứng tỏ băng thông bộ nhớ ít bị nghẽn hơn.
   - TTFT P50 đạt **2271ms** (tăng nhẹ so với 1802ms ở Seqs=48 do queueing delay tăng lên khi giảm số lượng slot xử lý song song).
   - Tuy nhiên, mức tăng 4ms của TPOT (từ 22ms lên 26ms) bị phạt rất nặng bởi công thức lũy thừa (S_tpot giảm từ 84.6% xuống còn 57.7%). Do đó, mặc dù passed_slo tăng từ 40 lên 57, tổng điểm vẫn bị giảm từ 42.33 xuống còn 31.19.
2. **Phân tích độ chính xác**:
   - `accuracy_drop` duy trì ở mức 0%.
3. **Kết luận**:
   - Seqs=32 cho thấy sự cải thiện rõ rệt so với Seqs=48 và Seqs=64 nhưng vẫn kém xa Seqs=24 về mặt điểm số ERS do TPOT cực kỳ nhạy cảm. Seqs=24 vẫn là cấu hình tối ưu nhất cho Serving trên MIG instance này.
