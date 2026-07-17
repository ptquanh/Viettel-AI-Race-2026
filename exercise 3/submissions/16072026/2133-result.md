# Kết quả Benchmark - 21:33 16/07/2026 (STT 128 - Slot 8 - Seqs=32 + Chunk=4096)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Quét đơn biến kích thước chunk 4096.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **45.08**  | Điểm số cuối cùng                                     |
| `ers`           | **45.08**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **5 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **91 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **142 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

- Điểm ERS **đạt đỉnh mới trong loạt quét Chunk**: **45.08 điểm**.
- TTFT P50 giảm sâu về **91ms**, TTFT P95 duy trì ở mức thấp **142ms**.
- Kích thước chunk 4096 là điểm ngọt (sweet spot) hoàn hảo cho context length của trace chấm điểm. Nó hạn chế tối đa số lượng chunk của turn 0 (hầu hết request turn 0 chỉ cần 1-2 chunks), giảm tải tối đa CPU scheduler trong khi vẫn ngăn được việc GPU bị độc chiếm quá lâu bởi prefill.
