# Kết quả Benchmark - Slot 1148 (Fusion Humming W4 + INT4 Marlin + FP8 KV Cache)

- **Cấu hình**: `docker-compose.fusion-humming-int4-fp8kv.submission.yml`

## Kết quả chi tiết (Slot 1148)
- **Điểm chung cuộc (ERS / Final Score)**: **67.6100**
- **TTFT P50**: **45ms**
- **TTFT P95**: **69ms**
- **TBT Median (TPOT)**: **3ms**
- **Failed Count**: **4** / 420 (Giảm được 2 request thất bại so với slot 0851!)
- **Warmup Count**: 0
- **Accuracy Drop**: 0
- **Tokens/sec**: 0.0497

## Nhận xét & Đánh giá
- **Độ ổn định tăng**: Số request thất bại giảm từ 6 xuống 4 (4/420), cho thấy việc kết hợp FP8 KV Cache giúp cải thiện độ ổn định bộ nhớ.
- **TTFT & TPOT**: TTFT P50 tăng nhẹ 2ms (từ 43ms lên 45ms), P95 tăng nhẹ 2ms (từ 67ms lên 69ms), TPOT duy trì 3ms.
- **Điểm ERS (67.61)**: Rất tiệm cận kỷ lục 68.38, khẳng định hướng kết hợp fusion có tính ổn định cao.
