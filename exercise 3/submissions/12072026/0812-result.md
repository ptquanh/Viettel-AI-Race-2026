# Kết quả Benchmark - 12/07/2026 (STT TBD - Ghost v9.1: Concurrency Tweak - Seqs 24 - Slot 2)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=24` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + Tắt Chunked Prefill.
- **Mục đích**: Tinh chỉnh giới hạn concurrency từ 32 xuống 24 để tối ưu hóa thêm tốc độ decode, nỗ lực đưa TPOT xuống mức vật lý cực hạn (< 15ms) trên GPU trong khi vẫn đủ năng lực xử lý một đợt 20 requests/5 giây.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |   **3.36**   | Điểm số cuối cùng                                   |
| `ers`           |   **3.36**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.033333** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **4**     | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **0%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **44 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **6711 ms** | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **12566 ms** | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Hiệu năng & So sánh**:
   - Điểm số chỉ đạt **3.36** (Passed SLO 4/120).
   - TPOT đạt **44 ms** (tốt hơn mức 56ms của slot 1 do giảm concurrency xuống 24).
   - TTFT P50 tăng vọt thảm hại lên **6711 ms** (gần gấp đôi slot 1).
2. **Nguyên nhân cốt lõi**:
   - **Thiếu `VLLM_CUSTOM_KERNEL=1`**: Tương tự như Slot 1, việc thiếu biến môi trường này khiến container không chạy Monkey Patch để tối ưu hóa Triton kernel dequantize KV Cache.
   - **Hiệu ứng hàng đợi tích lũy (Queuing Delay)**: Việc giới hạn concurrency xuống 24 kết hợp với tốc độ xử lý chậm (do không dùng custom kernel) làm cho hàng đợi tích lũy cực nhanh. 96 request còn lại phải xếp hàng chờ quá lâu, dẫn đến TTFT P50 tăng từ 3.6s lên 6.7s.
3. **Kết luận**:
   - Thử nghiệm này một lần nữa khẳng định: Nếu không kích hoạt custom kernel, việc hạ concurrency sẽ làm trầm trọng thêm queuing delay và triệt tiêu hoàn toàn điểm số.

