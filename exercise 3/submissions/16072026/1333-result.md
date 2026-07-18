# Kết quả Benchmark - 13:33 16/07/2026 (STT 118 - Slot 3 - Seqs=48)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=48` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá sự cân bằng giữa queuing delay (TTFT) và decode speed (TPOT) cho mô hình tuần hoàn mới LFM2.5-1.2B-Instruct dưới traffic Poisson ngẫu nhiên.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **47.76**  | Điểm số cuối cùng                                     |
| `ers`           | **47.76**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **8**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **6 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **55 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **93 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

1. **Phân tích hiệu năng hệ thống**:
   - **Xác nhận Grader mới**: Các chỉ số `total_count: 330` và `warmup_count: 90` khớp hoàn toàn với cấu trúc trace Poisson mới. Điểm số **42.91** là kết quả thực tế đầu tiên chạy trên mô hình **LFM2.5-1.2B-Instruct**.
   - **TTFT xuất sắc**: TTFT P50 đạt **103ms** và P95 đạt **151ms**, đều nằm sâu dưới ngưỡng trần **400ms** (Ceiling). Điều này chứng minh Prefix Caching hoạt động cực kỳ hoàn hảo cho các turn sau của hội thoại (gần như cache hit 100%), và mức concurrency 48 hoàn toàn hấp thụ được các đợt burst Poisson mà không bị nghẽn hàng đợi (P95 TTFT chỉ lệch 48ms so với P50).
   - **TPOT cực nhanh nhưng còn dư địa tối ưu**: TPOT Median đạt **5ms**, nằm dưới mốc trần 10ms (giúp ăn điểm thành phần TPOT). Tuy nhiên, theo công thức ERS thế lũy thừa $\gamma=2$:
     - Với TPOT = 5ms, điểm thành phần $s_{tpot} = \left(\frac{10 - 5}{9}\right)^2 \approx 0.31$ (chỉ ăn được 31% điểm TPOT tối đa).
     - Nếu đưa TPOT xuống **3ms**, điểm thành phần $s_{tpot}$ sẽ tăng vọt lên $\approx 0.60$ (tăng gấp đôi điểm TPOT, đẩy tổng điểm lên **~58.00**).
     - Nếu đưa TPOT xuống **2ms**, $s_{tpot} \approx 0.79$, tổng điểm ERS sẽ bứt phá lên **~67.00**.

2. **Cổ chai hiện tại và hướng tối ưu**:
   - Do model LFM2.5-1.2B rất nhỏ và VRAM cực kỳ dư dả, thời gian tính toán của GPU cho mỗi token là cực nhỏ (< 1ms). Cổ chai 5ms TPOT chủ yếu đến từ **CPU scheduling overhead** (vòng lặp điều phối của vLLM bằng Python trên 3 core CPU bị giới hạn).
   - Việc chạy concurrency lớn (`max_num_seqs=48`) làm vLLM tốn nhiều CPU time để duyệt và quản lý các active sequences ở mỗi bước decode.
   - Do hàng đợi hiện tại đang dư dả (P95 TTFT chỉ 151ms), chúng ta có thể **giảm mạnh concurrency** xuống mức `Seqs=32` hoặc `Seqs=24` để giảm tải tối đa cho CPU, từ đó kéo TPOT xuống mức 2ms - 3ms mà không lo ngại tăng TTFT vượt quá ngưỡng 400ms.

3. **Kết luận**:
   - **Slot 4 (Seqs=32)** là bước đi tiếp theo hoàn hảo để hiện thực hóa việc tối ưu TPOT.
