# Kết quả Benchmark - 21:47 16/07/2026 (STT 131 - Slot 11 - Seqs=32 + OMP=3)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=3` + `--enable-prefix-caching` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Thiết lập số luồng CPU bằng chính xác số core vật lý (3 cores).

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **43.96**  | Điểm số cuối cùng                                     |
| `ers`           | **43.96**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **5 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **96 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **145 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

- Điểm ERS là **43.96**, tốt hơn mốc OMP=4 mặc định (43.08) nhưng lại kém một chút so với mốc OMP=2 (44.54).
- TTFT P50 đạt **96ms**, P95 đạt **145ms**. 
- Kết quả cho thấy đối với LFM2.5, đặt `OMP_NUM_THREADS=2` là điểm tối ưu hơn cả để phục vụ tác vụ serving đơn luồng chính của vLLM Python, nhường 1 core CPU còn lại cho các tiến trình hệ thống và xử lý IO mạng của container.
