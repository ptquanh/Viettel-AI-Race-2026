# Kết quả Benchmark - 08:46 07/07/2026 (Slot 5 - performance-mode=interactivity Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--performance-mode=interactivity` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc chuyển sang chế độ tối ưu hóa độ trễ (latency-oriented) của vLLM v1 có giúp giảm TPOT xuống dưới 45ms (mốc tính điểm 50% ERS) hay không.

## Chỉ số đo được

- **Điểm số**: **16.33000** (Giảm **-2.66** so với Baseline 18.99)
- **Chỉ số chi tiết**:
  - **erc**: 0.716667
  - **ers**: 16.33
  - **passed_slo**: 86 / 120 (Tăng +1)
  - **ttft_p50_ms**: 694 ms (Baseline: 569 ms)
  - **ttft_p95_ms**: 8301 ms (Baseline: 8520 ms)
  - **tbt_median_ms (TPOT)**: 51 ms (Baseline: 51 ms)
  - **accuracy_drop**: 0

### Nhận xét & Phân tích:

1. **TPOT bất động:** TPOT vẫn đứng yên ở mức 51ms, chứng tỏ chế độ `interactivity` không làm giảm thời gian sinh token trên môi trường này.
2. **TTFT P50 tăng mạnh:** TTFT trung vị tăng đáng kể từ 569ms lên 694ms (+125ms), cho thấy khi có concurrency cao (120 requests dồn dập), cơ chế scheduling của `interactivity` gây hàng đợi prefill hoặc overhead điều phối CPU quá lớn (đặc biệt khi hệ thống chỉ có 3 nhân CPU).
3. **Kết luận:** **CẤM DÙNG `--performance-mode=interactivity`**. Bỏ qua toàn bộ các thử nghiệm liên quan đến `performance-mode` (kể cả throughput) do không giải quyết được TPOT và làm suy giảm nghiêm trọng TTFT.

---
