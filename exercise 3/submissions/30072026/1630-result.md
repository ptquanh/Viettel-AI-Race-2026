# Kết quả Benchmark - 16:30 30/07/2026 (STT 204 - Phase 3 Scheduler Decode-Priority Patch)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:phase3` + `DECODE_PREFILL_CAP=128` + `--dtype=bfloat16` + `--kv-cache-dtype=fp8`.
- **Mục đích**: Kiểm tra hiệu quả của Scheduler Decode-Priority patch (Phase 3) trong việc nén TPOT & cải thiện TTFT.

## Chỉ số đo được

| Chỉ số          |   Giá trị   | Ý nghĩa                                             |
| :-------------- | :---------: | :-------------------------------------------------- |
| `final_score`   | **68.2000** | Điểm số cuối cùng                                   |
| `ers`           |  **68.20**  | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           |    **1**    | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**    | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |   **411**   | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **420**   | Tổng số request benchmark                           |
| `failed_count`  |    **9**    | Số lượng request thất bại                           |
| `warmup_count`  |    **0**    | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**   | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **3 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **44 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   |  **73 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Hiệu quả nhảy vọt của Phase 3 (+1.69 ERS)**:
   - Điểm ERS tăng từ **66.51 lên 68.20** (tiến sát kỷ lục toàn giải 68.38).
   - TTFT P50 giảm từ **46ms xuống 44ms**.
   - TTFT P95 giảm từ **75ms xuống 73ms**.
2. **Điểm nghẽn cần khắc phục**:
   - `failed_count` tăng từ 5 lên **9 request** (do cap prefill 128 hơi chật ở những turn có prefill cực lớn).
   - Nếu giảm `failed_count` về mốc 4-5 request (bằng cách chỉnh `DECODE_PREFILL_CAP` từ 128 -> 192 hoặc 256), điểm ERS dự kiến sẽ vượt **69+ ERS**!
