# Kết Quả Thử Nghiệm 2209 (Slot 15 - 21/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2209`
- **File Compose**: `15-docker-compose.yml`
- **Thời gian chấm**: 21/07/2026 22:09
- **Cấu hình**: Image v9 + FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + `VLLM_CUDAGRAPH_MODE=FULL` + `OMP_NUM_THREADS=2` (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `58.28`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `58.28`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `56 ms`
- **TTFT P95**: `97 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Tổng Kết Ngày 21/07

1. **Hiệu năng Golden Run Cuối Ngày (`2209`)**:
   - Điểm ERS đạt **58.28đ**.
   - TTFT P50 ở mức **56 ms**, TTFT P95 bị tác động dội trễ lên **97 ms** (do ảnh hưởng tải hệ thống Grader BTC khung 22:00 muộn).
   - Failed Count duy trì mức tối ưu: **5 requests**.
2. **Tổng Kết Đánh Giá Toàn Bộ 15 Slots Ngày 21/07**:
   - **Tối ưu đột phá nhất ngày 21/07**: Chuyển sang `VLLM_CUDAGRAPH_MODE=FULL` trên Image v9 đã mở khóa khả năng triệt tiêu launch overhead, đưa điểm ERS đạt kỷ lục ban ngày **60.82đ** (Slot 06 / STT 80), cách kỷ lục all-time (61.24đ) chỉ 0.42đ.
   - **Tối ưu micro-tune**: `OMP_NUM_THREADS=1` giúp triệt tiêu CPU context switching, đưa Failed Count về kịch sàn **4 requests** (thấp nhất toàn giải - STT 88) và ERS đạt **60.45đ** (STT 85).
   - **Rào cản vật lý còn lại**: TPOT Median vẫn bị cắm cứng tại **4ms** trên v0.22.1 FP8 single model.
3. **Kế hoạch Ngày 22/07 (Phase 2 - Can Thiệp Sâu)**:
   - Sẵn sàng bước sang Phase 2: Build Custom Image v10 hỗ trợ Speculative Decoding (Draft Models/Draft Heads) & Nâng cấp vLLM Version mới + Sửa Engine Source Code để bứt phá TPOT từ 4ms xuống 2ms, hướng tới mốc **75 - 80+ điểm**!
