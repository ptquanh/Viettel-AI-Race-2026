# Kết quả Benchmark - 10:31 18/07/2026 (STT 38 - Slot 8 - Spec N-gram 4-3 + Compile L3 - Seqs=32 + FP8 + Warmup + Custom Kernels + Spec N-gram 4-3 + Compile L3)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + `--speculative-model=[ngram]` + `--ngram-prompt-lookup-max=4` + `--num-speculative-tokens=3` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá speculative decoding mức nhẹ (N-gram 4-3) trên nền Custom Image + Compile Level 3.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **59.80** | Điểm số cuối cùng                                     |
| `ers`           | **59.80** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **6**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **51 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **82 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng & Trễ (Latency)**:
   - Điểm số **ERS giảm từ 60.91 xuống còn 59.80** (-1.11 điểm).
   - TTFT P50 tăng từ 45ms lên **51ms** (+13.3%).
   - TTFT P95 tăng từ 70ms lên **82ms** (+17.1%).
   - TPOT Median vẫn giữ nguyên ở mức **4 ms**.

2. **Tại sao Speculative Decoding không đem lại hiệu năng tốt?**:
   - **Overhead xác thực lớn hơn lợi ích**: Mô hình LFM2.5 (1.2B) có recurrent layers tính toán cực kỳ nhanh (step forward chỉ mất ~1.7ms weights read + ~0.5ms computation). Khi kích hoạt Speculative Decoding, vLLM phải chạy thêm thuật toán tìm kiếm N-gram trên chuỗi context và thực hiện bước validation logits phức tạp. Trên môi trường 3 CPU cores hạn chế, overhead lập lịch và xác thực này triệt tiêu hoàn toàn lợi thế sinh nhiều token cùng lúc.
   - **Tác động lên compile**: Tracing đồ thị khi bật speculative decoding làm phình kích thước đồ thị CUDA Graphs, tăng overhead nạp và gọi kernel của GPU, dẫn đến TTFT tăng mạnh ở cả P50 và P95.
