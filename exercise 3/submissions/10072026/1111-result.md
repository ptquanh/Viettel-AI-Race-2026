# Kết quả Benchmark - 09:00 10/07/2026 (STT 64 - CUDA Graph Capture Size 65k)

- **Cấu hình**: Image gốc `vllm/vllm-openai:v0.22.1` + STT 21 config + `--max-seq-len-to-capture=65536`.
- **Mục đích**: Tăng trần capture CUDA Graphs lên 65536 tokens. Ngăn chặn vLLM fallback về eager mode cho các chuỗi dài 20k-42k trong trace, qua đó triệt tiêu CPU overhead trên 3 cores và ép TPOT xuống dưới 45ms.

- **Điểm số**: `Chấm điểm thất bại (Fail)`
- **Lỗi startup**: `api_server.py: error: unrecognized arguments: --max-seq-len-to-capture=65536`

## Phân tích kết quả

Thử nghiệm thất bại do lỗi cú pháp khởi động (startup error).

1. **Nguyên nhân:** Cờ `--max-seq-len-to-capture` không được hỗ trợ trong phiên bản vLLM v0.22.1 chính thức.
2. **Đánh giá:** Việc cố gắng tối ưu hóa CUDA Graphs bằng cách cấu hình trực tiếp các cờ của phiên bản mới trên bản vLLM v0.22.1 cũ là không khả thi.

**Kết luận:** Tuyệt đối không dùng cờ `--max-seq-len-to-capture` trên image gốc vLLM v0.22.1. Việc chuyển dịch sang v0.5.2 (Ghost Strategy v2) là cần thiết để có thể sử dụng các tính năng và cờ tối ưu hóa mới hơn.
