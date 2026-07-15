# Kết quả Benchmark - 10:27 15/07/2026 (STT 110 - Tối ưu Concurrency Seqs=96)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=96` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384`.
- **Mục đích**: Tối ưu Concurrency Seqs lên 96 để kiểm tra nốt chịu tải cực đại khi concurrency cực lớn.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |  **22.81**   | Điểm số cuối cùng                                   |
| `ers`           |  **22.81**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.166667** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **20**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **1%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **30 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **2462 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **4029 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Phân tích hiệu năng**:
   - Khi tăng Concurrency lên Seqs=96, TPOT đạt **30ms** (nghẽn bộ nhớ decode tương tự như Seqs=48 và Seqs=64).
   - Tuy nhiên, TTFT P50 tăng lên **2462ms** do GPU quá tải nặng, và passed_slo giảm thảm hại về **20/120** (giống hệt baseline Seqs=24 cũ nhưng TPOT tệ hơn), dẫn đến điểm số giảm mạnh về 22.81.
2. **Phân tích độ chính xác**:
   - `accuracy_drop` là 1%, suy giảm nhẹ không đáng kể.
3. **Kết luận**:
   - Khẳng định Concurrency cao (Seqs=96) hoàn toàn vô dụng trên MIG instance này và chỉ làm hỏng TPOT trong khi TTFT vẫn bị nghẽn do bão hòa năng lực tính toán.
