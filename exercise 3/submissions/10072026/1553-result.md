# Kết quả Benchmark - 15:53 10/07/2026 (STT 68 - Ghost Strategy v3: Slot 8 Ablation Study - No Chunked Prefill)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v3` + biến môi trường: `VLLM_MAX_NUM_SEQS=48`, `VLLM_ENABLE_CHUNKED_PREFILL=0`.
- **Mục đích**: Nghiên cứu độc lập (Ablation study) tác động của việc giảm `max-num-seqs` xuống 48 mà không bật chunked prefill. Việc này giúp xác nhận xem chunked prefill có thực sự cần thiết khi batch size đã giảm hay không, đồng thời loại trừ nhiễu của chunked prefill đối với chỉ số TPOT.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
