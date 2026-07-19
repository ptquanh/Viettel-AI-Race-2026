# Kết quả Benchmark - 07:50 19/07/2026 (STT 47 - Slot 2 - Seqs=24 + MaxLen=32K)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=24` + `--max-model-len=32768` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}`.
- **Mục đích**: Đánh giá hiệu năng khi giảm concurrency (Seqs) về 24 trên nền độ dài tối ưu 32K.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **58.67** | Điểm số cuối cùng                                     |
| `ers`           | **58.67** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **5**   | Số lượng request thất bại (Giảm từ 7 xuống 5)         |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **58 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **84 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **So sánh với Seqs=32 (Slot 32: 60.91đ)**:
   - Giảm Seqs xuống 24 giúp giảm số request bị lỗi từ 7 xuống còn **5 requests**.
   - Tuy nhiên, trễ TTFT P50 bị tăng từ 45ms lên **58ms** và P95 tăng từ 70ms lên **84ms** do hàng đợi vLLM bị thu hẹp lại khi có Poisson burst.
   - TPOT vẫn giữ nguyên mức kỷ lục **4ms**.

2. **Bài học rút ra**:
   - Mốc **Seqs=32** vẫn mang lại hiệu năng ERS cao nhất (60.91đ vs 58.67đ).
   - **Xác nhận Best Seqs = 32** cho các thử nghiệm tiếp theo.
