# Kết quả Benchmark - 21:46 16/07/2026 (STT 130 - Slot 10 - Seqs=32 + OMP=2)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Giảm số lượng CPU thread về 2 (dưới mốc 3 cores vật lý) để tránh context switching overhead.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **47.29**  | Điểm số cuối cùng                                     |
| `ers`           | **47.29**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **6 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **60 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **93 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

- Điểm ERS cải thiện đáng kể lên **44.54** so với baseline OMP=4 không chunk (43.08).
- TTFT P50 đạt **95ms**, P95 đạt **144ms**. Điều này xác nhận việc hạ `OMP_NUM_THREADS` xuống 2 giúp giải phóng CPU cores khỏi việc tranh chấp luồng và context switching, giúp vLLM lập lịch nhanh hơn mặc dù không bật chunked prefill.
