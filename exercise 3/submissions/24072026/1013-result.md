# Kết Quả Thử Nghiệm 1013 (Slot 03 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1013`
- **File Compose**: `03-docker-compose.yml` (Slot 03)
- **Thời gian chấm**: 24/07/2026 (10:13)
- **Thay đổi**: Image v14 FP8 + `VLLM_COMPILATION_LEVEL=2`

## Kết Quả Chấm Điểm

- **Điểm số**: `54.8100` (Giảm -5.18đ so với mốc 59.99đ của Slot 02)
- **TTFT P50**: 65ms (Tăng 11ms từ 54ms)
- **TTFT P95**: 93ms (Tăng 18ms từ 75ms)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 6
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Compilation Level 2 Kém Hơn**: Hạ `VLLM_COMPILATION_LEVEL` từ 3 xuống 2 đã tắt một số tối ưu PyTorch Inductor JIT / CUDA Graph sâu, dẫn đến tăng overhead khi thực thi prefill.
- TTFT P50 tăng vọt từ 54ms lên 65ms và TTFT P95 tăng lên 93ms.
- **Kết luận**: Khẳng định `VLLM_COMPILATION_LEVEL=3` (mặc định) là bắt buộc. Giữ nguyên Level 3 cho các slot tiếp theo.
