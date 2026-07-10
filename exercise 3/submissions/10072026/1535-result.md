# Kết quả Benchmark - 15:35 10/07/2026 (STT 67 - Ghost Strategy v3: Slot 7 Aggressive TPOT Tweak)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v3` + biến môi trường: `VLLM_MAX_NUM_SEQS=32`, `VLLM_MAX_NUM_BATCHED_TOKENS=1024`, `VLLM_ENABLE_CHUNKED_PREFILL=1`.
- **Mục đích**: Ép TPOT xuống mức tối thiểu (~20ms) bằng cách giảm tối đa số sequence xử lý đồng thời (`--max-num-seqs 32`) nhằm giảm lượng KV Cache cần load mỗi step. Chunked prefill giảm về 1024 để đảm bảo prefill không làm nghẽn decode. Thử nghiệm này có tính chất aggressive, chấp nhận hi sinh TTFT để đo đạc giới hạn điểm của $s_{tpot}$.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
