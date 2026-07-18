# Kết quả Benchmark - 18:19 16/07/2026 (STT 123 - Slot 4 - Seqs=16)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=16` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Kiểm tra xem việc hạ concurrency xuống cực hạn Seqs=16 có giúp kéo TPOT xuống dưới 5ms hay không.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **48.01**  | Điểm số cuối cùng                                     |
| `ers`           | **48.01**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **6 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **55 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **88 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

1. **Nhận xét điểm số**:
   - Điểm số **đạt kỷ lục mới**: **43.31 điểm** (+0.23 điểm so với Seqs=32).
   - TTFT P50 đạt **101ms** (giảm 2ms), TTFT P95 đạt **146ms** (giảm 12ms so với Seqs=32).
   - Concurrency cực thấp Seqs=16 giúp giảm thiểu tối đa tranh chấp tài nguyên và scheduler overhead của vLLM, đẩy cả TTFT P50 và P95 xuống mức tối ưu nhất từ trước tới nay cho LFM2.5.
   - Tuy nhiên, TPOT Median vẫn kẹt cứng ở **5ms**.

2. **Bài học rút ra**:
   - TPOT Median 5ms là giới hạn cứng của vLLM Serving đối với LFM2.5 trên 3 cores vật lý của Node chấm thi nếu chạy ở cấu hình mặc định (không bật chunked prefill hay lượng tử hóa).
   - Việc hạ Seqs xuống 16 giúp hệ thống phục vụ nhẹ nhàng hơn, giảm trễ xếp hàng hàng đợi (TTFT), qua đó đem lại điểm số tối ưu nhất hiện tại.
   - Do Seqs=16 đã cho điểm tốt nhất, trong các thử nghiệm ngày mai, nếu có điều kiện, chúng ta nên cân nhắc dùng Seqs=16 làm mốc so sánh chính. Tuy nhiên, do chúng ta đã nộp song song các slot từ 5 đến 15 dựa trên nền tảng Seqs=32 (vì lý do thiếu thời gian cuối ngày), chúng ta sẽ đánh giá tương quan hiệu quả dựa trên mốc Seqs=32 này trước.
