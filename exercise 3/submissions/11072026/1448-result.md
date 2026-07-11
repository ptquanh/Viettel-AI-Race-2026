# Kết quả Benchmark - 14:48 11/07/2026 (STT 85 - FP8 weights + Chunked Prefill 8192)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + Chunked Prefill 8192.
- **Mục đích**: Tìm điểm cân bằng chunk size, tăng từ 4096 lên 8192 để giảm số vòng lặp trên CPU.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |   **5.55**   | Điểm số cuối cùng                                   |
| `ers`           |   **5.55**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.658333** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **79**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **3%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **46 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **1503 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **8567 ms**  | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Hiệu năng giảm nghiêm trọng (5.55 so với 12.91 ở chunk size 4096)**:
   - TTFT P50 tăng vọt từ 960ms lên 1503ms, làm số request passed SLO giảm từ 85 xuống 79.
   - Nguyên nhân chính: Chunk size quá lớn (8192) chiếm dụng tài nguyên GPU tính toán prefill liên tục trong thời gian dài hơn, gây nghẽn nghiêm trọng (queuing delay) cho các bước decode của các request khác đang đồng thời chạy.
   - Mặc dù TPOT giảm nhẹ từ 51ms xuống 46ms (do gom batch prefill lớn giúp GPU xử lý tối ưu hơn ở bước decode sau đó nhờ RadixAttention), độ phạt lũy thừa $\gamma = 2$ của TTFT trong ERS đã triệt tiêu hoàn toàn điểm cộng này.
2. **Độ chính xác GPQA**:
   - Ghi nhận `accuracy_drop: 3%`, nằm trong biên độ an toàn và không bị phạt ($f(\Delta) = 1.0$).
3. **Kết luận**:
   - Tăng chunk size lên 8192 là đi ngược lại mục tiêu tối ưu. Càng nâng chunk size lên cao, TTFT càng tệ hại.
   - Phương án giảm chunk size xuống nhỏ hơn (như 2048 ở `slot1`) là hướng đi đúng đắn cần được xác minh tiếp theo.
