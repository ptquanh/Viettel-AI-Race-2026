# Kết quả Benchmark - 11:06 07/07/2026 (Slot 7 - compilation-config Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--compilation-config='{"cudagraph_mode":"FULL","max_cudagraph_capture_size":256}'` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Ép vLLM thế hệ mới (v1 engine) sử dụng chế độ FULL CUDA graph cho decode với kích thước capture tối đa là 256 (lớn hơn output size 200 tokens của benchmark), giúp giảm thiểu tối đa overhead kernel launch trên CPU.

## Chỉ số đo được

- **Điểm số**: **17.78000** (Giảm **-1.21** so với Baseline 18.99)
- **Chỉ số chi tiết**:
  - **erc**: 0.683333
  - **ers**: 17.78
  - **passed_slo**: 82 / 120 (Giảm -3)
  - **ttft_p50_ms**: 605 ms (Baseline: 569 ms)
  - **ttft_p95_ms**: 8929 ms (Baseline: 8520 ms)
  - **tbt_median_ms (TPOT)**: 51 ms (Baseline: 51 ms)
  - **accuracy_drop**: 0

### Nhận xét & Phân tích:

1. **TPOT không đổi:** TPOT giữ nguyên ở mức 51ms, chứng tỏ chế độ `FULL` CUDA graph decode không giúp cải thiện tốc độ sinh token so với chế độ capture mặc định của vLLM trên phần cứng này.
2. **TTFT suy giảm nhẹ:** Cả TTFT P50 (+36ms) và TTFT P95 (+409ms) đều tăng nhẹ, dẫn tới số lượng request pass SLO giảm từ 85 xuống 82. Điều này có thể do overhead compile graph ban đầu hoặc phân bổ tài nguyên bộ nhớ cho graph capture size lớn (256) làm tăng nhẹ chi phí điều phối.
3. **Kết luận:** **CẤM DÙNG `--compilation-config` với cudagraph_mode="FULL"**.

---
