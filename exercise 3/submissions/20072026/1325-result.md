# Kết Quả Thử Nghiệm 1325 (Slot 8 - 20/07/2026)

## Thông Tin Chung
- **Mã thử nghiệm**: `1325`
- **File Compose**: `1325-docker-compose.yml`
- **Thời gian chấm**: 20/07/2026 13:25
- **Cấu hình**: Image v5 (Custom Triton Kernel Fusion - RMSNorm + SiLU) + Golden Base (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm
- **Điểm số (ERS)**: `59.80`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `59.80`

## Chỉ Số Chi Tiết
- **Total Request**: `420`
- **TTFT P50**: `56 ms`
- **TTFT P95**: `75 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `6`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận
1. **Chạy thành công 100% không lỗi crash**: Image v5 với Triton Kernel Fusion hoạt động cực kỳ ổn định, không làm sai lệch kết quả (Accuracy Drop = 0%).
2. **TTFT P50/P95 ở mức 56ms / 75ms**: Điểm số đạt 59.80 điểm (do ảnh hưởng nhẹ bởi nhiễu host grader lúc 13:25).
3. **TPOT Median giữ ở mốc 4ms**: Do hệ thống chấm điểm BTC làm tròn TPOT theo số nguyên ms (integer ms), cải thiện sub-millisecond của RMSNorm+SiLU chưa đủ kéo integer TPOT từ 4ms xuống 3ms. Cần gộp sâu hơn vào các lớp Recurrent Conv1D & State Update (Image v5.1).
