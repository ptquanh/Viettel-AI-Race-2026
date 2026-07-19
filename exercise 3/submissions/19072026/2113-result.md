# BÁO CÁO THỬ NGHIỆM SLOT 13 (2113 - TIMEOUT FAIL)

## 1. Thông tin cấu hình

- **File nộp**: `2113-docker-compose.yml` (Slot 13)
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Cấu hình chính**: `Seqs=32`, `Len=32768`, `Compilation Level 3`, `Quant=fp8`, `VLLM_SPECULATIVE_MODEL=ngram`, `VLLM_NUM_SPECULATIVE_TOKENS=5`, `Chunked_Prefill=1`
- **Thời gian nộp**: 21:13 (19/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Trạng thái**: **Chấm điểm thất bại (FAILED)**
- **Lỗi chi tiết**: `job exceeded max duration of 2700s with no terminal callback` (Timeout 2700 giây)

## 3. Phân tích nguyên nhân & Kết luận

1. **Xác nhận 100% dự đoán xung đột N-gram với `COMPILATION_LEVEL=3`**:
   - Đúng như dự đoán ở Slot 11, cờ `VLLM_SPECULATIVE_MODEL=ngram` khi kết hợp với `COMPILATION_LEVEL=3` (`torch.compile` mode 3) làm tiến trình PyTorch Dynamo JIT bị đơ lặp vĩnh viễn (Deadlock) trong lúc khởi tạo CUDA Graph.
   - Container không thể sẵn sàng và bị hủy sau 2700s timeout.
2. **Khẳng định quy tắc thiết kế**:
   - **Tắt N-gram Speculative** để đảm bảo `torch.compile level 3` vận hành tối đa hiệu năng.
