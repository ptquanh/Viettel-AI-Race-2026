# Kết quả Benchmark - 15:06 17/07/2026 (STT 26 - Slot 11 - Seqs=32 + FP8 + OMP=2 + Chunk=4096 + VRAM 98% + KV Cache FP8)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096` + `--gpu-memory-utilization=0.98` + `--kv-cache-dtype=fp8`.
- **Mục đích**: Đánh giá hiệu năng khi kết hợp toàn bộ các nhân tố (OMP=2 + Chunk=4096 + VRAM 98% + KV Cache FP8).

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **55.91**  | Điểm số cuối cùng                                     |
| `ers`           | **55.91**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **76 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **114 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng bị giới hạn bởi nút thắt cổ chai VRAM 98%**:
   - Điểm số **ERS đạt 55.91 điểm** và TTFT P95 **114ms**, tương đương với mốc **55.94 điểm / 113ms** của Slot 8 (chỉ có VRAM 98% không có KV Cache FP8).
   - Sự cải thiện của KV Cache FP8 bị triệt tiêu hoàn toàn bởi overhead phát sinh từ việc đặt giới hạn bộ nhớ cực cận `0.98`.

2. **Bài học rút ra**:
   - Xác nhận thêm một lần nữa: Không nên sử dụng cờ `--gpu-memory-utilization=0.98` trong bất kỳ cấu hình tối ưu cuối cùng nào.
