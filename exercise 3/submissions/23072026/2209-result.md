# Kết Quả Thử Nghiệm 2209 (Slot 09 - 23/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2209`
- **File Compose**: `09-docker-compose.yml` (Slot 09)
- **Thời gian chấm**: 23/07/2026 (22:09)
- **Thay đổi**: v12 + `VLLM_MAX_NUM_SEQS=64`

## Kết Quả Chấm Điểm

- **Điểm số**: `55.7500`
- **TTFT P50**: 64ms
- **TTFT P95**: 99ms
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- Tăng `VLLM_MAX_NUM_SEQS` từ 32 lên 64 khiến TTFT P50 tăng vọt từ 58ms lên 64ms và P95 tăng lên 99ms do gia tăng tranh chấp hàng đợi scheduler và GPU compute khi prefill.
- Điểm ERS sụt giảm từ 58.79đ xuống 55.75đ (-3.04đ).
- **Kết luận**: Khẳng định mốc `VLLM_MAX_NUM_SEQS=32` là điểm ngọt (sweet-spot) tối ưu nhất cho kiến trúc LFM 1.2B.
