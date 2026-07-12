# Kết quả Benchmark - 21:44 11/07/2026 (STT 89 - FP8 weights + Custom FP8 KV + Chunk 4096 + Warmup)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup` + `--quantization fp8` + `--kv-cache-dtype fp8` + `--enable-chunked-prefill` (hijacked) + Warmup.
- **Mục đích**: Loại bỏ TTFT 2036ms của STT 83 bằng cách JIT compile Triton kernels thông qua 1 request warmup ban đầu, kết hợp giữ TPOT 31ms.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |  **25.09**   | Điểm số cuối cùng                                   |
| `ers`           |  **25.09**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.516667** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **62**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **30 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **1903 ms** | Time To First Token (P50)                           |
| `ttft_p95_ms`   |  **2968 ms** | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Hiệu năng & So sánh**:
   - Điểm số tăng nhẹ lên **25.09** (từ 20.82 của STT 83).
   - TPOT đạt mức cực tốt là **30 ms** (tốt hơn 1ms so với STT 83).
   - TTFT P50 giảm nhẹ từ 2036ms xuống **1903 ms**. Tuy nhiên, mức giảm này là quá nhỏ so với kỳ vọng (chỉ giảm ~130ms), chứng tỏ cơ chế Warmup hiện tại chưa hoàn toàn triệt tiêu được overhead compile kernel Triton hoặc do Chunked Prefill vẫn gây nghẽn đáng kể.
2. **Độ chính xác GPQA**:
   - `accuracy_drop: 0%` xác nhận việc sử dụng custom FP8 KV Cache hoàn toàn không ảnh hưởng đến độ chính xác của model Qwen3.5-2B.
3. **Kết luận**:
   - Warmup có tác dụng nhưng chưa đủ để kéo TTFT xuống dưới ngưỡng 1s.
   - Nguyên nhân sâu xa là sự kết hợp của Chunked Prefill (4096) trên CPU 3 cores vẫn gây ra độ trễ hàng đợi lập lịch lớn. Do đó, việc chuyển đổi sang tắt Chunked Prefill và kiểm soát concurrency (đã định hình trong kế hoạch 12/07) là hoàn toàn đúng đắn.
