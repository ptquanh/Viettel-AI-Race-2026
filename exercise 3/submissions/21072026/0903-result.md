# Kết Quả Thử Nghiệm 0903 (Slot 05 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0903`
- **File Compose**: `0903-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 09:03
- **Cấu hình**: Image v9 (CUDA Graph Dynamic Config) + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `60.82`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `60.82`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `47 ms`
- **TTFT P95**: `69 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Image v9 + `VLLM_CUDAGRAPH_MODE=FULL`**:
   - Điểm ERS bứt phá lên **60.82đ** (cao nhất trong ngày hôm nay, chỉ cách kỷ lục all-time 61.24đ đúng 0.42đ dù nộp vào buổi sáng ban ngày nghẽn tải!).
   - TTFT P50 đạt **47 ms** (rất gần mốc 44ms kỷ lục).
   - TTFT P95 đạt **69 ms** (mốc trễ đuôi thấp nhất trong ngày!).
   - Failed Count giảm về **5 requests** (mốc tối ưu nhất của hệ thống Grader BTC ban ngày).
2. **Đánh giá về Full CUDA Graph (`FULL`)**:
   - `cudagraph_mode: FULL` (capture toàn bộ forward pass cho cả prefill và decode) đem lại hiệu năng vượt trội hơn hẳn so với `FULL_DECODE_ONLY`.
   - Giúp giảm triệt để launch overhead trên cả 2 pha, ép TTFT P95 xuống kịch sàn 69ms.
3. **Bài học & Bước tiếp theo**:
   - Cấu hình `VLLM_CUDAGRAPH_MODE=FULL` hoàn toàn ổn định trên LFM2.5 + FlashInfer mà không bị crash/OOM.
   - Tiến tới Slot 6 (`06-docker-compose.yml`): kết hợp `VLLM_CUDAGRAPH_MODE=FULL` với danh sách capture sizes tối ưu `[1,2,4,8,16,32]` để xem có bứt phá phá kỷ lục 61.24đ ngay trong buổi sáng hay không!
