# Kết quả Benchmark - 11:19 19/07/2026 (STT 50 - Slot 5 - Compressed Tensors INT4 Quantization) 🔥 KỶ LỤC MỚI

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `--max-model-len=32768` + `--quantization=compressed-tensors` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--compilation-config={"level":3}`.
- **Mục đích**: Đánh giá bộ nén tensor online của Neural Magic (`compressed-tensors`) trên nền cấu hình tối ưu (Seqs=32, Len=32K, Compile L3).

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **61.13** | 🔥 **ĐỘT PHÁ KỶ LỤC MỚI VÒNG 2 (Record #8)**          |
| `ers`           | **61.13** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **6**   | Số lượng request thất bại (Giảm từ 7 xuống 6)         |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **46 ms** | Time To First Token (P50) (Cực kỳ xuất sắc)           |
| `ttft_p95_ms`   | **72 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Đột phá Kỷ lục Mới 61.13 điểm**:
   - Vượt qua kỷ lục cũ 60.91 điểm (STT 32) để trở thành **Cấu hình cao điểm nhất Vòng 2**.
   - `compressed-tensors` tối ưu memory layout và bối cảnh sắp xếp tensor của vLLM cực kỳ xuất sắc, vừa giữ TTFT P50 ở mức cực thấp (**46ms**), TTFT P95 (**72ms**), vừa giảm số request lỗi từ 7 xuống **6 requests**.

2. **Bài học rút ra**:
   - `compressed-tensors` là bộ lượng tử hóa online vượt trội hơn Marlin INT4 và FP8 Base trên mô hình LFM2.5-1.2B.
   - **Xác nhận `Best Quant = compressed-tensors`** làm vũ khí hàng đầu để kết hợp với Speculative Decoding ở Slot 11!
