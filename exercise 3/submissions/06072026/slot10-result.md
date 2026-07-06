# Kết quả Benchmark - Slot 10 06/07/2026 (max-num-seqs=256 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--max-num-seqs=256` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc nâng giới hạn request xử lý đồng thời lên 256 có giúp tận dụng năng lực tính toán tốt hơn khi weights đã được lượng tử hóa FP8 hay không.



## Chỉ số đo được

TBD

---
