# Kết quả Benchmark - 08:45 17/07/2026 (STT 17 - Slot 2 - Seqs=32 + FP8 Base + Chunk=4096)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096`.
- **Mục đích**: Đánh giá hiệu quả của Chunked Prefill với chunk size 4096 trên nền FP8.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **56.53**  | Điểm số cuối cùng                                     |
| `ers`           | **56.53**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **74 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **106 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu ứng cộng hưởng cực tốt**:
   - Điểm số **ERS đạt kỷ lục mới 56.53 điểm** (+1.49 điểm so với mốc Golden Baseline 55.04).
   - TTFT P50 giảm sâu từ 79ms xuống còn **74ms** (giảm 5ms).
   - TTFT P95 giảm từ 115ms xuống còn **106ms** (giảm 9ms).

2. **Bài học rút ra**:
   - Chunked Prefill hoạt động xuất sắc trên FP8. Việc cắt nhỏ prefill thành các chunk kích thước 4096 giúp scheduler xen kẽ prefill và decode mượt mà hơn.
   - Điều này đặc biệt có lợi cho TTFT P50/P95 và điểm tổng thể, vì các request prefill mới không còn chặn hoàn toàn các token decode của các request đang chạy dở.
   - Trễ TTFT P50 giảm xuống còn 74ms là mốc tối ưu nhất ghi nhận được từ trước đến nay.
