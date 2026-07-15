# Kết quả Benchmark - 12:12 15/07/2026 (STT 111 - Tối ưu CPU Threading OMP=6)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=24` + `OMP_NUM_THREADS=6` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384`.
- **Mục đích**: Tăng OpenMP threads lên 6 để tối ưu hóa tối đa năng lực xử lý CPU của baseline tốt nhất.

## Chỉ số đo được

| Chỉ số          |    Giá trị    | Ý nghĩa                                             |
| :-------------- | :-----------: | :-------------------------------------------------- |
| `final_score`   |   **42.24**   | Điểm số cuối cùng                                   |
| `ers`           |   **42.24**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.366667**  | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |     **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **44**     | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |    **120**    | Tổng số request benchmark                           |
| `failed_count`  |     **0**     | Số lượng request thất bại                           |
| `warmup_count`  |     **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**     | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |   **22 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **3292 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   |  **6392 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả
1. **Phân tích hiệu năng**:
   - Khi tăng `OMP_NUM_THREADS` lên 6, TPOT vẫn giữ vững ở mức tốt nhất là **22ms**.
   - Tuy nhiên, **TTFT P50 bị tăng từ 3015ms lên 3292ms** (tăng ~270ms). Nguyên nhân do cấu hình phần cứng Grader chỉ cấp 3 cores CPU vật lý. Việc chạy quá nhiều OpenMP threads (6 threads) đã gây ra tranh chấp tài nguyên và overhead chuyển cảnh ngữ cảnh (context switching) nghiêm trọng giữa các luồng CPU, làm chậm quá trình chuẩn bị prefill của scheduler.
   - Điểm số cuối cùng đạt 42.24, thấp hơn mức kỷ lục 42.33 của cấu hình OMP=4.
2. **Phân tích độ chính xác**:
   - `accuracy_drop` duy trì 0%.
3. **Kết luận**:
   - Khẳng định `OMP_NUM_THREADS=4` là điểm ngọt kỹ thuật tối ưu nhất trên hạ tầng 3 cores CPU vật lý của BTC. Cấu hình OMP=6 gây nghẽn do quá tải tranh chấp luồng và bị loại bỏ.
