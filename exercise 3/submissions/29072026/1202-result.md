# Kết quả Benchmark - Trưa 30/07/2026 (Slot 1202 - r5-int4-fast)

- **Cấu hình**: `r5-int4-fast` (INT4 Fast Mode / Quantization)

## Kết quả chi tiết (Slot 1202)
- **Điểm chung cuộc (ERS / Final Score)**: **67.9700** 🔥 **(KỶ LỤC MỚI!)**
- **TTFT P50**: 43ms
- **TTFT P95**: 94ms
- **TBT Median (TPOT)**: **3ms** 🔥 (Đột phá phá vỡ mức kẹt 4ms xuống 3ms!)
- **Failed Count**: 6 / 420
- **Accuracy Drop**: 0%
- **Tokens/sec**: 0.0512

## Nhận xét & Đột phá kỹ thuật
- **Ép TPOT xuống 3ms**: Cấu hình `r5-int4-fast` đã chính thức bẻ gãy giới hạn vật lý 4ms của FP8, đưa trễ sinh token (TPOT) về **3ms**.
- **Kỷ lục 67.97 ERS**: Tăng gần +4.6 điểm so với kỷ lục 63.36 trước đó.
- Đây chính là mảnh ghép quan trọng cho mục tiêu tiệm cận 80.0 ERS!
