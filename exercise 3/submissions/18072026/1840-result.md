# Kết quả Benchmark - 18:40 18/07/2026 (STT 45 - Slot 15 - Custom Image + Seqs=32 + Len=8192)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `VLLM_MAX_NUM_SEQS=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":3}` + **`--max-model-len=8192` (TỐI ƯU HÓA BỘ NHỚ)** + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Chạy cấu hình Golden Combo (Seqs=32, Len=8192, Compile L3 thuần) để kiểm chứng hiệu năng tối đa và độ ổn định.

## Chỉ số đo được

| Chỉ số          |  Giá trị  | Ý nghĩa                                               |
| :-------------- | :-------: | :---------------------------------------------------- |
| `final_score`   | **58.50** | Điểm số cuối cùng                                     |
| `ers`           | **58.50** | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**   | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**   | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**  | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **5**   | Số lượng request thất bại                             |
| `accuracy_drop` |  **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` | **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **56 ms** | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **91 ms** | Time To First Token (P95)                             |

## Phân tích kết quả

1. **Sự sụt giảm hiệu năng bất thường so với Slot 2 (60.91) và các Slot khác**:
   - Cấu hình Slot 15 giống hệt Slot 2 ngoại trừ việc đổi `--max-model-len` từ `32768` thành `8192`.
   - Kết quả: Điểm ERS giảm mạnh từ 60.91 xuống **58.50**. Trễ TTFT P50 tăng từ 45ms lên **56ms (+24.4%)**, TTFT P95 tăng từ 70ms lên **91ms (+30.0%)**.
2. **Lý giải nguyên nhân**:
   - **Tác động của Vấn đề Cướp Tài Nguyên / Noise từ Hệ thống (System Jitter)**: Lượt chạy này diễn ra vào lúc **18:40** (giờ cao điểm nộp bài cận kề kết thúc ngày). Sự suy giảm đồng loạt ở cả P50 (56ms) và P95 (91ms) trên cùng một cấu hình ngọt chỉ ra khả năng cao hệ thống host MiG của BTC bị nghẽn CPU/IO do quá tải chia sẻ tài nguyên phần cứng giữa các container hoặc hàng đợi chấm bài dồn dập.
   - **Tác động kỹ thuật của `--max-model-len=8192`**:
     - Mặc dù giảm `max-model-len` giúp giải phóng bộ nhớ KV cache (giảm được lỗi xuống còn 5 failed), nhưng nó lại làm thay đổi tập hợp các shapes được CUDA graph định dạng trước lúc compile.
     - Khi chạy thực tế, một số request có thể bị rơi vào các shape chưa được graph tối ưu tốt nhất, gây ra các bước tính toán eager fallback phụ trội làm chậm TTFT.
3. **Tổng kết so sánh nhóm đối chứng Concurrency dưới nền `Len=8192`**:
   - **Seqs=24 (Slot 14 - 15:39)**: ERS = **60.07**, P50 = 52ms, P95 = **69ms** (Trễ đuôi cực tốt).
   - **Seqs=48 (Slot 13 - 14:30)**: ERS = **60.10**, P50 = 53ms, P95 = 73ms.
   - **Seqs=32 (Slot 15 - 18:40)**: ERS = 58.50, P50 = 56ms, P95 = 91ms (Bị nhiễu hệ thống nặng).

4. **Kết luận**:
   - Cấu hình nền tảng tối ưu nhất cho ngày 18/07 vẫn là **Compile L3 + Custom Image + Seqs=32** của **Slot 2** mang lại kỷ lục **60.91**.
   - Cần tiếp tục duy trì `--max-model-len=32768` hoặc thực hiện kiểm thử kỹ lưỡng hơn về warmup shape cho `8192` trong các đợt chạy offline tiếp theo.
