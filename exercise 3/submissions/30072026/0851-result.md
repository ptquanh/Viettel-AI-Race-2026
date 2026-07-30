# Kết quả Benchmark - Sáng 30/07/2026 (Slot 0851 - r14-humming-w4-channel-bf16-fp8-v2)

- **Cấu hình**: `r14-humming-w4-channel-bf16-fp8-v2` (Humming W4 Channel-wise + BF16 + FP8 v2)

## Kết quả chi tiết (Slot 0851)
- **Điểm chung cuộc (ERS / Final Score)**: **68.3800** 🔥 **(KỶ LỤC TOÀN GIẢI MỚI!)**
- **TTFT P50**: **43ms**
- **TTFT P95**: **67ms** 🔥 (Giảm trễ đuôi P95 tuyệt đối từ 96ms xuống 67ms!)
- **TBT Median (TPOT)**: **3ms**
- **Failed Count**: 6 / 420
- **Accuracy Drop**: 0%
- **Tokens/sec**: 0.0497

## Nhận xét & Đột phá kỹ thuật
- **Ép trễ đuôi P95 xuống 67ms**: Cấu hình Humming W4 Channel-wise v2 giúp cắt giảm đáng kể độ trễ phân phối đuôi TTFT P95 (từ 96ms về 67ms) trong khi vẫn duy trì TTFT P50 = 43ms và TPOT = 3ms.
- **Kỷ lục mới 68.38 ERS**: Thiết lập mốc điểm cao nhất từ trước tới nay của toàn đội!
