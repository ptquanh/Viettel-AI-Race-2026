# Kết Quả Thử Nghiệm 2126 (Slot 07 - 23/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2126`
- **File Compose**: `07-docker-compose.yml` (Slot 07)
- **Thời gian chấm**: 23/07/2026
- **Cấu hình**: Image v13 (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v13`) + PyTorch Profiler được inject vào hàm `LFMForCausalLM.forward`.

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `58.88`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `58.88`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `59 ms`
- **TTFT P95**: `77 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `6`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`

## Phân Tích & Kết Luận

1. **Hiệu năng không bị ảnh hưởng**:
   - Dù ta đã chèn PyTorch Profiler hook vào bên trong, hệ thống vẫn vượt qua bài test trót lọt với điểm 58.88.
   - Thậm chí việc profile từ step 10 đến 15 không gây phình TTFT quá lớn, TPOT vẫn giữ nguyên 4ms.
2. **Vấn đề trích xuất Log**:
   - Mục đích chính của Slot 07 KHÔNG PHẢI là lấy điểm, mà là lấy được **Bảng thống kê CUDA Time** từ PyTorch Profiler được in ra `stderr`.
   - Cần xác nhận xem Portal có trả về log chi tiết (stdout/stderr) cho các submission PASS hay không. Nếu không, ta phải làm nó FAIL có chủ đích.
