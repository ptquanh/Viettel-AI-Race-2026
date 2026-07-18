# Kết quả Benchmark - 13:26 18/07/2026 (STT 40 - Slot 10 - Spec N-gram 3-2 + Compile L3 - Seqs=32 + FP8 + Warmup + Custom Kernels + Spec N-gram 3-2 + Compile L3)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + `--speculative-model=[ngram]` + `--ngram-prompt-lookup-max=3` + `--num-speculative-tokens=2` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá speculative decoding mức rất nhẹ (N-gram 3-2) trên nền Custom Image + Compile Level 3.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **60.46** | Điểm số cuối cùng                                     |
| `ers`           | **60.46** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **5**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **51 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **72 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng so với các cấu hình Speculative khác**:
   - Điểm số **ERS tăng từ 59.80 (Slot 8) và 60.00 (Slot 9) lên 60.46** (+0.66 và +0.46 điểm).
   - TTFT P50 giữ nguyên ở mức **51 ms**, nhưng TTFT P95 cải thiện vượt trội về **72 ms** (-10ms so với Slot 8).
   - Số request thất bại giảm từ 6 xuống còn **5 requests**.

2. **Bài học rút ra**:
   - Cấu hình N-gram 3-2 là mức speculative decoding nhẹ nhất, giúp hạn chế tối đa khối lượng tính toán sinh draft tokens và xác thực logits trên CPU. Điều này làm giảm đáng kể trễ đuôi (TTFT P95) và số lượng kết nối bị timeout (failed_count).
   - Tuy nhiên, trễ TTFT P50 vẫn bị kẹt cứng ở mức **51 ms** (tệ hơn Slot 2 là 45ms) do overhead cố định của hệ thống lập lịch vLLM để tích hợp speculative logic vào đồ thị compile.
   - **Kết luận**: Cấu hình không Speculative (Slot 2) vẫn tối ưu hơn cả cho bài toán LFM2.5.
