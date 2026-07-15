# Kết quả Benchmark - 19:34 15/07/2026 (STT 117 - Slot 15 - Seqs=20)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=20` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384` + `VLLM_GPU_MEMORY_UTILIZATION=0.96`.
- **Mục đích**: Tăng nhẹ concurrency từ 16 lên 20 nhằm cải thiện TTFT trong khi kỳ vọng TPOT vẫn giữ $\le 20ms$ để ăn trọn điểm bảo hiểm $s_{tpot} = 1.0$.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |   **45.41**  | Điểm số cuối cùng                                   |
| `ers`           |   **45.41**  | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           |   **0.025**  | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **3**     | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **20 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **5074 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **6449 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả
1. **Phân tích hiệu năng**:
   - **TPOT Median chạm đúng biên 20ms**. Tuy nhiên, do là giá trị Median, khoảng 50% số request có $TPOT_{mean} > 20ms$ và bị tính phạt lũy thừa $\gamma = 2$ theo công thức ERS. Điều này giải thích vì sao mức điểm sàn bảo hiểm bị sụt giảm, kéo điểm tổng ERS xuống còn **45.41** (thấp hơn nhiều so với 51.10 của Seqs=16).
   - **TTFT không những không cải thiện mà còn tệ đi**: TTFT P50 tăng lên **5074ms** (so với 4742ms ở Seqs=16), dẫn đến passed_slo sụt giảm nghiêm trọng chỉ còn **3/120**. 
   - **Nguyên nhân hệ thống**: Khi chạy song song nhiều request hơn (20 so với 16) trên tài nguyên GPU MIG bị giới hạn, thời gian xử lý mỗi bước decode tăng lên (từ 16ms lên 20ms). Sự chậm trễ của bước decode làm kéo dài thời gian hoàn thành các request đang chạy, khiến các request đang xếp hàng trong queue phải chờ lâu hơn để giải phóng slot (queue clearing rate chậm đi). Do đó, tăng concurrency trong điều kiện tài nguyên bị nghẽn băng thông memory decode lại phản tác dụng, làm tăng cả TTFT lẫn TPOT.
2. **Phân tích độ chính xác**:
   - `accuracy_drop` duy trì 0%.
3. **Kết luận**:
   - Con đường tối ưu nhất vẫn là giữ `VLLM_MAX_NUM_SEQS` ở mức thấp để giải phóng băng thông decode và đẩy nhanh tốc độ dọn dẹp queue.
   - Chúng ta sẽ thử nghiệm **Slot 17 (Seqs=18)** để xem liệu đây có phải là điểm ngọt an toàn để ép TPOT Median xuống dưới hẳn 20ms (tầm 18ms) để lấy trọn điểm $s_{tpot}=1.0$ cho hầu hết request, đồng thời kiểm chứng tốc độ dọn queue của Seqs=18 so với Seqs=16.
