# Kết quả Benchmark - 15:53 10/07/2026 (STT 68 - Ghost Strategy v3: Slot 8 Ablation Study - No Chunked Prefill)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v3` + biến môi trường: `VLLM_MAX_NUM_SEQS=48`, `VLLM_ENABLE_CHUNKED_PREFILL=0`.
- **Mục đích**: Nghiên cứu độc lập (Ablation study) tác động của việc giảm `max-num-seqs` xuống 48 mà không bật chunked prefill. Việc này giúp xác nhận xem chunked prefill có thực sự cần thiết khi batch size đã giảm hay không, đồng thời loại trừ nhiễu của chunked prefill đối với chỉ số TPOT.

## Chỉ số đo được

- **Score (Điểm số)**: **15.19** (Passed SLO: 84/120)
- **erc**: 0.7
- **ers**: 15.19
- **penalty**: 1
- **ttft_p50_ms**: 709 ms
- **ttft_p95_ms**: 10032 ms
- **tbt_median_ms (TPOT)**: 59 ms
- **failed_count**: 0

### Nhận xét & Phân tích

- Khi tắt Chunked Prefill (so sánh STT 68 vs STT 66):
  - TPOT giữ nguyên ở mức **59ms** (không thay đổi).
  - TTFT P50 tăng nhẹ từ **637ms** lên **709ms** do không được chia nhỏ prefill xử lý xen kẽ.
- Điều này chứng minh rằng:
  1. Bản thân việc giảm `max-num-seqs` xuống 48 (cho dù có chunked prefill hay không) đều chịu chung số phận TPOT = 59ms (không đạt target ≤ 45ms).
  2. Băng thông đọc KV cache hoặc overhead tính toán của 6 layers full-attention ở GQA decode vẫn quá lớn so với năng lực của 3 CPU cores + GPU H200 (khi bị giới hạn 1/7 MIG).
  3. Cờ `--enable-chunked-prefill` thực sự giúp ích nhẹ cho TTFT (giảm ~70ms) nhưng không phải là yếu tố thay đổi cuộc chơi cho TPOT.
