# Kết quả Benchmark - 09:12 18/07/2026 (STT 33 - Slot 3 - Custom Image + Compile Level 2 - FAILED)

- **Cấu hình**: Custom Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--compilation-config={"level":2}` + `--no-enable-log-requests` + `--disable-log-stats`.
- **Mục đích**: Đánh giá hiệu năng và tính ổn định của cơ chế biên dịch `torch.compile` level 2 trên nền Custom Image.

## Trạng thái chấm điểm

- **Kết quả**: **FAILED** (Thất bại)
- **Lý do lỗi**: `job exceeded max duration of 2700s with no terminal callback` (Container bị treo/deadlock hoặc mất quá nhiều thời gian khởi chạy dẫn đến vượt quá giới hạn 45 phút của Grader).

## Phân tích kết quả & Khắc phục

1. **Nguyên nhân lỗi treo (Timeout)**:
   - Cơ chế biên dịch `torch.compile` với `level 2` (biên dịch một phần đồ thị) có thể gặp lỗi deadlock hoặc vòng lặp biên dịch vô hạn (infinite compilation loop) trong vLLM/PyTorch khi tối ưu recurrent layers của LFM2.5.
   - Trái ngược với `level 3` chạy cực tốt (60.91 điểm) nhờ cơ chế gộp CUDA Graphs toàn diện, `level 2` tạo ra các phân mảnh đồ thị động không tối ưu, làm tràn hàng đợi hoặc treo luồng CPU/GPU lập lịch lúc nhận request warmup đầu tiên.

2. **Khuyến nghị hành động**:
   - Tránh hoàn toàn việc sử dụng `--compilation-config '{"level": 2}'` cho LFM2.5.
   - Nếu muốn dùng compile, hãy chọn hẳn `--compilation-config '{"level": 3}'` (đã chứng minh độ ổn định và tăng điểm vượt trội).
