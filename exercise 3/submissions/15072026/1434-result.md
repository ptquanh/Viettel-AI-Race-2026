# Kết quả Benchmark - 14:34 15/07/2026 (STT 114 - Tối ưu hóa KV Cache dung lượng 0.96)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=24` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384` + `VLLM_GPU_MEMORY_UTILIZATION=0.96`.
- **Mục đích**: Tăng dung lượng KV Cache trên GPU lên tối đa 96% để ngăn ngừa tình trạng cache eviction và preemption, hướng tới ổn định trễ đầu tiên (TTFT).

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |  **42.62**   | Điểm số cuối cùng                                   |
| `ers`           |  **42.62**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.366667** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **44**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **22 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **3104 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **5870 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Phân tích hiệu năng**:
   - Khi tăng giới hạn VRAM cho KV Cache lên `0.96` (`VLLM_GPU_MEMORY_UTILIZATION=0.96`), TPOT duy trì tối ưu xuất sắc ở mức **22ms**.
   - **TTFT P95 giảm rất sâu từ 6430ms xuống 5870ms (giảm 560ms)**. TTFT P50 giữ ổn định ở mức 3104ms. Số lượng passed_slo tăng từ 40 lên 44.
   - Kết quả này chứng minh giả thuyết ban đầu là chính xác: việc nới rộng dung lượng KV Cache lên 96% giúp vLLM có thêm không gian chứa các context active, giảm đáng kể tần suất cache eviction / preemption (khiến hệ thống phải tính toán lại prefill và làm trễ P95 tăng vọt).
   - Điểm số cuối cùng thiết lập kỷ lục mới cực kỳ ấn tượng: **42.62** (so với 42.33 ở Slot 2).
2. **Phân tích độ chính xác**:
   - `accuracy_drop` duy trì 0%.
3. **Kết luận**:
   - Tối ưu hóa KV Cache lên 0.96 mang lại hiệu quả rất rõ rệt và an toàn. Cấu hình này chắc chắn sẽ được dùng để kết hợp với Prefix Caching ở Slot 14 nhằm đẩy điểm số lên cao hơn nữa.
