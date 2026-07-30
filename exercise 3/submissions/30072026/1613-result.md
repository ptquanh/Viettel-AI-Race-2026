# Kết quả Benchmark - 16:13 30/07/2026 (STT 203 - r25-humming-mig-persistent bfloat16 fix)

- **Cấu hình**: Image `sha256:dc9e` (vLLM v0.26.0) + `--dtype=bfloat16` + `--kv-cache-dtype=fp8` + `--mamba-cache-dtype=bfloat16`.
- **Mục đích**: Fix lỗi FlashAttention-3 dtype mismatch của Slot 1532 (`float16` -> `bfloat16`) để chạy thử nghiệm engine v0.26.0 trên H200 MIG.

## Chỉ số đo được

| Chỉ số          |   Giá trị   | Ý nghĩa                                             |
| :-------------- | :---------: | :-------------------------------------------------- |
| `final_score`   | **66.5100** | Điểm số cuối cùng                                   |
| `ers`           |  **66.51**  | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           |    **1**    | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**    | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |   **415**   | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **420**   | Tổng số request benchmark                           |
| `failed_count`  |    **5**    | Số lượng request thất bại                           |
| `warmup_count`  |    **0**    | Số lượng request warmup                             |
| `accuracy_drop` |   **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **3 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **46 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   |  **75 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Hiệu năng Engine v0.26.0**:
   - Fix `float16` -> `bfloat16` giúp hệ thống khởi động thành công, không bị crash FA3.
   - Kết quả đạt **66.51 ERS** (TPOT = 3ms, TTFT P50 = 46ms, P95 = 75ms).
   - Số request thất bại giảm xuống 5 (so với 6 của các cấu hình khác).
2. **So sánh với baseline 0851 (68.38 ERS)**:
   - TTFT P95 của image `sha256:dc9e` là 75ms (so với 67ms của image `sha256:2f1c`).
   - TPOT vẫn giữ ở mốc 3ms. Do đó điểm ERS đạt 66.51 (thấp hơn 0851 1.87 điểm).
3. **Kết luận**:
   - Khẳng định engine v0.26.0 chạy ổn định với `bfloat16`.
   - Để đạt 80+ ERS, cần Phase 3 (Scheduler Decode-Priority Patch) để ép TPOT từ 3ms xuống 2ms.
