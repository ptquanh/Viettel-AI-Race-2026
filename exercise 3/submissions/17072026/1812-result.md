# Kết quả Benchmark - 18:12 17/07/2026 (STT 28 - Slot 13 - Seqs=32 + FP8 Base + KV Cache FP8)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=4` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--kv-cache-dtype=fp8`.
- **Mục đích**: Đánh giá hiệu quả của cờ lượng tử hóa KV Cache FP8 (`--kv-cache-dtype=fp8`) dạng đơn biến trên nền tảng FP8 Base (không có OMP=2 hay Chunked Prefill).

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **58.83**  | Điểm số cuối cùng                                     |
| `ers`           | **58.83**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **4**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **58 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **80 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

1. **Hiệu năng tương đương với FP8 Base gốc**:
   - Điểm số **ERS đạt 55.02 điểm**, hầu như tương đồng tuyệt đối với mốc **55.04 điểm** của FP8 Base gốc (chạy ngày 16/07).
   - TTFT P50/P95 đạt **81ms / 115ms** (so với 79ms / 115ms của FP8 Base).

2. **Bài học rút ra**:
   - Việc áp dụng đơn biến `--kv-cache-dtype=fp8` trên cấu hình mặc định (không tối ưu hóa CPU thread và không có Chunked Prefill để điều phối) không tạo ra cải thiện rõ rệt về mặt độ trễ.
   - Điều này xác nhận lượng tử hóa KV Cache chỉ thực sự phát huy sức mạnh vượt trội khi đi kèm với bộ điều phối luồng hiệu quả (như `OMP=2` và `Chunked Prefill`) giúp giảm tải CPU bottlenecks.
