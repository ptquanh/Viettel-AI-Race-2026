# Kết quả Benchmark - 21:18 16/07/2026 (STT 124 - Slot 7 - Seqs=32 + Chunk=2048)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--enable-chunked-prefill` + `--max-num-batched-tokens=2048` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Kiểm tra hiệu quả của Chunked Prefill (với chunk size 2048) trên nền tảng Seqs=32 nhằm giải quyết hiện tượng prefill interference và cải thiện trễ TTFT.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **44.63**  | Điểm số cuối cùng                                     |
| `ers`           | **44.63**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **5 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   |  **96 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **139 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Nhận xét điểm số**:
   - Điểm số **đạt kỷ lục mới xuất sắc**: **44.63 điểm** (tăng mạnh +1.55 điểm so với mốc 1645 Seqs=32 không chunk, và +1.32 điểm so với kỷ lục Seqs=16 ở Slot 4).
   - TTFT P50 lần đầu tiên hạ xuống dưới 100ms, đạt **96ms** (giảm 7ms).
   - TTFT P95 giảm rất sâu còn **139ms** (giảm tới 19ms so với Seqs=32 không chunk).
   - TPOT Median vẫn giữ ổn định ở **5ms**.

2. **Bài học rút ra**:
   - **Chunked Prefill hoạt động cực kỳ hiệu quả**: Việc cắt nhỏ quá trình prefill thành các chunk 2048 giúp vLLM scheduler dễ dàng chèn xen kẽ (interleave) các bước decode và prefill. Nhờ đó, các request mới không bị block lâu bởi các pha prefill context dài của turn 0, giúp triệt tiêu hoàn toàn các spike của TTFT và tối ưu hóa trễ P95.
   - Trễ TTFT P95 giảm sâu xuống 139ms giúp kéo điểm số ERS trung bình của toàn bộ request lên rất cao, thiết lập kỷ lục mới dù TPOT vẫn kẹt ở 5ms.
   - Thử nghiệm này củng cố giả thuyết rằng **Prefill Interference** là một trong những cổ chai lớn của hệ thống serving LFM2.5 trên 3 cores CPU này.
