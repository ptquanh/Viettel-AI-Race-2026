# Kết quả Benchmark - 14:51 15/07/2026 (STT 115 - GPU Mem 0.96 + Prefix Caching)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=24` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384` + `VLLM_GPU_MEMORY_UTILIZATION=0.96` + `VLLM_ENABLE_PREFIX_CACHING=1`.
- **Mục đích**: Kết hợp tối ưu hóa KV Cache dung lượng tối đa (0.96) và Prefix Caching nhằm tận dụng cộng hưởng hiệu năng của cả 2 cải tiến.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |  **42.47**   | Điểm số cuối cùng                                   |
| `ers`           |  **42.47**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.141667** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **17**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **22 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **3312 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **6165 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Phân tích hiệu năng**:
   - Khi kết hợp cả 2 cấu hình, TPOT vẫn giữ vững xuất sắc ở mức **22ms**.
   - Tuy nhiên, **passed_slo sụt giảm mạnh về 17/120** (so với 44 của Slot 12 và 50 của Slot 10). Điểm số cuối cùng đạt 42.47, thấp hơn Slot 12 (42.62) nhưng vẫn cao hơn mức baseline OMP=4 (42.33).
   - TTFT P50 tăng lên 3312ms và P95 tăng lên 6165ms.
   - Nguyên nhân của sự sụt giảm thông lượng này là do tranh chấp và overhead tăng cao. Việc vừa đẩy GPU memory utilization lên mức cực hạn (96%) vừa kích hoạt Prefix Caching (vốn cần bộ nhớ VRAM để duy trì bảng băm ánh xạ block và siêu dữ liệu) làm giảm không gian VRAM hoạt động của engine, dẫn đến phân mảnh bộ nhớ (memory fragmentation) hoặc kích hoạt cơ chế dọn dẹp cache thường xuyên hơn. Sự cộng hưởng này phản tác dụng, làm chậm scheduler.
2. **Phân tích độ chính xác**:
   - `accuracy_drop` duy trì 0%.
3. **Kết luận**:
   - Sự kết hợp đồng thời KV Cache 0.96 và Prefix Caching không đem lại hiệu năng cộng hưởng tốt. Baseline tối ưu nhất của chúng ta vẫn là **Slot 12 (KV Cache 0.96 độc lập)** đạt **42.62 điểm**.
