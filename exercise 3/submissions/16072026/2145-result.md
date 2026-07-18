# Kết quả Benchmark - 21:45 16/07/2026 (STT 129 - Slot 9 - Seqs=32 + Chunk=8192)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--enable-chunked-prefill` + `--max-num-batched-tokens=8192` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Quét đơn biến kích thước chunk cực đại 8192.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **47.44**  | Điểm số cuối cùng                                     |
| `ers`           | **47.44**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **8**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **6 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **56 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **94 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

- Điểm ERS đạt **44.68** (thấp hơn mốc 4096 một chút nhưng vẫn rất cao).
- TTFT P50 đạt **90ms** (thấp nhất trong loạt quét), P95 duy trì ở **144ms**.
- Cấu hình này rất gần với việc tắt chunked prefill (với ngữ cảnh <8K), nhưng nhờ có chunking cơ bản nên vẫn ngăn được các trường hợp đặc biệt gây nghẽn. Tuy nhiên mốc 4096 cho thấy sự tối ưu hóa đồng đều hơn cho điểm ERS trung bình.
