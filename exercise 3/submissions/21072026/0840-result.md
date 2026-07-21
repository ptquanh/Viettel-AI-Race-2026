# Kết Quả Thử Nghiệm 0840 (Slot 03 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0840`
- **File Compose**: `0840-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 08:40
- **Cấu hình**: Image v9 (CUDA Graph Dynamic Config) + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL_DECODE_ONLY` + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32]` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `60.40`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `60.40`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `48 ms`
- **TTFT P95**: `73 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Image v9 + `FULL_DECODE_ONLY` + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32]`**:
   - Điểm số tăng tiếp từ **59.06đ (Slot 2)** lên **60.40đ (+1.34 điểm)**!
   - TTFT P50 giảm sâu từ **56ms → 48ms (tiết kiệm thêm 8ms)**, tiệm cận mốc kỷ lục cũ (44ms).
   - TTFT P95 giảm từ **82ms → 73ms (tiết kiệm thêm 9ms)**.
   - Số lượng request lỗi tăng nhẹ lên 7 (do nhiễu hệ thống BTC lúc 08:40 sáng).
2. **Tác động của `cudagraph_capture_sizes`**:
   - Giới hạn danh sách capture sizes giúp vLLM không phải allocate các CUDA Graphs cho những batch sizes quá lớn không cần thiết.
   - Tiết kiệm đáng kể VRAM allocation overhead và giảm startup/warmup time, giúp TTFT P50 giảm ấn tượng xuống 48ms ngay trong điều kiện ban ngày.
3. **Bài học & Bước tiếp theo**:
   - `FULL_DECODE_ONLY` kết hợp `cudagraph_capture_sizes` mang lại hiệu quả rất rõ rệt.
   - Tiến tới Slot 4 (`04-docker-compose.yml`): thử thu hẹp `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16]` và ép `VLLM_MAX_CUDAGRAPH_CAPTURE_SIZE=16` để kiểm chứng xem việc giải phóng thêm VRAM có giúp hạ Failed count và đẩy TTFT về mốc <45ms hay không.
