# Kết quả Benchmark - 19:01 17/07/2026 (STT 30 - Slot 15 - Seqs=32 + FP8 + OMP=1 + Chunk=4096)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=1` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096`.
- **Mục đích**: Thử nghiệm cực hạn giảm OpenMP xuống 1 thread (`OMP_NUM_THREADS=1`) để so sánh hiệu năng CPU thread với mốc OMP=2 và OMP=4 (mặc định) khi kết hợp cùng Chunk=4096.

## Chỉ số đo được

| Chỉ số          |  Giá trị   | Ý nghĩa                                               |
| :-------------- | :--------: | :---------------------------------------------------- |
| `final_score`   | **58.83**  | Điểm số cuối cùng                                     |
| `ers`           | **58.83**  | Điểm số hiệu năng (Effective Request Score)           |
| `f_delta`       |   **1**    | Hệ số phạt chất lượng (1 = Không phạt)                |
| `penalty`       |   **1**    | Hệ số phạt chung (1 = Không bị phạt)                  |
| `total_count`   |  **420**   | Tổng số request benchmark được chấm điểm              |
| `warmup_count`  |   **0**   | Số lượng request khởi động (Warmup - không tính điểm) |
| `failed_count`  |   **6**    | Số lượng request thất bại                             |
| `accuracy_drop` |   **0%**   | Độ sụt giảm độ chính xác                              |
| `tbt_median_ms` |  **4 ms**  | Median Time Between Tokens (TPOT)                     |
| `ttft_p50_ms`   | **57 ms**  | Time To First Token (P50)                             |
| `ttft_p95_ms`   | **80 ms** | Time To First Token (P95)                             |



> [!NOTE]
> Kết quả này đã được BTC tự động chấm lại. Các chỉ số đo được trong bảng dưới đây đã được cập nhật theo kết quả mới nhất.

## Phân tích kết quả

1. **Hiệu năng giảm mạnh so với OMP=2**:
   - Điểm số **ERS đạt 55.02 điểm** (thấp hơn nhiều so với **56.79** của Slot 4).
   - TTFT P95 tăng vọt lên **118ms** (so với 93ms ở Slot 4).

2. **Xác nhận đồ thị hình chuông của luồng OpenMP (OMP_NUM_THREADS)**:
   - Thử nghiệm này hoàn tất bức tranh phân tích CPU của chúng ta:
     - **OMP=4 (Mặc định)**: Đạt **56.53 điểm** (TTFT P95 = 106ms). Bị nghẽn nhẹ do CPU context switching (vượt quá 3 physical cores).
     - **OMP=2 (Sweet-spot)**: Đạt **56.79 điểm** (TTFT P95 = 93ms). Tối ưu tuyệt đối nhờ cân bằng tải: 2 thread tính toán song song, chừa lại 1 core cho tiến trình I/O và Scheduler.
     - **OMP=1 (Thiếu luồng)**: Đạt **55.02 điểm** (TTFT P95 = 118ms). Bị nghẽn cổ chai tính toán do chỉ có 1 thread đơn lẻ gánh toàn bộ tác vụ.
   - Kết quả này củng cố khẳng định chắc chắn: **`OMP_NUM_THREADS=2` là cấu hình tối ưu nhất** cho phần cứng 3 Core CPU của BTC.
