# Kết quả Benchmark - 14:01 11/07/2026 (STT 82 - FP8 weights + Chunked Prefill (chunk 4096) - Fixed 🔥)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--quantization fp8` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096` + `OMP_NUM_THREADS=3`
- **Mục đích**: Bản sửa lỗi cú pháp cho STT 81 (`1147`). Kết hợp weights FP8 với Chunked Prefill kích thước lớn (4096 tokens) để giảm scheduling overhead của CPU 3 cores và bảo vệ luồng decode.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |  **12.91**   | Điểm số cuối cùng                                   |
| `ers`           |  **12.91**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.708333** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **85**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0**     | Độ sụt generate sụt giảm độ chính xác               |
| `tbt_median_ms` |  **51 ms**   | Median Time Between Tokens                          |
| `ttft_p50_ms`   |  **960 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **7780 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Hiệu năng giảm mạnh so với baseline (12.91 so với 18.99 ở STT 21)**:
   - Mặc dù vẫn sử dụng FP8 weights và passed SLO vẫn là 85/120, điểm số bị kéo sụt nghiêm trọng từ 18.99 xuống 12.91.
   - Nguyên nhân chính: **TTFT P50 tăng vọt từ 569ms (STT 21) lên 960ms**. Điều này cho thấy việc chia chunk prefill quá lớn (`--max-num-batched-tokens=4096`) trên CPU 3 cores làm tăng scheduling delay/queuing delay, khiến thời gian phản hồi đầu tiên của từng request bị chậm lại đáng kể.
   - TPOT vẫn giữ nguyên ở mức **51 ms**, xác nhận chunked prefill không cứu được decode step khi dùng KV cache gốc (BF16).
2. **Độ chính xác hoàn hảo**: `accuracy_drop: 0` chứng minh FP8 weights giữ nguyên chất lượng mô hình gốc.
3. **Kết luận**: Chunked Prefill với chunk size lớn (4096) là phản tác dụng cho TTFT trên hạ tầng CPU 3 cores. Chúng ta cần chunk size nhỏ hơn (như 2048 ở `slot1`) hoặc tắt chunked prefill khi dùng FP8 weights.
