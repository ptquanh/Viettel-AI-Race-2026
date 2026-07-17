# Kết quả Benchmark - 18:44 17/07/2026 (STT 29 - Slot 14 - Seqs=32 + FP8 + OMP=2 + Chunk=4096 + KV Cache FP8)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096` + `--kv-cache-dtype=fp8`.
- **Mục đích**: Đánh giá hiệu năng của combo kết hợp toàn bộ các tối ưu mạnh nhất gồm OMP=2, Chunk=4096 và lượng tử hóa KV Cache FP8.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **56.22**  | Điểm số cuối cùng                                     |
| `ers`           | **56.22**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **75 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **107 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng giảm nhẹ so với mốc KV Cache FP16 (Slot 4 - 56.79)**:
   - Điểm số **ERS đạt 56.22 điểm** (thấp hơn so với mốc kỷ lục **56.79** của Slot 4).
   - TTFT P95 tăng nhẹ từ 93ms lên **107ms**.

2. **Bài học rút ra**:
   - Ở nhánh Chunk=2048 (Slot 10 vs Slot 7), lượng tử hóa KV Cache FP8 giúp tăng điểm từ 55.44 lên 55.51 do giảm tải băng thông.
   - Tuy nhiên ở nhánh Chunk=4096 (Slot 14 vs Slot 4), KV Cache FP8 lại gây tác dụng ngược (giảm từ 56.79 xuống 56.22). Lý do là khi Chunk size đạt mức tối ưu (4096), năng lực tính toán của GPU đã bão hòa rất tốt. Lúc này, overhead chuyển đổi kiểu dữ liệu (casting/quantize/dequantize) trong nhân attention của kiến trúc model lai (LFM2.5) trở thành yếu tố cản trở, làm trễ TTFT tăng từ 93ms lên 107ms.
   - Kết quả này khẳng định **Slot 4 (OMP=2 + Chunk=4096 + VRAM 95% + KV Cache FP16 mặc định) là cấu hình tối ưu tuyệt đối (Sweet-spot)**.
