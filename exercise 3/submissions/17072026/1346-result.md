# Kết quả Benchmark - 13:46 17/07/2026 (STT 23 - Slot 8 - Seqs=32 + FP8 + OMP=2 + Chunk=4096 + VRAM 98%)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096` + `--gpu-memory-utilization=0.98`.
- **Mục đích**: Kiểm tra xem việc tăng dung lượng VRAM cấp phát cho KV cache lên 98% (thay vì 95%) có giúp cải thiện hiệu năng của combo tối ưu (OMP=2 + Chunk=4096) hay không.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **55.94**  | Điểm số cuối cùng                                     |
| `ers`           | **55.94**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **330**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **90**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **0**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **75 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **113 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Hiệu năng giảm so với mốc VRAM 95% (Slot 4)**:
   - Điểm số **ERS đạt 55.94 điểm** (giảm đáng kể so với mốc **56.79 điểm** của Slot 4).
   - TTFT P95 tăng vọt từ 93ms lên **113ms**.

2. **Bài học rút ra**:
   - Việc tăng `--gpu-memory-utilization` lên `0.98` gây tác dụng ngược. Dù về mặt lý thuyết nó giúp tăng số lượng block KV cache trên GPU để giảm tải việc swap, nhưng ở giới hạn cực cận (98% VRAM của H200 18GB), CUDA driver hoặc vLLM Memory Profiler phải chịu thêm overhead quản lý bộ nhớ hoặc phân mảnh (memory fragmentation).
   - Trong bối cảnh tài nguyên CPU bị giới hạn ở 3 core, overhead bổ sung này trực tiếp kéo lùi trễ TTFT P95.
   - Do đó, **mức `--gpu-memory-utilization=0.95` vẫn là giới hạn an toàn và tối ưu nhất**.
