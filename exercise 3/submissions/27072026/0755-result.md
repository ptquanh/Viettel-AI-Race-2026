# Kết quả chấm điểm Slot 02 (0755 - 27/07/2026) - TĂNG ĐIỂM + CẢI THIỆN ỔN ĐỊNH (53.26đ)

- **Thời gian nộp**: 07:55 AM (27/07/2026)
- **Chiến lược**: Custom CUDA C++ Kernel Fusion (`v16.3`) + `CUDAGRAPH_NUM_OF_WARMUPS=10`
- **Cấu hình**: Champion Config + `CUDAGRAPH_NUM_OF_WARMUPS=10` (`GPU_MEM=0.94`)
- **Điểm số**: **53.2600 điểm** (Tăng +0.50đ so với Slot 01!)
- **Số request lỗi (Failed count)**: 5 (Giảm 1 lỗi từ 6 xuống 5!)

## Chỉ số chi tiết (Benchmark Metrics)

| Chỉ số Metric         |   Giá trị   | Nhận xét                                              |
| :-------------------- | :---------: | :---------------------------------------------------- |
| **Final Score**       | **53.2600** | 🔥 **Tăng điểm nhẹ (+0.50đ) nhờ độ ổn định cao hơn!** |
| **TTFT P50**          |  **57 ms**  | Duy trì tốc độ siêu cấp (Champion cũ = 58ms)          |
| **TTFT P95**          |  **74 ms**  | Duy trì P95 ấn tượng (Champion cũ = 85ms)             |
| **TBT Median (TPOT)** |  **5 ms**   | Giữ mốc 5ms                                           |
| **Accuracy Drop**     |  **0.00**   | Độ chính xác nguyên bản 100%                          |
| **Failed Requests**   |    **5**    | 🔥 **Giảm 1 lỗi (từ 6 xuống 5 requests)**             |
| **Tokens / sec**      | **0.0557**  |                                                       |

---

## Phân tích chuyên sâu (Technical Insight)

1. **Hiệu quả của `CUDAGRAPH_NUM_OF_WARMUPS=10`**:
   - Tăng số vòng khởi động CUDA Graph Warmup từ 5 lên 10 giúp GPU Graph Allocator ghi nhớ chính xác hơn các kích thước batch/sequence thường gặp.
   - Kết quả trực tiếp: **Failed requests giảm từ 6 xuống 5**, jitter hệ thống ít hơn, giúp tổng điểm tăng từ 52.76đ lên **53.26đ**!

2. **Khẳng định cấu hình Baseline tối ưu**:
   - Kết hợp giữa **Image `v16.3` + `GPU_MEM=0.94` + `CUDAGRAPH_NUM_OF_WARMUPS=10`** hiện là bộ khung Baseline chạy ổn định và mượt mà nhất (TTFT P50 = 57ms, P95 = 74ms).
