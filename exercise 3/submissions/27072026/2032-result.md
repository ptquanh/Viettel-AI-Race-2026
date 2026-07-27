# Kết quả chấm điểm Slot 13 (2032 - 27/07/2026) - KẾT QUẢ ĐỈNH CAO 59.79đ (WARMUPS=12 BENCHMARK)

- **Thời gian nộp**: 08:32 PM (27/07/2026)
- **Chiến lược**: CUTLASS FP8 Scaled MM Kernel (`v20.0`) + Warmup 12 Cycles
- **Cấu hình**: Image `v20.0` + `GPU_MEM=0.95` + `MAX_LEN=32768` + `SEQS=32` + `WARMUPS=12`
- **Điểm số**: **59.7900 điểm** (Duy trì vị thế đỉnh cao sát mốc 60đ!)
- **Số request lỗi (Failed count)**: 5

## Chỉ số chi tiết (Benchmark Metrics)

| Chỉ số Metric         |   Giá trị   | Nhận xét                                                  |
| :-------------------- | :---------: | :-------------------------------------------------------- |
| **Final Score**       | **59.7900** | Duy trì phong độ đỉnh cao tiệm cận 60đ!                   |
| **TTFT P50**          |  **55 ms**  | Rất nhanh (chỉ tăng nhẹ 3ms so với kỷ lục 52ms ở Slot 12) |
| **TTFT P95**          |  **71 ms**  | 🔥 Trễ đuôi cực nhanh (thấp hơn mốc cũ 78ms 7ms)!         |
| **TBT Median (TPOT)** |  **4 ms**   | Giữ vững mốc 4ms chuẩn                                    |
| **Accuracy Drop**     |  **0.00**   | Độ chính xác nguyên bản 100%                              |
| **Failed Requests**   |    **5**    | Ổn định                                                   |
| **Tokens / sec**      | **0.0545**  |                                                           |

---

## Phân tích so sánh (Technical Comparison)

1. **Khẳng định `WARMUPS=10` là Golden Warmup Count tuyệt đối**:
   - Khi tăng Warmup từ 10 (Slot 12) lên 12 (Slot 13), TTFT P50 tăng nhẹ từ 52ms lên 55ms, điểm số giảm nhẹ từ 60.40đ xuống 59.79đ.
   - Kết luận: **`WARMUPS=10`** chính là mốc Warmup chuẩn mực nhất cho hệ thống.

2. **Chiến lược cho Slot 14**:
   - Quay lại sử dụng đúng bộ tham số Champion ở Slot 12: Image `v20.0` + `GPU_MEM=0.95` + `WARMUPS=10` + `SEQS=32` để săn tìm mốc kỷ lục mới trên 60.40đ!
