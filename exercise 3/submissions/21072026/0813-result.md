# Kết Quả Thử Nghiệm 0813 (Slot 01 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0813`
- **File Compose**: `0813-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 08:13
- **Cấu hình**: Image v9 (CUDA Graph Dynamic Config) + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` (`32K`, `Seqs=32`, `Level 3`, không set thêm CUDA Graph env vars để đối chứng baseline)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `54.73`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `54.73`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `71 ms`
- **TTFT P95**: `96 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Image v9 (Baseline đối chứng)**:
   - Điểm ERS sụt giảm còn **54.73** với TTFT P50 tăng mạnh lên **71ms** và TTFT P95 lên **96ms**.
   - Mặc dù cấu hình tương đương hoàn toàn với kỷ lục **61.24đ (Slot 13 - 1945)** của Image v7, nhưng kết quả kém hẳn.
2. **Nguyên nhân cốt lõi**:
   - **Lịch chạy**: Chạy lúc 08:13 sáng — đây là thời điểm hệ thống host của BTC bắt đầu chịu tải cực lớn từ các đội tham gia hoạt động ban ngày.
   - **Đánh giá JIT Warmup**: Image v9 Lean không có cơ chế Deep Warmup mà chỉ có Primer Warmup tự nhiên. Việc bị cạnh tranh tài nguyên CPU/GPU vật lý lúc khởi động ở thời điểm tải cao khiến PyTorch JIT compile mất nhiều thời gian hơn và trễ TTFT bị đội lên rất cao (71ms).
   - Số lượng requests failed vẫn ở mức 5, phản ánh đúng tình trạng quá tải/nhiễu hệ thống BTC lúc buổi sáng.
3. **Bài học**:
   - Cần tiếp tục test các slot tiếp theo mang tính chất so sánh tương đối trực tiếp trong cùng buổi sáng (để loại trừ noise thời gian và so sánh hiệu năng thực tế của các cấu hình CUDA Graph).
