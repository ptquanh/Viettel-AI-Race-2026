# Kết quả Benchmark - 08:08 19/07/2026 (STT 48 - Slot 3 - Seqs=48 + MaxLen=32K)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=48` + `--max-model-len=32768` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}`.
- **Mục đích**: Đánh giá hiệu năng khi tăng concurrency (Seqs) lên 48 trên nền độ dài tối ưu 32K.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **55.85**  | Điểm số cuối cùng                                     |
| `ers`           | **55.85**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**    | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **69 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   |  **91 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **So sánh với Seqs=32 (Slot 32: 60.91đ)**:
   - Tăng Seqs lên 48 làm gia tăng độ tranh chấp compute (compute contention) trên GPU.
   - Trễ TTFT P50 tăng vọt từ 45ms lên **69ms** (+24ms) và P95 tăng từ 70ms lên **91ms** (+21ms), kéo tổng điểm ERS giảm 5.06 điểm xuống **55.85 điểm**.
   - Số request lỗi không giảm (vẫn kẹt ở 7 failed).

2. **Bài học rút ra**:
   - `Seqs=48` quá rộng gây tranh chấp GPU execution resources, trong khi `Seqs=24` quá hẹp làm nghẽn hàng đợi vLLM.
   - **Xác nhận tuyệt đối `Best Seqs = 32`** và **`Best Len = 32768 (32K)`**.
   - Mốc baseline tối ưu nhất: **Seqs=32, Len=32K, Compile Level 3 (STT 32: 60.91 điểm)**.
