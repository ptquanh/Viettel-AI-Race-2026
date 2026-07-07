# Kết quả Benchmark - 08:30 07/07/2026 (Slot 4 - block-size=32 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--block-size=32` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc tăng kích thước KV Cache block từ 16 lên 32 có giúp tối ưu hóa truy cập bộ nhớ liên tiếp trên GPU, giảm số lượng block metadata cần quản lý hay không.

## Chỉ số đo được

- **Điểm số**: **17.23000** (Giảm **-1.76** so với Baseline 18.99)
- **Chỉ số chi tiết**:
  - **erc**: 0.708333
  - **ers**: 17.23
  - **passed_slo**: 85 / 120
  - **ttft_p50_ms**: 632 ms (Baseline: 569 ms)
  - **ttft_p95_ms**: 8430 ms (Baseline: 8520 ms)
  - **tbt_median_ms (TPOT)**: 51 ms (Baseline: 51 ms)
  - **accuracy_drop**: 3

### Nhận xét & Phân tích:

1. **Hiệu năng giảm sụt (Score dropped):** Điểm số giảm rõ rệt từ 18.99 xuống 17.23.
2. **TTFT P50 tăng lên:** TTFT P50 tăng từ 569ms lên 632ms (+63ms).
3. **TPOT giữ nguyên:** TPOT vẫn dậm chân tại chỗ ở mức 51ms.
4. **Nguyên nhân:** Kích thước block=32 làm tăng phân mảnh bộ nhớ trong (internal memory fragmentation) trong KV Cache hoặc làm chậm quá trình phân bổ/truy xuất block của vLLM scheduler, từ đó gián tiếp làm tăng TTFT P50.
5. **Kết luận:** **CẤM DÙNG `--block-size=32`**. Giữ nguyên mặc định (16).

---
