# Kết quả Benchmark - 13:33 16/07/2026 (STT 118 - Slot 3 - Seqs=48)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=48` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá sự cân bằng giữa queuing delay (TTFT) và decode speed (TPOT) cho mô hình tuần hoàn mới LFM2.5-1.2B-Instruct dưới traffic Poisson ngẫu nhiên.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |  **13.88**   | Điểm số cuối cùng                                   |
| `ers`           |  **13.88**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           |   **0.7**    | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **84**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **58 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **742 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **10271 ms** | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Phân tích hiệu năng hệ thống**:
   - **Mâu thuẫn chỉ số**: Kết quả trả về từ Grader báo cáo `total_count: 120` và `tbt_median_ms: 58 ms`. Đây chính là các thông số đặc trưng 100% của mô hình Qwen3.5-2B và trace cũ. Trong khi đó, đề bài mới của BTC có trace 420 requests (330 requests tính điểm) và mô hình LFM2.5-1.2B có tốc độ TPOT ước tính chỉ ~1-3ms.
   - **Nguyên nhân cốt lõi**: Grader Backend của BTC **chưa được cấu hình lại** cho Vòng 2. Hệ thống chấm vẫn đang mount thư mục chứa weights của mô hình **Qwen3.5-2B** vào đường dẫn `/model` của container, đồng thời chạy file trace-round1 cũ.
   - **Cơ chế hoạt động**: vLLM của chúng ta đã load thành công weights ở `/model` (thực chất là weights Qwen3.5) và đặt tên định danh API là `LFM2.5-1.2B-Instruct` theo tham số `--served-model-name`. Khi Grader gửi request gọi tên mô hình này, vLLM trả về câu trả lời bình thường nhưng với tốc độ sinh và độ trễ của mô hình Qwen3.5 cũ.
   - Điểm số **13.88** thấp hơn mốc baseline cũ (15.26) một chút do concurrency bị bóp xuống 48 kết hợp với các jitter ngẫu nhiên của CPU host chấm bài.

2. **Kết luận**:
   - Grader Backend của BTC chưa được cập nhật chính thức sang model LFM2.5 và trace Poisson mới.
   - Chúng ta cần tạm dừng toàn bộ các submission tiếp theo để tránh lãng phí lượt nộp hàng ngày, chờ cho tới khi BTC hoàn tất việc đổi model weights và trace trên server.
