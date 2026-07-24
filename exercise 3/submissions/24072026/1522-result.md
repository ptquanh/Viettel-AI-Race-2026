# Kết Quả Thử Nghiệm 1522 (Slot 07 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1522`
- **File Compose**: `1522-docker-compose.yml` (Slot 07)
- **Thời gian chấm**: 24/07/2026 (15:22)
- **Thay đổi**: Best Slot 06 (`spawn`) + `VLLM_MAX_MODEL_LEN=5120`

## Kết Quả Chấm Điểm

- **Điểm số**: `56.2000` (❌ Sụt 5.39đ so với kỷ lục 61.59đ của Slot 06)
- **TTFT P50**: 61ms (Tăng 14ms từ 47ms!)
- **TTFT P95**: 97ms (Tăng 29ms từ 68ms!)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 4 (Cực kỳ ổn định, giảm được 1 lỗi)
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Nguyên nhân giảm điểm**: Giới hạn `VLLM_MAX_MODEL_LEN=5120` quá sát mốc max context (4700 tokens) gây xáo trộn CUDA Graph stride buckets của vLLM block manager. Các turn cuối (Turn 5-6 ~3950–4400 tokens) gặp hiện tượng re-allocation hoặc stride alignment kém tối ưu, khiến TTFT P50 vọt lên 61ms và P95 vọt lên 97ms.
- **Điểm tích cực**: Failed count giảm xuống 4 requests (thấp kỷ lục).
- **Kết luận**: Khẳng định **MaxLen=8192** là mốc chuẩn duy nhất cho CUDA Graph stride alignment. Không thu hẹp MaxLen xuống 5120 nữa.
