# Kết quả Benchmark - 17:24 16/07/2026 (STT 122 - Slot 3 - Seqs=24)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=24` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Kiểm tra xem việc hạ concurrency xuống 24 có giúp giảm tải CPU, từ đó cải thiện TPOT và tăng điểm số hay không.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **42.46**  | Điểm số cuối cùng                                     |
| `ers`           | **42.46**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **5 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **102 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **153 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Nhận xét điểm số**:
   - Điểm số **giảm** từ 43.08 (ở Seqs=32) xuống **42.46** (-0.62 điểm).
   - TTFT P50 giữ nguyên **102ms** (giảm 1ms), TTFT P95 giảm xuống **153ms** (giảm 5ms) do concurrency thấp giúp tăng nhẹ tốc độ xử lý hàng đợi song song.
   - Tuy nhiên, TPOT Median vẫn kẹt cứng ở **5ms**. Việc điểm tổng bị sụt giảm dù TTFT tốt hơn chứng tỏ việc hạ concurrency xuống 24 khiến hàng đợi bị ứ đọng nhiều hơn ở các phase Poisson burst cực đại, làm tăng trung bình TTFT của toàn bộ request (không được thể hiện rõ ở P50/P95).

2. **Bài học rút ra**:
   - TPOT Median vẫn ở mức 5ms cho thấy CPU scheduler của vLLM chưa thực sự được giải phóng ở mốc Seqs=24.
   - Chúng ta cần chờ đợi kết quả của **Slot 4 (Seqs=16)** để xem liệu mức concurrency cực thấp này có thể kéo TPOT xuống mức 2-3ms hay không. Nếu có, điểm số sẽ bứt phá. Nếu không, cổ chai 5ms TPOT là giới hạn cứng của CPU serving trên MiG H200 này và chúng ta cần chuyển hướng sang tối ưu hóa lập lịch (Phase 3).
