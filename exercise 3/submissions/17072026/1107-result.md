# Kết quả Benchmark - 11:07 17/07/2026 (STT 20 - Slot 5 - Seqs=32 + FP8 + OMP=2 + MaxLen=8K)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--max-model-len=8192`.
- **Mục đích**: Đánh giá hiệu năng kết hợp của OMP=2 và giới hạn MaxLen=8K trên nền FP8.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **54.16**  | Điểm số cuối cùng                                     |
| `ers`           | **54.16**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **83 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **124 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng sụt giảm đáng kể**:
   - Điểm số **ERS giảm xuống còn 54.16 điểm** (giảm tới 1.91 điểm so với cấu hình chỉ có OMP=2 ở Slot 1 là 56.07).
   - TTFT P50 tăng lên **83ms** (so với 78ms).
   - TTFT P95 tăng vọt lên **124ms** (so với 107ms).

2. **Bài học rút ra**:
   - Mặc dù giới hạn `max-model-len=8192` giúp tăng nhẹ hiệu năng trên FP16 ngày 16/07, nhưng trên nền FP8 nó lại phản tác dụng rất mạnh.
   - Việc hạ giới hạn context tối đa làm thay đổi cách vLLM Block Allocator lập lịch và phân bổ bộ nhớ cho KV Cache. Trên kiến trúc H200 và mô hình FP8 siêu nhanh, việc giới hạn này dường như làm giảm hiệu quả của cơ chế Prefix Caching (hoặc làm tăng overhead quản lý metadata khi block cache bị phân mảnh nhiều hơn), dẫn đến TTFT P95 bị kéo dài đáng kể.
   - Kết quả này cảnh báo chúng ta nên cẩn trọng với các cấu hình kết hợp có chứa `MaxLen=8K` ở nhóm sau (Slot 8, Slot 11). Cấu hình không giới hạn MaxLen (giữ mặc định 32768) có thể sẽ cho kết quả tốt hơn.
