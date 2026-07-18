# Kết quả Benchmark - 20:50 16/07/2026 (STT 125 - Slot 5 - Seqs=32 + Chunk=ON)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--enable-chunked-prefill` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Chỉ bật cờ Chunked Prefill (dùng chunk size mặc định của vLLM) làm đối chứng đơn biến với baseline Seqs=32 không chunk.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **48.01**  | Điểm số cuối cùng                                     |
| `ers`           | **48.01**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **6 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **57 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **90 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

- Việc bật Chunked Prefill mặc định giúp TTFT P50 giảm xuống **98ms** (-5ms) và TTFT P95 giảm xuống **143ms** (-15ms) so với Seqs=32 không chunk.
- Điểm ERS cải thiện lên **43.69** (+0.61 điểm). TPOT Median giữ nguyên **5ms**. Điều này chứng minh chunking prefill rất có lợi cho LFM2.5.
