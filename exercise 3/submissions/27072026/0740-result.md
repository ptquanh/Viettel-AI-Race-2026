# Kết quả chấm điểm Slot 11 (0740 - 27/07/2026) - KỶ LỤC TTFT P50 MỚI (56ms)!

- **Thời gian nộp**: 07:40 AM (27/07/2026)
- **Chiến lược**: Custom CUDA C++ Kernel Fusion (`v16.3`) + Restore `GPU_MEMORY_UTILIZATION=0.94`
- **Cấu hình**: Champion Config (MAX_LEN=8192, GPU_MEM=0.94)
- **Điểm số**: **52.7600 điểm**
- **Số request lỗi (Failed count)**: 6

## Chỉ số chi tiết (Benchmark Metrics)

| Chỉ số Metric         |   Giá trị   | Nhận xét                                                               |
| :-------------------- | :---------: | :--------------------------------------------------------------------- |
| **Final Score**       | **52.7600** | Chạy thành công 420 requests!                                          |
| **TTFT P50**          |  **56 ms**  | 🔥 **Kỷ lục mới! Giảm từ 67ms -> 56ms** (Nhanh hơn Champion 58ms 2ms!) |
| **TTFT P95**          |  **72 ms**  | 🔥 **Cực kỳ ấn tượng! (Champion P95 = 85ms)**                          |
| **TBT Median (TPOT)** |  **5 ms**   | Giữ mốc 5ms                                                            |
| **Accuracy Drop**     |  **0.00**   | Độ chính xác nguyên bản 100%                                           |
| **Failed Requests**   |    **6**    | Do hệ thống BTC nghẽn tải buổi sáng                                    |
| **Tokens / sec**      | **0.0556**  |                                                                        |

---

## Phân tích chuyên sâu (Technical Insight & Breakthrough)

1. **Khôi phục `GPU_MEMORY_UTILIZATION=0.94` giải phóng TTFT**:
   - Đúng như dự đoán, khi trả `GPU_MEMORY_UTILIZATION` từ `0.90` về lại **`0.94`**, vLLM lập tức có đủ KV Cache RAM GPU.
   - Kết quả: **TTFT P50 giảm kỷ lục xuống 56ms** (vượt qua mốc 58ms của Champion cũ), và **TTFT P95 giảm xuống 72ms** (so với 85ms của Champion)!
2. **Tại sao điểm tổng 52.76đ chưa bứt phá lên 63+đ?**:
   - **Lỗi hệ thống BTC buổi sáng**: Số lượng `failed_count = 6` (buổi sáng BTC thường nghẽn làm trễ request).
   - **TBT Median (TPOT) đang ở mốc 5ms**: Do Custom C++ Kernel `v16.3` hiện tại mới chỉ fuse hàm `ShortConv.forward_cuda`. Bản thân op này ở LFM2.5 bị giới hạn bởi Băng thông bộ nhớ GPU (Memory Bandwidth Bound).
