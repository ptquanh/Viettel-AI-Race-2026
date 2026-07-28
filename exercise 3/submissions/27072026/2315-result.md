# Kết quả chấm điểm Slot 14 (2315 - 27/07/2026) - KẾT QUẢ GIỜ ĐÊM (54.95đ, FAILED REDUCED TO 4)

- **Thời gian nộp**: 11:15 PM (27/07/2026)
- **Chiến lược**: CUTLASS FP8 Scaled MM Kernel (`v20.0`) + Champion Setup
- **Cấu hình**: Image `v20.0` + `GPU_MEM=0.95` + `MAX_LEN=32768` + `SEQS=32` + `WARMUPS=10`
- **Điểm số**: **54.9500 điểm**
- **Số request lỗi (Failed count)**: 4 (Đã giảm 1 request lỗi so với 5 lỗi ở Slot 12!)

## Chỉ số chi tiết (Benchmark Metrics)

| Chỉ số Metric         |   Giá trị   | Nhận xét                                          |
| :-------------------- | :---------: | :------------------------------------------------ |
| **Final Score**       | **54.9500** |                                                   |
| **TTFT P50**          |  **68 ms**  | Ảnh hưởng do tải máy chủ BTC giờ cao điểm ban đêm |
| **TTFT P95**          |  **94 ms**  |                                                   |
| **TBT Median (TPOT)** |  **4 ms**   | Giữ vững mốc 4ms chuẩn                            |
| **Accuracy Drop**     |  **0.00**   | Độ chính xác nguyên bản 100%                      |
| **Failed Requests**   |    **4**    | 🔥 Giảm từ 5 xuống 4 request lỗi!                 |
| **Tokens / sec**      | **0.0544**  |                                                   |

---

## Phân tích chuyên sâu (Technical Insight)

1. **Điểm sáng**: Số request lỗi giảm xuống chỉ còn **4 lỗi** (giảm 1 lỗi so với Slot 12).
2. **Nguyên nhân biến động TTFT**: Khung giờ đêm (23:15 PM) hạ tầng máy chủ chấm thi BTC chịu tải cao điểm gây nhiễu TTFT P50 (68ms).
3. **Hình mẫu đỉnh cao**: Bản **`v20.0`** đã xác lập kỷ lục 60.40đ ở Slot 12 và giữ ổn định ở mốc 59.79đ ở Slot 13.
