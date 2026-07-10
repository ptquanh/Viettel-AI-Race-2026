# Kết quả Benchmark - 09:00 10/07/2026 (STT 64 - CUDA Graph Capture Size 65k)

- **Cấu hình**: Image gốc `vllm/vllm-openai:v0.22.1` + STT 21 config + `--max-seq-len-to-capture=65536`.
- **Mục đích**: Tăng trần capture CUDA Graphs lên 65536 tokens. Ngăn chặn vLLM fallback về eager mode cho các chuỗi dài 20k-42k trong trace, qua đó triệt tiêu CPU overhead trên 3 cores và ép TPOT xuống dưới 45ms.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
