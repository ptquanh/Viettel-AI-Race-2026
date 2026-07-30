# Kết quả Benchmark - 17:11 30/07/2026 (STT 206 - r26-humming-f16accum-fa3)

- **Cấu hình**: Image `sha256:d739` + `VLLM_HUMMING_USE_F16_ACCUM=1` + `--dtype=float16` + `--kv-cache-dtype=fp8`.
- **Mục đích**: Thử nghiệm Image mới của Teammate sử dụng FP16 accumulation cho Humming kernel kết hợp FlashAttention-3.

## Chỉ số đo được

| Chỉ số          |   Giá trị   | Ý nghĩa                                             |
| :-------------- | :---------: | :-------------------------------------------------- |
| `final_score`   | **67.3200** | Điểm số cuối cùng                                   |
| `ers`           |  **67.32**  | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           |    **1**    | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**    | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |   **415**   | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **420**   | Tổng số request benchmark                           |
| `failed_count`  |    **5**    | Số lượng request thất bại                           |
| `warmup_count`  |    **0**    | Số lượng request warmup                             |
| `accuracy_drop` |   **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **3 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **46 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   |  **66 ms**  | **KỶ LỤC TRỄ ĐUÔI MỚI!** (TTFT P95 thấp nhất giải)  |

## Phân tích kết quả

1. **Kỷ lục TTFT P95 mới (66ms)**:
   - Việc bật `VLLM_HUMMING_USE_F16_ACCUM=1` giúp tối ưu toán tử tích lũy Humming trên Tensor Cores của H200.
   - Trễ đuôi TTFT P95 giảm xuống **66ms** (vượt qua mốc 67ms của kỷ lục cũ 0851).
   - Điểm ERS đạt **67.32**, cực kỳ ấn tượng!
2. **Cơ hội kết hợp Phase 3**:
   - Nếu build Phase 3 (Decode-Priority Scheduler Patch) trên base image `sha256:d739` này:
     - Giữ nguyên trễ đuôi TTFT P95 = 66ms của image này.
     - Ép TTFT P50 từ 46ms xuống 44ms (nhờ scheduler patch).
     - **Tổng điểm ERS dự kiến sẽ vượt 70.0+ ERS!**
