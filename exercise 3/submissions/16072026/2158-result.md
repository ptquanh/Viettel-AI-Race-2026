# Kết quả Benchmark - 21:58 16/07/2026 (STT 132 - Slot 12 - Seqs=32 + OMP=5)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=5` + `--enable-prefix-caching` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Thử nghiệm hyperthreading (vượt quá số core vật lý 3).

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **47.67**  | Điểm số cuối cùng                                     |
| `ers`           | **47.67**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **6 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **56 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **93 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

- Điểm ERS giảm về **43.53** (thấp hơn nhiều so với OMP=2/3).
- TTFT P95 tăng lên **156ms** (so với 144ms ở OMP=2).
- Việc vượt quá số core vật lý (OMP=5 trên 3 cores) gây nghẽn nghiêm trọng cho CPU do context switching liên tục giữa các luồng OpenMP tính toán, làm trễ quá trình lập lịch của vLLM.
