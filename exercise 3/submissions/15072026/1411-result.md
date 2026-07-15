# Kết quả Benchmark - 14:11 15/07/2026 (STT 113 - Tinh chỉnh Chunk Size = 8192)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `VLLM_MAX_NUM_SEQS=24` + `OMP_NUM_THREADS=4` + `VLLM_MAX_NUM_BATCHED_TOKENS=8192`.
- **Mục đích**: Đổi chunk size của chunked prefill về 8192 (kết hợp OMP=4) xem có giảm TTFT P50 so với việc dùng Chunk=16384 hay không.

## Chỉ số đo được

| Chỉ số          |   Giá trị   | Ý nghĩa                                             |
| :-------------- | :---------: | :-------------------------------------------------- |
| `final_score`   |  **41.01**  | Điểm số cuối cùng                                   |
| `ers`           |  **41.01**  | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           |  **0.35**   | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**    | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |   **42**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**   | Tổng số request benchmark                           |
| `failed_count`  |    **0**    | Số lượng request thất bại                           |
| `warmup_count`  |    **0**    | Số lượng request warmup                             |
| `accuracy_drop` |   **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **22 ms**  | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **3260 ms** | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **6242 ms** | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Phân tích hiệu năng**:
   - Khi hạ `VLLM_MAX_NUM_BATCHED_TOKENS` xuống 8192, TPOT duy trì tốt ở mức tối ưu là **22ms**.
   - Tuy nhiên, **TTFT P50 bị tăng từ 3015ms lên 3260ms** (tệ hơn Slot 2 Chunk 16384). Số lượng passed_slo cũng giảm xuống còn 42 (so với 50 ở Slot 10 và 40 ở Slot 2).
   - Nguyên nhân là do chunk size nhỏ hơn làm tăng số lượng chunk prefill cần lập lịch, qua đó làm gia tăng CPU scheduling overhead trên 3 cores CPU vật lý của Grader, gián tiếp làm TTFT P50 bị chậm lại.
   - Điểm số cuối cùng đạt 41.01, thấp hơn so với cả Slot 2 (42.33) và Slot 10 (42.34).
2. **Phân tích độ chính xác**:
   - `accuracy_drop` duy trì 0%.
3. **Kết luận**:
   - Khẳng định `Chunk Size = 16384` là lựa chọn tối ưu hơn hẳn `8192` cho vLLM khi chạy trên môi trường benchmark này nhờ giảm tải tối đa cho CPU Scheduler.
