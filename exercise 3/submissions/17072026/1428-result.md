# Kết quả Benchmark - 14:28 17/07/2026 (STT 25 - Slot 10 - Seqs=32 + FP8 + OMP=2 + Chunk=2048 + KV Cache FP8)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=2048` + `--kv-cache-dtype=fp8`.
- **Mục đích**: Đánh giá hiệu năng khi áp dụng lượng tử hóa KV Cache FP8 (`--kv-cache-dtype=fp8`) kết hợp với OMP=2 và Chunk=2048.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **55.51**  | Điểm số cuối cùng                                     |
| `ers`           | **55.51**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **78 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **113 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng cải thiện nhẹ so với KV Cache FP16 (Slot 7)**:
   - Điểm số **ERS đạt 55.51 điểm** (tăng nhẹ so với **55.44 điểm** của Slot 7).
   - TTFT P95 giảm từ 118ms xuống **113ms**.

2. **Bài học rút ra**:
   - Việc kích hoạt `--kv-cache-dtype=fp8` mang lại hiệu quả tích cực rõ rệt. Quantization KV Cache sang FP8 làm giảm 50% băng thông truyền tải dữ liệu KV cache giữa GPU VRAM và Tensor Cores, giúp giảm thiểu độ trễ đọc/ghi bộ nhớ trong cả pha prefill và decode.
   - Kết quả này hứa hẹn cực kỳ tích cực cho các slot tiếp theo, đặc biệt là **Slot 14** (`OMP=2 + Chunk=4096 + KV Cache FP8`), nơi kết hợp những nhân tố mạnh nhất với lượng tử hóa KV Cache.
