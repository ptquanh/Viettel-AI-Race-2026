# Kết quả Benchmark - 22:09 16/07/2026 (STT 134 - Slot 14 - Seqs=32 + MaxLen=8192)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--max-model-len=8192` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Hạ cực hạn context tối đa về 8K (giới hạn đủ đáp ứng trace benchmark).

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **43.62**  | Điểm số cuối cùng                                     |
| `ers`           | **43.62**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **5 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **97 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **151 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

- Điểm ERS cải thiện lên **43.62** (+0.54 so với mốc 32K).
- TTFT P50 đạt **97ms**, P95 đạt **151ms**.
- Việc giảm max-model-len xuống 8K giúp giảm tải bộ nhớ cho KV Cache block manager đáng kể, qua đó giảm nhẹ trễ lập lịch và cải thiện TTFT. Đây là phương án tối ưu tốt để kết hợp cùng các phương án khác.
