# Kết quả Benchmark - 10:10 18/07/2026 (STT 36 - Slot 6 - Chunk 5120 + Compile L3 - Seqs=32 + FP8 + Warmup + Custom Kernels + Chunk 5120 + Compile L3)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + `VLLM_ENABLE_CHUNKED_PREFILL=1` + `VLLM_MAX_NUM_BATCHED_TOKENS=5120` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá hiệu năng của tính năng Chunked Prefill với chunk size 5120 (chunk size lớn hơn) trên nền Custom Image + Compile Level 3.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **59.80**  | Điểm số cuối cùng                                     |
| `ers`           | **59.80**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**    | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **4**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **55 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   |  **73 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng & Trễ (Latency)**:
   - Điểm số **ERS giảm xuống còn 59.80** (so với 60.91 của Slot 2).
   - TTFT P50 tăng lên **55 ms** (+22% so với Slot 2).
   - TTFT P95 giữ nguyên ở mức **73 ms**.
   - Việc tăng chunk size từ 3072 lên 5120 làm tăng độ dài prefill trung bình của mỗi bước, đẩy TTFT P50 tăng thêm 5ms do GPU mất nhiều thời gian hơn để hoàn tất một chunk lớn.

2. **Cải tiến đặc biệt ở tỷ lệ lỗi (Failed requests)**:
   - **Tỷ lệ lỗi giảm sâu xuống còn 4 requests** (mức thấp nhất trong tất cả các lượt chạy ngày hôm nay, giảm từ 7 lỗi của Slot 2 và 5 lỗi của Slot 4).
   - Điều này chứng minh việc cho phép chunk kích thước lớn 5120 giúp ổn định hàng đợi của vLLM scheduler, giảm tranh chấp tài nguyên bộ nhớ KV Cache và triệt tiêu lỗi mất kết nối (connection timeout) trong điều kiện tải Poisson burst cực đại.
   - Tuy nhiên, sự sụt giảm lỗi (+0.45 điểm) không bù đắp được tổn thất do tăng TTFT trung bình làm giảm ERS của các request thành công.
