# Kết quả Benchmark - 12/07/2026 (STT TBD - Ghost v9.0: FP8 Weights + Custom FP8 KV + Seqs 32 + Prefix Warmup - Slot 1)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=32` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + Tắt Chunked Prefill.
- **Mục đích**: Áp dụng công thức 100 điểm: Tắt Chunked Prefill để giải phóng CPU scheduling bottleneck, kết hợp giới hạn concurrency Seqs=32 để hạ TPOT xuống $\le 20\text{ms}$ và triệt tiêu Queuing Delay, đồng thời dùng JIT Warmup thông qua System Prompt thực tế để cache sẵn prefix 20k tokens.

## Chỉ số đo được

| Chỉ số          |   Giá trị    | Ý nghĩa                                             |
| :-------------- | :----------: | :-------------------------------------------------- |
| `final_score`   |   **2.29**   | Điểm số cuối cùng                                   |
| `ers`           |   **2.29**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           | **0.041667** | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       |    **1**     | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |    **5**     | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |   **120**    | Tổng số request benchmark                           |
| `failed_count`  |    **0**     | Số lượng request thất bại                           |
| `warmup_count`  |    **0**     | Số lượng request warmup                             |
| `accuracy_drop` |    **1%**    | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **56 ms**   | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   | **3698 ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   | **11450 ms** | Time To First Token (P95)                           |

## Phân tích kết quả

1. **Hiệu năng sụt giảm nghiêm trọng (2.29 điểm, Passed SLO 5/120)**:
   - TPOT tăng vọt từ 30ms lên **56 ms** (bằng mức BF16 gốc).
   - TTFT P50 tăng vọt lên **3698 ms**.
2. **Nguyên nhân cốt lõi**:
   - **Thiếu biến môi trường `VLLM_CUSTOM_KERNEL=1`**: Trong `slot1-docker-compose.yml`, chúng ta đã quên không thiết lập biến này. Do đó, script `sitecustomize.py` trong container không kích hoạt Monkey Patch cho PagedAttention. Việc lượng tử hóa KV cache chạy bằng cơ chế gốc của vLLM gây ra overhead chuyển đổi cực lớn trên CPU 3 cores, triệt tiêu hoàn toàn hiệu năng của GPU.
   - **Lỗi định dạng YAML trong deploy GPU**: Cấu hình thiết bị GPU bị chia thành 3 phần tử danh sách riêng biệt thay vì lồng trong cùng 1 thiết bị (`- driver: nvidia`, `- count: 1`, `- capabilities: [gpu]`). Điều này có thể làm giảm khả năng nhận diện GPU tối ưu của Docker.
3. **Kết luận**:
   - Thử nghiệm này vô hiệu do lỗi cấu hình môi trường.
   - Bắt buộc phải bổ sung `VLLM_CUSTOM_KERNEL=1` và sửa định dạng YAML GPU cho các đợt chạy tiếp theo để kích hoạt custom Triton kernel.
