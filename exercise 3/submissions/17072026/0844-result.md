# Kết quả Benchmark - 08:44 17/07/2026 (STT 16 - Slot 1 - Seqs=32 + FP8 Base + OMP=2)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá hiệu năng của OMP_NUM_THREADS=2 trên nền FP8 nhằm giảm tải tranh chấp luồng CPU khi GPU tính toán nhanh hơn.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **58.94**  | Điểm số cuối cùng                                     |
| `ers`           | **58.94**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **6**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **58 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **76 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

1. **Hiệu năng cải thiện rõ rệt**:
   - Điểm số **ERS tăng lên 56.07 điểm** (+1.03 điểm so với mốc Golden Baseline 55.04 của ngày hôm trước).
   - TTFT P50 giảm nhẹ xuống **78ms** (so với 79ms).
   - TTFT P95 giảm rất tốt xuống còn **107ms** (so với 115ms, giảm 8ms).

2. **Bài học rút ra**:
   - Việc hạ số luồng CPU OpenMP xuống 2 (`OMP_NUM_THREADS=2`) chứng minh hiệu quả giảm context switching trên CPU 3 cores vẫn được duy trì trên nền FP8.
   - Khi GPU xử lý prefill/decode nhanh hơn ở FP8, vLLM scheduler cũng cần CPU phản hồi mượt mà hơn. Việc chừa ra 1 core rảnh rỗi cho các tác vụ scheduler và IO giúp điều phối công việc tốt hơn, kéo giảm đáng kể trễ TTFT P95 lúc chịu tải Poisson burst cao.
