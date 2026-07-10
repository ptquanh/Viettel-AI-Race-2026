# Kết quả Benchmark - 08:30 10/07/2026 (STT 62 - MTP Speculative Decoding Retry)

- **Cấu hình**: Image gốc `vllm/vllm-openai:v0.22.1` + STT 21 config + `--speculative-config={"method":"mtp","num_speculative_tokens":1}`.
- **Mục đích**: Retry MTP speculative decoding (STT 50 bị Timeout 2700s). Qwen3.5 có native MTP head (`mtp_num_hidden_layers: 1`). Nếu thành công, effective TPOT giảm từ 51ms xuống ~32ms (1.6x tokens/step).

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
