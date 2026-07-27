# Kết quả chấm điểm Slot 10 (1358 - 27/07/2026) - KỶ LỤC TTFT P95 MỚI (78ms) & ĐIỂM SỐ 59.39đ

- **Thời gian nộp**: 01:58 PM (27/07/2026)
- **Chiến lược**: Triton JIT Kernel Fusion (`v18.0`) + Golden VRAM (`GPU_MEM=0.95`)
- **Cấu hình**: Image `v18.0` + `GPU_MEM=0.95` + `MAX_LEN=32768` + `SEQS=32` + `WARMUPS=10`
- **Điểm số**: **59.3900 điểm** (Đạt phong độ đỉnh cao, 100% Accuracy Drop!)
- **Số request lỗi (Failed count)**: 5

## Chỉ số chi tiết (Benchmark Metrics)

| Chỉ số Metric         |   Giá trị   | Nhận xét                                                        |
| :-------------------- | :---------: | :-------------------------------------------------------------- |
| **Final Score**       | **59.3900** | Duy trì mốc điểm đỉnh cao tiệm cận 60đ!                         |
| **TTFT P50**          |  **55 ms**  | 🔥 Nhanh cực đại (suýt soát kỷ lục 54ms ở Slot 06)!             |
| **TTFT P95**          |  **78 ms**  | 🔥 **KỶ LỤC TTFT P95 MỚI TOÀN GIẢI! (Giảm từ 80ms xuống 78ms)** |
| **TBT Median (TPOT)** |  **4 ms**   | Giữ vững mốc 4ms chuẩn                                          |
| **Accuracy Drop**     |  **0.00**   | Độ chính xác nguyên bản 100%                                    |
| **Failed Requests**   |    **5**    | Ổn định                                                         |
| **Tokens / sec**      | **0.0551**  |                                                                 |

---

## Phân tích chuyên sâu (Technical Insights)

1. **Khẳng định bộ khung Golden Setup của `v18.0`**:
   - `SEQS=32` + `WARMUPS=10` + `32k Context` + `Triton Kernel` tạo ra sự ổn định tuyệt đối.
   - Trễ đuôi **TTFT P95 giảm kịch sàn xuống 78ms** (thấp nhất từ đầu giải tới giờ).

2. **Xác định giới hạn và Bước ngoặt chiến lược**:
   - Với việc chỉ fuse riêng `ShortConv`, TPOT giữ ở 4ms mang lại mốc điểm tối đa **~59.70đ - 60.00đ**.
   - Để phá vỡ giới hạn này và vọt lên **80 - 90+ điểm** ở các Slot cuối ngày, ta bắt buộc phải nâng cấp lên **`v19.0` Triton Full Layer Fusion (`InProj + ShortConv + OutProj`)** để ép TPOT giảm 50% từ 4ms xuống **`< 2 ms`**!
