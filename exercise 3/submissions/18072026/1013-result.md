# Kết quả Benchmark - 10:13 18/07/2026 (STT 37 - Slot 7 - block-size 8 + Compile L3 - Seqs=32 + FP8 + Warmup + Custom Kernels + Block Size 8 + Compile L3)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + `--block-size=8` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá hiệu năng khi giảm block size của KV cache từ 16 (mặc định) xuống 8 để giảm phân mảnh bộ nhớ trên nền Custom Image + Compile Level 3.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **59.76**  | Điểm số cuối cùng                                     |
| `ers`           | **59.76**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**    | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **5**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **52 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   |  **80 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng & Trễ (Latency)**:
   - Điểm số **ERS giảm từ 60.91 xuống còn 59.76** (-1.15 điểm).
   - TTFT P50 tăng từ 45ms lên **52ms** (+15.5%).
   - TTFT P95 tăng từ 70ms lên **80ms** (+14.3%).
   - Việc giảm block size xuống 8 làm tăng gấp đôi số lượng block cần quản lý trong bộ nhớ cho cùng một lượng tokens. Điều này làm gia tăng overhead quản lý bảng ánh xạ block (block lookup table) của vLLM scheduler, đồng thời làm giảm hiệu năng tính toán của attention kernel do block size quá nhỏ, kéo TTFT tăng lên ở cả P50 và P95.

2. **Tỷ lệ lỗi (Failed requests)**:
   - Số request thất bại giảm từ 7 xuống còn **5 requests**. Việc phân chia nhỏ block size giúp quản lý bộ nhớ linh hoạt hơn, hạn chế việc bị từ chối request do phân mảnh bộ nhớ vật lý lúc cao điểm. Tuy nhiên, sự cải thiện nhỏ này không bù lại được mức tăng latency ở các request thành công.
   - **Kết luận**: Mức block size mặc định 16 vẫn là tối ưu nhất cho cấu hình phục vụ LFM2.5.
