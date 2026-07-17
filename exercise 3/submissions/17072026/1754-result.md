# Kết quả Benchmark - 17:54 17/07/2026 (STT 27 - Slot 12 - Seqs=32 + FP8 + OMP=2 + Chunk=2048 + VRAM 98% + KV Cache FP8)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=2048` + `--gpu-memory-utilization=0.98` + `--kv-cache-dtype=fp8`.
- **Mục đích**: Đánh giá hiệu năng kết hợp lượng tử hóa KV Cache FP8 với nhánh Chunk=2048 trên nền VRAM 98%.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **55.40**  | Điểm số cuối cùng                                     |
| `ers`           | **55.40**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **79 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **119 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng tăng nhẹ nhờ KV Cache FP8 so với Slot 9**:
   - Điểm số **ERS đạt 55.40 điểm** (tăng 0.37 điểm so với **55.03 điểm** của Slot 9).
   - Tuy nhiên, trễ TTFT P95 vẫn ở mức cao (**119ms**), khẳng định cấu hình này không tối ưu bằng nhánh Chunk=4096.

2. **Bài học rút ra**:
   - Lượng tử hóa KV Cache FP8 liên tục mang lại cải tiến hiệu năng nhỏ nhưng ổn định, củng cố thêm niềm tin vào khả năng tạo đột phá của Slot 14 sắp tới.
