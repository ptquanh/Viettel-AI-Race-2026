# Kết quả Benchmark - 08:53 18/07/2026 (STT 31 - Slot 1 - Custom Image Baseline - Seqs=32 + FP8 + Warmup + Custom Kernels)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: So sánh trực tiếp hiệu năng của Custom Image (có Warmup JIT và Custom Triton Kernels) với Stock Baseline cao điểm nhất (STT 16: 58.94 điểm) chạy cùng cấu hình.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **59.51** | Điểm số cuối cùng                                     |
| `ers`           | **59.51** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **6**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **50 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **86 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Đột phá kỷ lục mới**:
   - Điểm số **ERS đạt kỷ lục mới 59.51 điểm** (+0.57 điểm so với Stock Baseline cao nhất 58.94).
   - Sự tiến bộ rõ rệt nhất nằm ở **TTFT P50 giảm sâu từ 58ms xuống còn 50ms**, chứng minh hiệu quả vượt trội của cơ chế **Warmup JIT** giúp loại bỏ độ trễ biên dịch JIT của GPU khi bắt đầu nhận tải.

2. **Bài học rút ra**:
   - Triton Custom Kernels kết hợp JIT Warmup đã mang lại cải thiện hiệu năng thực sự mà không làm suy giảm độ chính xác hoặc tăng tỷ lệ lỗi (failed count giữ nguyên ở mức 6 requests).
   - Đây là cơ sở cực kỳ vững chắc để tiếp tục thử nghiệm Nhóm G1 (bật Compile Level 2/3 trên nền Custom Image) và Nhóm G3 (Speculative Decoding) nhằm đẩy điểm số vượt mốc 60-65+.
