# Kết Quả Thử Nghiệm 0000 (Slot 15 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0000`
- **File Compose**: `0000-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 00:00
- **Cấu hình**: Image v8 (Flash-Linear-Attention Edition) + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.96` + `CUDA_DEVICE_MAX_CONNECTIONS=1` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `60.07`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `60.07`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `51 ms`
- **TTFT P95**: `79 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Phân tích hiệu năng Image v8 (FLA + GPU_MEM=0.96)**:
   - TTFT P50 tăng lên 51ms và TTFT P95 vọt lên 79ms, dẫn đến điểm ERS giảm về 60.07đ.
   - Nguyên nhân kép:
     a) Cấu hình thừa hưởng `GPU_MEM=0.96` từ Slot 14 vốn đã bị chèn trễ do VRAM allocation.
     b) Việc nộp bài vào nửa đêm 00:00 (lúc hàng loạt đội cùng nộp bài tự động chốt slot ngày) làm tăng đáng kể nhiễu tải hệ thống Grader BTC (Failed count vọt lên 7 requests).
2. **Khẳng định chiến lược**:
   - Mốc kỷ lục **61.24 điểm (Slot 13 - 1945)** dùng **Image v7 Lean + FlashInfer + `block-size=32` + `GPU_MEM=0.95`** tiếp tục là baseline tối ưu nhất.
   - Rút kinh nghiệm: Cần giữ nguyên `GPU_MEM=0.95` và né khung giờ tròn giờ (như 00:00) khi các bot thi đấu tập trung nộp dồn dập.
