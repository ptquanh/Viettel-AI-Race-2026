# Kết quả Benchmark - 13:40 18/07/2026 (STT 41 - Slot 11 - Custom Triton Kernels = OFF + Compile L3 - Seqs=32 + FP8 + Warmup + Custom Triton Kernels = OFF + Compile L3)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + **`VLLM_CUSTOM_KERNEL=0` (TẮT TRITON KERNELS)** + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đo lường đóng góp hiệu năng độc lập (Ablation study) của Triton custom kernels (đặc biệt là các fusion kernels của recurrent layers trong mô hình LFM2.5) trên nền Compile Level 3.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **56.93** | Điểm số cuối cùng                                     |
| `ers`           | **56.93** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **64 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **88 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Tác động của Triton Custom Kernels đối với LFM2.5**:
   - Khi tắt Triton Custom Kernels (`VLLM_CUSTOM_KERNEL=0`), điểm số **sụt giảm cực mạnh từ 60.91 (Slot 2) xuống còn 56.93 (-3.98 điểm)**.
   - Trễ TTFT P50 tăng vọt từ 45ms lên **64ms (+42.2%)**.
   - Trễ TTFT P95 tăng vọt từ 70ms lên **88ms (+25.7%)**.
   - Số request thất bại giữ nguyên ở mức 7.

2. **Bài học rút ra**:
   - Đây là bằng chứng rõ ràng nhất về sự đóng góp của **Triton Custom Kernels** được tối ưu hóa riêng cho các tầng tuần hoàn (Recurrent Gated Short-Convolution Fusion và Normalized Linear Fusion Layers) trong LFM2.5.
   - Việc tích hợp Triton Kernels giúp giảm thiểu thời gian tính toán trạng thái ẩn của mô hình Recurrent và giảm đáng kể số lần đọc weights/băng thông VRAM, từ đó cải thiện mạnh cả TTFT P50 và P95.
   - **Kết luận**: Triton Custom Kernels bắt buộc phải được kích hoạt (`VLLM_CUSTOM_KERNEL=1`) trong cấu hình tối ưu cuối cùng.
