# Kết quả Benchmark - 10:12 15/07/2026 (STT 108 - Tối ưu Concurrency Seqs=64)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=64` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384`.
- **Mục đích**: Tối ưu Concurrency Seqs lên 64 để hấp thụ thêm Turn 3 mà không bắt chúng phải chờ hàng đợi.

## Chỉ số đo được

| Chỉ số          |    Giá trị    | Ý nghĩa                                             |
| :-------------- | :-----------: | :-------------------------------------------------- |
| `final_score`   |   **21.08**   | Điểm số cuối cùng                                   |
| `ers`           |   **21.08**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           |   **0.475**   | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |     **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **57**     | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |    **120**    | Tổng số request benchmark                           |
| `failed_count`  |     **0**     | Số lượng request thất bại                           |
| `warmup_count`  |     **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**     | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |   **31 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **2068 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   |  **3016 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả
1. **Phân tích hiệu năng**:
   - Khi tăng `max_num_seqs` từ 48 (Slot 5) lên 64, hiệu năng hệ thống bị quá tải nghiêm trọng. 
   - **TTFT P50 tăng ngược trở lại** từ 1802ms lên 2068ms. Nguyên nhân là khi có quá nhiều request chạy đồng thời (Seqs=64), GPU phải xử lý song song quá nhiều decode steps. Việc này chiếm dụng băng thông bộ nhớ và làm chậm tiến trình prefill của các chunk, khiến TTFT bị kéo dài thêm.
   - TPOT (`tbt_median_ms`) vẫn giữ ở mức nghẽn **31ms**. Điểm số cuối cùng giảm còn 21.08.
2. **Phân tích độ chính xác**:
   - `accuracy_drop` tiếp tục duy trì 0%, không có sụt giảm chất lượng.
3. **Kết luận**:
   - Khẳng định Seqs từ 48 trở lên gây quá tải hệ thống phục vụ (MIG H200), làm tăng cả TTFT và TPOT. Cấu hình này thất bại và cần bị loại bỏ.
