# Kết Quả Thử Nghiệm 1945 (Slot 13 - 20/07/2026) — 🔥 KỶ LỤC MỚI 61.24 ĐIỂM!

## Thông Tin Chung

- **Mã thử nghiệm**: `1945`
- **File Compose**: `1945-docker-compose.yml`
- **Thời gian chấm**: 20/07/2026 19:45
- **Cấu hình**: FlashInfer Backend + `VLLM_BLOCK_SIZE=32` + `CUDA_DEVICE_MAX_CONNECTIONS=1` + Image v7 Lean (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `61.24` 🔥 **KỶ LỤC MỚI CAO NHẤT TOÀN ĐỘI!**
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `61.24` (Phá kỷ lục cũ 61.13đ)

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `44 ms` 🔥 **Kỷ lục trễ thấp nhất từ trước tới nay!**
- **TTFT P95**: `74 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `4` (Thấp kỷ lục!)
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **XÁC NHẬN HOÀN TOÀN GIẢ THUYẾT KỸ THUẬT**:
   - Tổ hợp **FlashInfer Backend + `block-size=32`** đã căn chỉnh tối ưu bộ nhớ PagedAttention KV Cache theo chuẩn 128-byte cache line của GPU NVIDIA H200.
   - Trễ prefill TTFT P50 chính thức bị đánh gục xuống **44ms** (kỷ lục cũ là 46ms).
2. **Khắc phục lỗi triệt để**: Cờ `CUDA_DEVICE_MAX_CONNECTIONS=1` cùng với Image v7 Lean giữ nguyên số failed count ở mức **4 requests** (mốc thấp kỷ lục).
3. **Ý nghĩa bứt phá**: Đây là minh chứng rõ ràng cho việc căn chỉnh kiến trúc phần cứng GPU H200 (Cache alignment) mang lại hiệu quả vượt trội.
