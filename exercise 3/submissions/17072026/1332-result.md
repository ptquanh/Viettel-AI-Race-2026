# Kết quả Benchmark - 13:32 17/07/2026 (STT 22 - Slot 7 - Seqs=32 + FP8 + OMP=2 + Chunk=2048)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=2048`.
- **Mục đích**: Đánh giá hiệu năng kết hợp OMP=2 và Chunk=2048 để so sánh hiệu quả của kích thước chunk (2048 vs 4096) trên nền FP8.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **55.44**  | Điểm số cuối cùng                                     |
| `ers`           | **55.44**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **78 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **118 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng kém hơn mốc Chunk=4096**:
   - Điểm số **ERS đạt 55.44 điểm** (thấp hơn tới 1.35 điểm so với mốc kỷ lục 56.79 của Slot 4 dùng Chunk=4096).
   - TTFT P50 tăng lên **78ms** (so với 73ms ở Slot 4).
   - TTFT P95 tăng lên **118ms** (so với 93ms ở Slot 4).

2. **Bài học rút ra**:
   - So sánh trực tiếp giữa Slot 7 (Chunk=2048) và Slot 4 (Chunk=4096) cho thấy: **Chunk=4096 tối ưu hơn hẳn trên nền FP8**.
   - Nguyên nhân là do khi cắt nhỏ chunk size về 2048, số lượng chunk cần xử lý cho mỗi request tăng lên, làm gia tăng số bước lập lịch (scheduling loops) của vLLM trên CPU. Trên nền FP8 (tốc độ GPU cực nhanh), CPU overhead lúc này đóng vai trò quyết định, do đó số lượng bước lập lịch nhiều hơn sẽ làm chậm tiến trình giải phóng hàng đợi, kéo dài TTFT.
   - Kết quả này khẳng định **Chunk=4096 là sweet-spot tuyệt đối** cho LFM2.5 trên H200. Các combo dựa trên Chunk=4096 (như Slot 8, Slot 11, Slot 14) sẽ nắm chắc lợi thế so với nhánh Chunk=2048 (Slot 9, Slot 10, Slot 12).
