# Kết Quả Thử Nghiệm 0828 (Slot 02 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0828`
- **File Compose**: `0828-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 08:28
- **Cấu hình**: Image v9 (CUDA Graph Dynamic Config) + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL_DECODE_ONLY` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `59.06`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `59.06`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `56 ms`
- **TTFT P95**: `82 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Hiệu năng Image v9 + `VLLM_CUDAGRAPH_MODE=FULL_DECODE_ONLY`**:
   - Điểm số tăng mạnh từ **54.73đ** (Slot 1) lên **59.06đ** (**+4.33 điểm**).
   - TTFT P50 cải thiện đáng kể từ **71ms → 56ms** (giảm 15ms).
   - TTFT P95 cải thiện từ **96ms → 82ms** (giảm 14ms).
   - Số lượng request lỗi giữ nguyên ở mức 5.
   - TPOT Median vẫn giữ ở mức 4ms.
2. **Đánh giá CUDA Graph**:
   - Chế độ `FULL_DECODE_ONLY` đã chứng minh hiệu quả rất rõ rệt khi cải thiện TTFT P50/P95 đáng kể trong cùng một điều kiện host grader bị nghẽn tải vào buổi sáng (Failed=5).
   - Việc chỉ capture CUDA Graph cho phase decode giúp loại bỏ triệt để overhead khởi tạo/lập lịch CPU cho decode loops, làm giảm áp lực luồng CPU và gián tiếp giảm thời gian xử lý prefill (TTFT).
3. **Bài học**:
   - CUDA Graph hoạt động cực tốt và ổn định. Chúng ta sẽ tiếp tục tiến tới Slot 3 (`03-docker-compose.yml`) để tối ưu hóa bộ nhớ CUDA Graph thông qua việc giới hạn `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32]`.
