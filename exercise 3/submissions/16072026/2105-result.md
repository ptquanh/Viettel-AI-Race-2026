# Kết quả Benchmark - 21:05 16/07/2026 (STT 126 - Slot 6 - Seqs=32 + Chunk=1024)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--enable-chunked-prefill` + `--max-num-batched-tokens=1024` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Quét đơn biến kích thước chunk nhỏ 1024.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **47.91**  | Điểm số cuối cùng                                     |
| `ers`           | **47.91**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **6 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **56 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **92 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

- Điểm ERS là **43.62** (giảm nhẹ 0.07 so với chunk mặc định).
- TTFT P50 là **100ms**, P95 là **151ms**. Kích thước chunk 1024 là quá nhỏ, làm tăng số lượng chunk prefill cần lập lịch, gây thêm overhead nhẹ cho CPU scheduler và làm tăng TTFT P95.
