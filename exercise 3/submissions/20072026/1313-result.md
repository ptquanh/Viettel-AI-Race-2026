# Kết Quả Thử Nghiệm 1313 (Slot 7 - 20/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1313`
- **File Compose**: `1313-docker-compose.yml`
- **Thời gian chấm**: 20/07/2026 13:13
- **Cấu hình**: Image v4.1 + `TORCHINDUCTOR_MAX_AUTOTUNE=1` + `TORCHINDUCTOR_FX_GRAPH_CACHE=1`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `57.41`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `57.41`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `64 ms`
- **TTFT P95**: `87 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Trễ TTFT P50 tăng từ 51ms lên 64ms**: Cờ `TORCHINDUCTOR_MAX_AUTOTUNE=1` khiến PyTorch Inductor thử nghiệm nhiều kernel variants on-the-fly, gây ra overhead compilation phụ khi nhận request đầu tiên của từng context shape.
2. **TPOT vẫn giữ 4ms**: Autotuning của Inductor không thể hạ TPOT từ 4ms xuống 3ms do không thay đổi được số lượng kernel launches per layer trong kiến trúc LFM2.5.
3. **Khẳng định**: Tắt Max Autotune (`TORCHINDUCTOR_MAX_AUTOTUNE=0`), không sử dụng cờ này trong cấu hình chính thức.
