# Kết quả Benchmark - 10:59 19/07/2026 (STT 49 - Slot 4 - Marlin INT4 Quantization)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `--max-model-len=32768` + `--quantization=marlin` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--compilation-config={"level":3}`.
- **Mục đích**: Đánh giá hiệu năng Marlin INT4 Quantization Kernel online trên nền cấu hình tối ưu (Seqs=32, Len=32K, Compile L3).

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **59.81** | Điểm số cuối cùng                                     |
| `ers`           | **59.81** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **6**   | Số lượng request thất bại (Giảm từ 7 xuống 6)         |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **51 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **80 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **So sánh với FP8 Native (Slot 32: 60.91đ)**:
   - Marlin INT4 chạy rất mượt và ổn định (**59.81 điểm**), giảm số request lỗi từ 7 xuống còn **6 requests**.
   - Tuy nhiên, trễ dequantization on-the-fly (INT4 $\rightarrow$ FP16/FP8) làm tăng nhẹ TTFT P50 từ 45ms lên **51ms** (+6ms) và P95 từ 70ms lên **80ms** (+10ms).
   - TPOT vẫn ở mốc 4ms do mô hình 1.2B quá nhẹ, chưa khai thác được ưu thế băng thông của W4A16 vượt trội hơn Tensor Cores FP8 Native.

2. **Bài học rút ra**:
   - Marlin INT4 là phương án lượng tử hóa INT4 xuất sắc, giữ nguyên accuracy (0% drop) và điểm số chạm sát 60đ.
   - Đối với LFM2.5-1.2B, FP8 Native vẫn giữ lợi thế nhỉnh hơn (+1.1 điểm) nhờ phần cứng FP8 Tensor Cores trực tiếp của H200.
