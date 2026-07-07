# Kết quả Benchmark - 11:58 07/07/2026 (Slot 8 - compilation-config FULL_DECODE_ONLY Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--compilation-config='{"cudagraph_mode":"FULL_DECODE_ONLY","max_cudagraph_capture_size":256}'` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Ép vLLM thế hệ mới (v1 engine) chỉ sử dụng CUDA graph cho decode (bỏ qua prefill để tránh crash/timeout với context dài 20k-42k tokens) với kích thước capture tối đa là 256 (lớn hơn output size 200 tokens của benchmark), giúp giảm thiểu tối đa overhead kernel launch trên CPU khi sinh token.

## Chỉ số đo được

- **Điểm số**: **18.24000** (Giảm **-0.75** so với Baseline 18.99)
- **Chỉ số chi tiết**:
  - **erc**: 0.708333
  - **ers**: 18.24
  - **passed_slo**: 85 / 120 (Bằng Baseline)
  - **ttft_p50_ms**: 601 ms (Baseline: 569 ms)
  - **ttft_p95_ms**: 8426 ms (Baseline: 8520 ms)
  - **tbt_median_ms (TPOT)**: 51 ms (Baseline: 51 ms)
  - **accuracy_drop**: 0

### Nhận xét & Phân tích:

1. **TPOT không đổi:** TPOT vẫn giữ nguyên ở mức 51ms, chứng tỏ chế độ `FULL_DECODE_ONLY` CUDA graph decode không mang lại cải tiến hiệu năng giải mã thực tế nào so với chế độ capture mặc định của vLLM.
2. **TTFT P50 tăng nhẹ:** TTFT P50 tăng nhẹ khoảng 32ms khiến điểm số sụt giảm nhẹ về 18.24.
3. **Kết luận:** **CẤM DÙNG `--compilation-config`**.

---
