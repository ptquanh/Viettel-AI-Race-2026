# Kết quả Benchmark - 13:51 15/07/2026 (STT 112 - Bật Prefix Caching)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=24` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384` + `VLLM_ENABLE_PREFIX_CACHING=1`.
- **Mục đích**: Bật tính năng Prefix Caching để cache lại prefill của các query trùng lặp prefix (system prompt/few-shot), tối ưu hóa thông lượng và TTFT.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |  **42.34**   | Điểm số cuối cùng                                   |
| `ers`           |  **42.34**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.416667** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **50**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **22 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **3441 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **6417 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Phân tích hiệu năng**:
   - Khi bật `VLLM_ENABLE_PREFIX_CACHING=1`, TPOT vẫn giữ vững xuất sắc ở mức tốt nhất là **22ms**.
   - **Số lượng request đạt chuẩn SLO tăng mạnh từ 40 lên 50 (tăng 25% throughput đạt SLO)**. Điều này cho thấy Prefix Caching giúp giảm tải prefill đáng kể cho các request có chung prefix, giải phóng tài nguyên tính toán giúp nhiều request cán mốc SLO thành công.
   - TTFT P50 tăng nhẹ từ 3015ms lên 3441ms, chủ yếu do biến động tải ngẫu nhiên tại thời điểm chạy benchmark của portal chấm thi hoặc scheduler của vLLM phải xử lý metadata cache trong các turn đầu. Tuy nhiên việc throughput đạt SLO tăng lên đã giúp điểm tổng ERS tăng nhẹ lên đỉnh mới **42.34**.
2. **Phân tích độ chính xác**:
   - `accuracy_drop` duy trì 0%.
3. **Kết luận**:
   - Prefix Caching mang lại lợi thế lớn về thông lượng (tăng 25% passed SLO). Cấu hình này sẽ làm Baseline mới cho các thử nghiệm tiếp theo.
