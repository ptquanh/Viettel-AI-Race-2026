# Kết Quả Thử Nghiệm 1414 (Slot 9 - 20/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1414`
- **File Compose**: `1414-docker-compose.yml`
- **Thời gian chấm**: 20/07/2026 14:14
- **Cấu hình**: Image v5.1 (Deep Triton Kernel Fusion - RMSNorm + Conv1D + SiLU) + Golden Base (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `54.13`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `54.13`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `72 ms`
- **TTFT P95**: `96 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **TTFT P50 tăng mạnh lên 72ms**: Việc gộp toán tử Conv1D vào Triton Kernel làm phát sinh thêm overhead JIT compile dynamic shape trong quá trình warmup prefill, kéo trễ TTFT tăng từ 56ms (v5) lên 72ms.
2. **TPOT Median không đổi (4ms)**: Do overhead dynamic stride dispatch của Triton kernel làm triệt tiêu phần tiết kiệm tính toán trên LFM2.5 Recurrent state.
3. **Đánh giá chiến lược**: Image v4.1 (Golden Base - 61.11đ) và Image v5 (v5 Baseline - 59.80đ) là 2 phiên bản ổn định nhất. Khuyên dùng Image v4.1 / v5 cho các lượt Re-run săn kỷ lục vào khung giờ vàng (Slots 10-15).
