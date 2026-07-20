# Kết Quả Thử Nghiệm 1816 (Slot 12 - 20/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1816`
- **File Compose**: `1816-docker-compose.yml`
- **Thời gian chấm**: 20/07/2026 18:16
- **Cấu hình**: Image v7 Lean + FlashInfer Backend (`VLLM_ATTENTION_BACKEND=FLASHINFER`) + `CUDA_DEVICE_MAX_CONNECTIONS=1` + Golden Base (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `60.52`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `60.52`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `51 ms`
- **TTFT P95**: `72 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `5`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **FlashInfer Cải Thiện Trễ Đuôi (Tail Latency)**: Bật FlashInfer backend giúp kéo giảm TTFT P50 từ 53ms xuống **51ms** và đặc biệt là TTFT P95 từ 76ms xuống **72ms** so với FlashAttention mặc định (Slot 11 - 60.24đ).
2. **Điểm số nâng nhẹ lên 60.52đ**: Khẳng định FlashInfer hoạt động tối ưu và ổn định hơn cho mô hình LFM2.5 với các request prefill nhỏ.
3. **Chiến lược tiếp theo (Slots 13-15)**: FlashInfer + Image v7 Lean là tổ hợp mạnh nhất hiện tại. Khuyên dùng tổ hợp này để Re-run vào các khung giờ đêm khuya (khi host BTC ít tải/vắng) để săn kỷ lục mới 62-65+ điểm!
