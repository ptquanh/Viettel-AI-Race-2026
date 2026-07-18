# Kết quả Benchmark - 10:08 18/07/2026 (STT 35 - Slot 5 - Chunk 3072 + Compile L3 - Seqs=32 + FP8 + Warmup + Custom Kernels + Chunk 3072 + Compile L3)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + `VLLM_ENABLE_CHUNKED_PREFILL=1` + `VLLM_MAX_NUM_BATCHED_TOKENS=3072` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá hiệu năng của tính năng Chunked Prefill với chunk size 3072 (tối ưu hóa độ dài prefill) trên nền Custom Image + Compile Level 3.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **60.31**  | Điểm số cuối cùng                                     |
| `ers`           | **60.31**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**    | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **50 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   |  **73 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng so với Baseline không Chunked Prefill (Slot 2)**:
   - Điểm số **ERS giảm nhẹ từ 60.91 xuống còn 60.31** (-0.60 điểm).
   - TTFT P50 tăng từ 45ms lên **50ms** (+11%).
   - TTFT P95 tăng từ 70ms lên **73ms** (+4%).
   - Kết quả này cho thấy Chunked Prefill ở chunk size 3072 tạo ra overhead lập lịch bổ sung (chunking overhead) làm chậm thời gian phản hồi TTFT trung bình (P50) mà không mang lại cải tiến đáng kể ở TTFT đuôi (P95) trên nền LFM2.5.
