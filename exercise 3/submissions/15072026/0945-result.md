# Kết quả Benchmark - 09:45 15/07/2026 (STT 107 - Tối ưu Concurrency Seqs=48)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=48` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384`.
- **Mục đích**: Tối ưu Concurrency Seqs lên 48 để hấp thụ Turn 2 mà không bắt chúng phải chờ hàng đợi, giảm TTFT P50.

## Chỉ số đo được

| Chỉ số          |    Giá trị    | Ý nghĩa                                             |
| :-------------- | :-----------: | :-------------------------------------------------- |
| `final_score`   |   **25.91**   | Điểm số cuối cùng                                   |
| `ers`           |   **25.91**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.558333**  | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |     **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **67**     | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |    **120**    | Tổng số request benchmark                           |
| `failed_count`  |     **0**     | Số lượng request thất bại                           |
| `warmup_count`  |     **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**     | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |   **31 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **1802 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   |  **2776 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả
1. **Phân tích hiệu năng**:
   - Đúng như dự đoán, việc tăng `max_num_seqs` từ 24 lên 48 giúp **TTFT P50 giảm mạnh từ 3015ms xuống còn 1802ms** (giảm 40%), và `passed_slo` tăng từ 40 lên 67. Điều này chứng minh hàng đợi đã được giải phóng đáng kể.
   - Tuy nhiên, TPOT (`tbt_median_ms`) bị **tăng mạnh từ 22ms lên 31ms** (tăng 40%). Sự sụt giảm TPOT này khiến điểm số của các request đạt SLO bị kéo thấp đáng kể (S_tpot giảm từ 0.84 xuống 0.31), dẫn đến điểm số cuối cùng giảm xuống còn 25.91.
2. **Phân tích độ chính xác**:
   - `accuracy_drop` là 0%, giữ nguyên chất lượng mô hình.
3. **Kết luận**:
   - Tăng Seqs lên 48 làm giảm mạnh TTFT nhưng lại gây nghẽn băng thông bộ nhớ khi decode (TPOT tăng từ 22ms lên 31ms), dẫn đến tổng điểm giảm sâu. Ta cần tìm điểm ngọt thấp hơn, ví dụ Seqs=32 để xem có dung hòa được cả hai không.
