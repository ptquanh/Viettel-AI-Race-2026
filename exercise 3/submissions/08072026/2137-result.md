# Kết quả Benchmark - 21:37 08/07/2026 (STT 50 - MTP Speculative Decoding Test)

- **Cấu hình**: Baseline + `--speculative-config='{"method":"mtp","num_speculative_tokens":1}'` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem vLLM v0.22.1 của BTC có hỗ trợ MTP Speculative Decoding hay không.

## Chỉ số đo được

**Chấm điểm thất bại**

```
job exceeded max duration of 2700s with no terminal callback
```

---

*Kết luận: vLLM v0.22.1 khi kích hoạt MTP bị treo hoặc chạy cực kỳ chậm (deadlock/infinite loop ở decoding loop), dẫn tới vượt giới hạn 2700s (45 phút) của Grader. vLLM MTP chính thức bị loại khỏi danh sách tối ưu.*
