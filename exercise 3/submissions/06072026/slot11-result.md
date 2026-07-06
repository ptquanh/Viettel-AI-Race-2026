# Kết quả Benchmark - Slot 11 06/07/2026 (max-num-seqs=128 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--max-num-seqs=128` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc nâng giới hạn request xử lý đồng thời lên 128 có giúp tối ưu hóa luồng xử lý và giảm CPU scheduling overhead khi weights đã lượng tử hóa FP8 hay không.



## Chỉ số đo được

TBD

---
