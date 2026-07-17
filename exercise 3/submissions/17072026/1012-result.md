# Kết quả Benchmark - 10:12 17/07/2026 (STT 19 - Slot 4 - Seqs=32 + FP8 + OMP=2 + Chunk=4096)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096`.
- **Mục đích**: Đánh giá hiệu năng kết hợp của 2 nhân tố mạnh nhất (OMP=2 và Chunk=4096) trên nền FP8.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **56.79**  | Điểm số cuối cùng                                     |
| `ers`           | **56.79**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **73 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   |  **93 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Kỷ lục mới ấn tượng**:
   - Điểm số **ERS đạt kỷ lục mới 56.79 điểm** (+1.75 điểm so với Golden Baseline 55.04).
   - Lần đầu tiên trong bài thi, **trễ TTFT P95 phá vỡ hoàn toàn mốc 100ms để chạm xuống 93ms**!
   - TTFT P50 cũng đạt mốc tốt nhất từ trước đến nay là **73ms**.

2. **Bài học rút ra**:
   - **Hiệu ứng cộng dồn cực kỳ rõ rệt**: Sự kết hợp giữa tối ưu hóa lập lịch CPU (`OMP_NUM_THREADS=2` để giảm context switching) và tối ưu hóa xen kẽ prefill/decode (`Chunk=4096` để giải quyết nghẽn prefill chèn ngang) đã cộng hưởng hoàn hảo trên GPU FP8.
   - Nhờ đó, cả TTFT trung bình (P50) và TTFT ở các điểm bùng phát Poisson burst (P95) đều được giảm thiểu tối đa, tạo nên hiệu năng cực kỳ ấn tượng.
   - Kết quả này là cơ sở vững chắc tin rằng cấu hình Ultimate (kết hợp thêm MaxLen=8K hoặc các cấu hình KV Cache FP8 nâng cao ở nhóm sau) sẽ tiếp tục đẩy điểm số lên mốc 58-60+.
