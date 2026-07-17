# Kết quả Benchmark - 22:10 16/07/2026 (STT 135 - Slot 15 - Seqs=32 + FP8 Quantization)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Kích hoạt chế độ lượng tử hóa FP8 online của vLLM để tối đa hóa băng thông bộ nhớ và năng lực tính toán của GPU.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **55.04**  | Điểm số cuối cùng                                     |
| `ers`           | **55.04**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **79 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **115 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Đột phá hiệu năng cực kỳ ấn tượng**:
   - Điểm số **ERS nhảy vọt lên 55.04 điểm** (+9.96 điểm so với kỷ lục tốt nhất trước đó là 45.08 ở Slot 8). Đây là một bước nhảy vọt chưa từng có ở Round 2!
   - Lần đầu tiên trong tất cả các lượt chạy, **TPOT Median được bẻ gãy xuống còn 4ms** (so với mốc 5ms bất biến của tất cả cấu hình FP16).
   - TTFT P50 giảm sâu không tưởng xuống còn **79ms** (giảm 12ms so với mốc tốt nhất ở chunk size sweep).
   - TTFT P95 giảm xuống chỉ còn **115ms** (giảm tới 24ms so với mốc tốt nhất ở chunk size sweep).

2. **Bài học rút ra**:
   - **FP8 online quantization hoạt động cực kỳ mượt mà**: vLLM tự động lượng tử hóa các tính toán ma trận về FP8 giúp GPU giảm một nửa băng thông bộ nhớ truyền tải weights, tăng tốc độ tính toán Tensor core đáng kể ở cả hai pha prefill và decode.
   - Nhờ tốc độ xử lý GPU cực nhanh, trễ decode trung bình trên token giảm đáng kể, giúp TPOT Median chính thức phá vỡ giới hạn scheduler CPU để chạm mốc 4ms.
   - Việc TTFT P95 giảm xuống 115ms cho thấy tốc độ prefill của FP8 cực nhanh, giúp dọn dẹp hàng đợi siêu tốc, triệt tiêu hoàn toàn nghẽn hàng đợi lúc Poisson burst.
   - Đây chính là cấu hình nền tảng tuyệt đối (Golden Baseline) cho tất cả các thử nghiệm tối ưu kết hợp của Ngày 17/07.
