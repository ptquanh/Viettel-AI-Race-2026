# Kết Quả Thử Nghiệm 1534 (Slot 11 - 20/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1534`
- **File Compose**: `11-docker-compose.yml`
- **Thời gian chấm**: 20/07/2026 15:34
- **Cấu hình**: Image v7 Lean (Zero Warmup / Primer Only) + `CUDA_DEVICE_MAX_CONNECTIONS=1` + Golden Base (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `60.24`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `60.24`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `53 ms`
- **TTFT P95**: `76 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `4` (Thấp nhất từ trước đến nay!)
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Khẳng định tính ổn định của Image v7 Lean**: Việc bỏ hoàn toàn script warmup tự chế và phụ thuộc 100% vào 90 primer requests của BTC hoạt động hoàn hảo (đạt 60.24đ, 0 lỗi khởi động).
2. **Cờ `CUDA_DEVICE_MAX_CONNECTIONS=1` phát huy tác dụng**: Giảm thành công số request thất bại từ 6-7 xuống còn **4 requests** (mức thấp kỷ lục).
3. **TTFT P50 dao động ở 53ms**: Do không warmup trước các shape bucket bằng script python, 15 request đầu tiên hơi chậm nhẹ đẩy P50 lên 53ms (so với 46ms lúc host vắng).
4. **Hướng bứt phá tiếp theo (Slot 12)**: Thử nghiệm `VLLM_ATTENTION_BACKEND=FLASHINFER` trên nền Image v7 Lean để tối ưu tốc độ prefill của FlashAttention mặc định.
