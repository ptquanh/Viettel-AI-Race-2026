# Kết quả Benchmark - 16:05 15/07/2026 (STT 116 - Hạ Concurrency Seqs=16)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=16` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384` + `VLLM_GPU_MEMORY_UTILIZATION=0.96`.
- **Mục đích**: Hạ concurrency xuống 16 để triệt tiêu hoàn toàn nghẽn băng thông memory decode, ép TPOT xuống mức cực tiểu.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |   **51.10**  | Điểm số cuối cùng                                   |
| `ers`           |   **51.10**  | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.133333** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **16**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **16 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **4742 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **8019 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả
1. **Phân tích hiệu năng**:
   - **TPOT Median giảm kỷ lục xuống còn 16ms** (giảm 27% so với mức 22ms). Vì 16ms nằm dưới mức Floor (20ms) của BTC, nên điểm số TPOT ($s_{tpot}$) cho **tất cả các request** đạt tối đa là **1.0**.
   - Với công thức ERS: $S_{request} = 0.5 \cdot s_{ttft} + 0.5 \cdot s_{tpot}$, việc đưa $s_{tpot} = 1.0$ giúp thiết lập mức "điểm sàn" tối thiểu cho mọi request xử lý thành công là **0.50**, bất chấp trễ TTFT có vượt trần 1.5s hay không.
   - Do hạ Seqs xuống 16, hàng đợi bị dồn ứ khiến TTFT P50 tăng lên 4742ms và TTFT P95 lên 8019ms, làm passed_slo giảm còn 16. Nhưng do trần điểm sàn tăng từ `0.5 * 0.84 = 0.42` lên `0.5 * 1.0 = 0.50`, điểm số tổng ERS đã bứt phá ngoạn mục lên **51.10** (Kỷ lục tuyệt đối mới!).
2. **Phân tích độ chính xác**:
   - `accuracy_drop` duy trì 0%.
3. **Kết luận**:
   - Đây là một phát hiện toán học cực kỳ quan trọng: **Đạt TPOT <= 20ms giúp nâng điểm sàn ERS của mọi request lên 0.5**.
   - Mục tiêu tiếp theo là tìm điểm ngọt concurrency (Seqs) nằm giữa 16 và 24 (ví dụ Seqs=20 hoặc 21) để vừa duy trì được TPOT <= 20ms (để ăn trọn điểm sàn 0.5 cho TPOT), vừa kéo giảm TTFT P50 để nâng số lượng request passed_slo lên, đẩy điểm số tiến sát mốc 60.
