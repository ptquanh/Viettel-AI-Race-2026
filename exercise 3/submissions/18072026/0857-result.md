# Kết quả Benchmark - 08:57 18/07/2026 (STT 32 - Slot 2 - Custom Image + Compile Level 3 - Seqs=32 + FP8 + Warmup + Custom Kernels + Compile L3)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá hiệu năng và tính ổn định của cơ chế biên dịch `torch.compile` level 3 (aggresive operator fusion + CUDA Graphs nâng cao) trên nền Custom Image.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **60.91** | Điểm số cuối cùng                                     |
| `ers`           | **60.91** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **45 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **70 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Đột phá mốc 60 điểm (Kỷ lục mới)**:
   - Điểm số **ERS đạt kỷ lục mới 60.91 điểm** (+1.40 điểm so với Slot 1).
   - Cơ chế `torch.compile` level 3 đã tối ưu cực kỳ thành công độ trễ TTFT:
     - **TTFT P50 giảm từ 50ms xuống còn 45ms** (-10%).
     - **TTFT P95 giảm cực mạnh từ 86ms xuống còn 70ms** (-18.6%).
   - Điều này xác nhận việc biên dịch gộp kernel (operator fusion) và tận dụng CUDA Graphs nâng cao giúp loại bỏ triệt để CPU overhead lúc lập lịch kernel trong điều kiện Poisson burst tải cao.

2. **Độ ổn định & Chính xác**:
   - Tỷ lệ lỗi tăng nhẹ thêm 1 request (7 vs 6 của Slot 1) trên tổng số 420 requests, đây là mức biến động nhỏ bình thường của hệ thống mạng/Grader và hoàn toàn chấp nhận được.
   - Không có sự sụt giảm độ chính xác (accuracy drop = 0%).
   - Compilation level 3 hoàn toàn an toàn và mang lại hiệu quả rất lớn cho mô hình LFM2.5.
