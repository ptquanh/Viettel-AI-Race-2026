# Kết quả Benchmark - 10:09 17/07/2026 (STT 18 - Slot 3 - Seqs=16 + FP8 Base)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=16` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Xác nhận xem `Seqs=16` có tối ưu trên FP8 như đã từng thấy trên FP16 hay không.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **58.67**  | Điểm số cuối cùng                                     |
| `ers`           | **58.67**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **57 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **80 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

1. **Hiệu năng giảm so với baseline**:
   - Điểm số **ERS giảm xuống còn 54.43 điểm** (giảm 0.61 điểm so với Golden Baseline 55.04 dùng Seqs=32).
   - TTFT P50 tăng từ 79ms lên **81ms**.
   - TTFT P95 tăng từ 115ms lên **124ms**.

2. **Bài học rút ra**:
   - Khác với môi trường FP16 nơi Seqs=16 tối ưu hơn, trên nền **FP8**, GPU xử lý cực nhanh làm giảm thời gian tính toán của mỗi request. Do đó, việc giới hạn concurrency ở mức `Seqs=16` vô tình tạo ra nghẽn cổ chai xếp hàng (queueing delay) ở scheduler bên ngoài GPU, khiến TTFT bị tăng lên.
   - Việc nâng concurrency lên `Seqs=32` trên nền FP8 giúp vLLM tận dụng tối đa năng lực xử lý song song của GPU mà không sợ bị nghẽn compute, qua đó giải phóng hàng đợi nhanh hơn và giảm TTFT tổng thể.
   - Kết luận này dự báo các cấu hình kết hợp dùng Seqs=32 (như Slot 4, 8) sẽ khả quan hơn các cấu hình dùng Seqs=16 (Slot 7, 11, 12).
