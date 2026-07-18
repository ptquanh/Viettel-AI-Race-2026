# Kết quả Benchmark - 10:37 18/07/2026 (STT 39 - Slot 9 - Spec N-gram 6-5 + Compile L3 - Seqs=32 + FP8 + Warmup + Custom Kernels + Spec N-gram 6-5 + Compile L3)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + `--speculative-model=[ngram]` + `--ngram-prompt-lookup-max=6` + `--num-speculative-tokens=5` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá speculative decoding mức aggressive hơn (N-gram 6-5) trên nền Custom Image + Compile Level 3.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **60.00** | Điểm số cuối cùng                                     |
| `ers`           | **60.00** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **6**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **51 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **75 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng so với Speculative 4-3 (Slot 8)**:
   - Điểm số **ERS tăng nhẹ từ 59.80 lên 60.00** (+0.20 điểm).
   - TTFT P50 giữ nguyên ở mức **51 ms**, nhưng TTFT P95 cải thiện từ 82ms xuống còn **75 ms** (-8.5%).
   - TPOT Median vẫn giữ ở mức **4 ms**.

2. **Tại sao cấu hình Aggressive (6-5) tốt hơn Conservative (4-3)?**:
   - Khi tăng lookup window lên 6 và dự đoán tối đa 5 tokens, xác suất khớp các cụm từ lặp lại trong context tăng lên. Nhờ đó, số lượng token được sinh ra và xác nhận trong 1 bước tính toán (forward pass) tăng lên, giúp tối ưu hóa tổng thời gian sinh chuỗi và kéo giảm trễ TTFT ở phân khúc đuôi (P95).
   - Tuy nhiên, trễ TTFT P50 trung bình vẫn bị kẹt ở **51 ms** (tệ hơn Slot 2 là 45ms) do overhead khởi tạo và chạy thuật toán so khớp trên CPU của vLLM vẫn quá lớn đối với mô hình siêu nhỏ LFM2.5.
   - **Kết luận**: Speculative Decoding không phù hợp để làm baseline lâu dài cho LFM2.5 trên phần cứng 3 cores CPU.
