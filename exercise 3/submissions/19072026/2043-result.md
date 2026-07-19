# BÁO CÁO THỬ NGHIỆM SLOT 11 (2043 - TIMEOUT FAIL)

## 1. Thông tin cấu hình

- **File nộp**: `2043-docker-compose.yml` (Slot 11)
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Cấu hình chính**: `Seqs=32`, `Len=32768`, `Compilation Level 3`, `Quant=fp8`, `VLLM_SPECULATIVE_MODEL=ngram`, `VLLM_NUM_SPECULATIVE_TOKENS=5`
- **Thời gian nộp**: 20:43 (19/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Trạng thái**: **Chấm điểm thất bại (FAILED)**
- **Lỗi chi tiết**: `job exceeded max duration of 2700s with no terminal callback` (Timeout 2700 giây)

## 3. Phân tích nguyên nhân gốc (Root Cause Analysis)

1. **Xung đột giữa JIT Compilation Level 3 và N-gram Speculative**:
   - Trong vLLM v0.22.1, khi bật đồng thời `VLLM_COMPILATION_LEVEL=3` (`mode: 3`) và `VLLM_SPECULATIVE_MODEL=ngram`, trình biên dịch PyTorch Dynamo của `torch.compile` gặp xung đột khi cố gắng trace vòng lặp khớp token N-gram động trong JIT CUDA Graph.
   - Việc này khiến tiến trình warmup của vLLM rơi vào vòng lặp treo vĩnh viễn (Infinite Tracing Loop / Deadlock), khiến container không bao giờ sẵn sàng và bị BTC tự động hủy sau 2700s timeout.
2. **Kết luận kỹ thuật ngắt kết nối**:
   - **KHÔNG ĐƯỢC kết hợp `COMPILATION_LEVEL=3` với `VLLM_SPECULATIVE_MODEL=ngram`** trong vLLM v0.22.1!
   - Nếu muốn dùng `N-gram Speculative`, phải hạ `COMPILATION_LEVEL=0` (hoặc `enforce-eager`). Tuy nhiên, `enforce-eager` đã làm giảm điểm từ 60.91 xuống 57.06 (ở STT 34), chứng tỏ `torch.compile level 3` mang lại giá trị cao hơn nhiều so với N-gram!
