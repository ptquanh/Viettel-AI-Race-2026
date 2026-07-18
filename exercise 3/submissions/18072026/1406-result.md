# Kết quả Benchmark - 14:06 18/07/2026 (STT 42 - Slot 12 - Custom Image + Compile L3 + disable-async-output)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + **`--disable-async-output-proc`** + `--max-model-len=32768` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đo lường tác động của cơ chế async output processing (xử lý output không đồng bộ của vLLM) nhằm giảm CPU scheduling jitter trên host 3 cores.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **60.46** | Điểm số cuối cùng                                     |
| `ers`           | **60.46** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **6**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **47 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **80 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Tác động của việc tắt Async Output Processing**:
   - Khi tắt async output (`--disable-async-output-proc`), điểm số **giảm nhẹ từ 60.91 (Slot 2) xuống còn 60.46 (-0.45 điểm)**.
   - Trễ TTFT P50 tăng nhẹ từ 45ms lên **47 ms**.
   - Trễ TTFT P95 tăng từ 70ms lên **80 ms (+14.3%)**.
   - Tuy nhiên, số request thất bại giảm từ 7 xuống còn **6**.

2. **Bài học rút ra**:
   - Việc tắt xử lý output không đồng bộ giúp giảm bớt CPU context switching và scheduling overhead giữa các luồng xử lý/truyền dữ liệu, do đó giúp giảm nhẹ số request lỗi (từ 7 xuống 6).
   - Tuy nhiên, nó làm chậm quá trình phản hồi token đầu tiên (TTFT) do vLLM phải chờ block output đồng bộ hóa xong mới tiếp tục, dẫn đến độ trễ tổng thể tăng lên (đặc biệt là trễ đuôi P95 tăng 10ms).
   - **Kết luận**: Giữ nguyên tính năng async output mặc định (bật) cho cấu hình tối ưu cuối cùng, vì lợi ích giảm trễ TTFT lớn hơn nhiều so với việc giảm 1 request lỗi.
