# Kết quả Benchmark - 16:45 16/07/2026 (STT 120 - Slot 2 - Seqs=32)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Kiểm tra xem việc hạ concurrency xuống 32 có giúp giảm tải CPU, từ đó cải thiện TPOT và tăng điểm số hay không.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **43.08**  | Điểm số cuối cùng                                     |
| `ers`           | **43.08**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **5 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **103 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **158 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Nhận xét điểm số**:
   - Điểm số **tăng nhẹ** từ 42.91 lên **43.08** (+0.17 điểm).
   - TTFT P50 giữ nguyên **103ms**, TTFT P95 tăng nhẹ từ 151ms lên **158ms** (+7ms) do hàng đợi hẹp hơn (Seqs=32 so với 48).
   - TPOT Median vẫn kẹt ở **5ms**. Điểm số tăng nhẹ chứng tỏ phân phối TPOT của các request riêng lẻ có sự cải thiện nhẹ (ít request bị vượt ngưỡng 5ms hơn), nhưng chưa có sự đột phá.

2. **Bài học rút ra**:
   - Giảm `max-num-seqs` từ 48 xuống 32 là chưa đủ để giải phóng CPU overhead của vLLM trên 3 cores vật lý đối với mô hình LFM2.5.
   - Chúng ta cần thử nghiệm các mốc concurrency thấp hơn nữa ở các slot tiếp theo:
     - **Slot 3 (Seqs=24)**: Điểm ngọt truyền thống của vLLM.
     - **Slot 4 (Seqs=16)**: Điểm cực đoan để ép TPOT chạm mốc tối đa.
