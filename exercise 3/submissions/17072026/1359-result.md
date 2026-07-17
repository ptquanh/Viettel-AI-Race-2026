# Kết quả Benchmark - 13:59 17/07/2026 (STT 24 - Slot 9 - Seqs=32 + FP8 + OMP=2 + Chunk=2048 + VRAM 98%)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=2048` + `--gpu-memory-utilization=0.98`.
- **Mục đích**: Kiểm tra xem việc tăng dung lượng VRAM cấp phát cho KV cache lên 98% có giúp ích gì cho nhánh Chunk=2048 (Slot 7) hay không.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **55.03**  | Điểm số cuối cùng                                     |
| `ers`           | **55.03**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **80 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **114 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng tiếp tục suy giảm so với VRAM 95% (Slot 7)**:
   - Điểm số **ERS đạt 55.03 điểm** (thấp hơn so với **55.44 điểm** của Slot 7).
   - TTFT P50 tăng nhẹ lên **80ms** (so với 78ms của Slot 7).
   - TTFT P95 giữ nguyên mức chậm trễ quanh **114ms - 118ms**.

2. **Bài học rút ra**:
   - Kết quả này nhất quán hoàn hảo với Slot 8: Việc đẩy VRAM lên `0.98` không những không giúp ích mà còn làm suy giảm nhẹ hiệu năng trên cả hai nhánh Chunk size (2048 và 4096).
   - Rõ ràng ở mốc 95% VRAM, vLLM đã có đủ số lượng block KV cache cần thiết cho 32 requests đồng thời (Seqs=32) mà không bị swap, nên việc tăng lên 98% chỉ mang lại overhead quản lý mà không đem lại giá trị thực tế nào.
