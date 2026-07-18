# Kết quả Benchmark - 21:59 16/07/2026 (STT 133 - Slot 13 - Seqs=32 + MaxLen=16384)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--max-model-len=16384` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Hạ giới hạn context tối đa về 16K.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **47.54**  | Điểm số cuối cùng                                     |
| `ers`           | **47.54**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **8**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **6 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **57 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **94 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

- Điểm ERS đạt **43.03**, không có cải thiện đáng kể so với baseline Seqs=32 mặc định 32K (43.08).
- TTFT P50 là **99ms**, P95 là **155ms**.
- Việc hạ từ 32K xuống 16K chưa đủ tác động sâu sắc đến hiệu năng của block allocator trong scheduler của vLLM.
