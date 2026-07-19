# Kết quả Benchmark - 07:39 19/07/2026 (STT 46 - Slot 1 - Seqs=32 + MaxLen=16K)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `--max-model-len=16384` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}`.
- **Mục đích**: Đánh giá hiệu năng mốc trung gian MaxLen=16384 trên nền baseline tối ưu (compile level 3).

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **49.74**  | Điểm số cuối cùng                                     |
| `ers`           | **49.74**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**    | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **7**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **5 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **79 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **105 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Suy giảm hiệu năng mạnh**:
   - Điểm ERS giảm nặng từ 60.91 (STT 32) xuống còn **49.74 điểm** (-11.17 điểm).
   - TPOT vọt từ 4ms lên 5ms, làm giảm 30% s_score TPOT (từ 0.444 xuống 0.308).
   - TTFT P50 tăng từ 45ms lên 79ms và P95 tăng từ 70ms lên 105ms.

2. **Bài học rút ra**:
   - Mốc 16K làm lệch Triton kernel tiling dimensions và tạo ra memory fragmentation nhẹ với CUDA Graph Level 3.
   - **Xác nhận Best Len = 32768 (32K)** là mốc duy nhất tối ưu phần cứng trên hạ tầng H200 của BTC.
