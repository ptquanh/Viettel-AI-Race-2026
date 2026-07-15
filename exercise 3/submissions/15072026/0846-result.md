# Kết quả Benchmark - 15/07/2026 (STT 105 - slot 0846 - Async Output=OFF)

- **Cấu hình**: Seqs=24, Chunk=16384, OMP=3, Warmup=ON, Custom Kernel=ON, **VLLM_DISABLE_ASYNC_OUTPUT=1**.
- **Mục đích**: Tắt xử lý async output để kiểm tra xem việc giảm overhead thread coordination có giúp tối ưu TPOT hay không.

## Chỉ số đo được

- **Điểm số**: **Chấm điểm thất bại** (Grader failed)
- **Lý do**: Container khởi động thất bại (inference container exited with code 2).

## Phân tích kết quả

1. **Lỗi đối số dòng lệnh không hợp lệ (Unrecognized arguments)**:
   - File log từ Grader chỉ ra lỗi: `api_server.py: error: unrecognized arguments: --disable-async-output-proc`.
   - Điều này xảy ra do entrypoint wrapper script của image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` tự động phát hiện biến môi trường `VLLM_DISABLE_ASYNC_OUTPUT=1` và cố gắng thêm tham số `--disable-async-output-proc` vào câu lệnh khởi chạy vLLM API Server.
   - Tuy nhiên, phiên bản vLLM cài đặt trong runtime image không hỗ trợ tham số này (đã bị gỡ bỏ hoặc thay đổi cú pháp trong mã nguồn vLLM gốc), làm API server crash ngay lập tức.
2. **Kết luận**:
   - Không thể sử dụng biến môi trường `VLLM_DISABLE_ASYNC_OUTPUT=1` với image runtime hiện tại. Chúng ta bắt buộc phải để async output hoạt động ở trạng thái mặc định (mở).
