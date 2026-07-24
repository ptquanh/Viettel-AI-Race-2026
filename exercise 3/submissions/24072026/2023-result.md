# Kết Quả Thử Nghiệm 2023 (Slot 11 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2023`
- **File Compose**: `2023-docker-compose.yml` (Slot 11)
- **Thời gian chấm**: 24/07/2026 (20:23)
- **Thay đổi**: Golden Config + Full Micro-env combo (`TOKENIZERS_PARALLELISM=false`, `VLLM_NO_USAGE_STATS=1`, `MALLOC_TRIM_THRESHOLD_=0`, `LOGGING_LEVEL=ERROR`)

## Kết Quả Chấm Điểm

- **Điểm số**: `58.5700` (❌ Giảm 2.54đ so với 61.11đ của Slot 20:12)
- **TTFT P50**: 59ms (Tăng +11ms từ 48ms của Slot 20:12!)
- **TTFT P95**: 78ms (Tăng +5ms từ 73ms!)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Nguyên nhân sụt giảm hiệu năng**:
  1. `MALLOC_TRIM_THRESHOLD_=0`: Ép glibc `malloc` phải gọi system calls (`brk`/`sbrk`/`madvise`) trả bộ nhớ ngay lập tức về OS mỗi khi giải phóng VRAM/RAM. Điều này tạo ra syscall overhead cực kỳ nặng trên CPU khi vLLM phân bổ và giải phóng memory blocks liên tục, kéo TTFT P50 tăng vọt từ 48ms lên **59ms**.
  2. Việc ép thêm quá nhiều biến môi trường chưa qua kiểm chứng đơn biến gây tác dụng ngược lên CPU scheduler.
- **Kết luận**:
  - **LOẠI BỎ NGAY `MALLOC_TRIM_THRESHOLD_=0`**.
  - Giữ lại cấu hình chiến thắng của Slot 20:12 (`GPU_MEM=0.94` + `VLLM_WORKER_MULTIPROC_METHOD=spawn` + `FLASHINFER` + `BLOCK_SIZE=32`) cho các đợt Golden Runs tiếp theo!
