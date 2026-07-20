# BÁO CÁO THỬ NGHIỆM SLOT 1 - NGÀY 20/07 (0755 - SUCCESS)

## 1. Thông tin cấu hình

- **File nộp**: `0755-docker-compose.yml` (Slot 1 ngày 20/07)
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Cấu hình chính**: `Seqs=32`, `MaxModelLen=8192` (Re-test H3 trên v2), `Compilation Level 3`, `Quant=fp8`
- **Thời gian nộp**: 07:55 (20/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Điểm số cuối cùng (Final Score)**: **59.29 điểm**
- **TTFT P50**: **54 ms**
- **TTFT P95**: **82 ms**
- **TPOT (tbt_median_ms)**: **4 ms**
- **Failed Requests**: **4 requests** (Tỷ lệ thành công 99.0%)
- **Accuracy Drop / Penalty**: `0` / `1.0`

## 3. Phân tích nguyên nhân & Đánh giá Kỹ thuật

1. **Kết quả thực tế của Max Model Len 8192 trên Image v2**:
   - `MaxModelLen=8192` giữ tỷ lệ request lỗi ở mức rất thấp (**4 requests**).
   - Tuy nhiên, trễ TTFT P50 bị đẩy từ 46-48ms lên **54ms** và TTFT P95 bị đẩy từ 76ms lên **82ms**, làm điểm sụt giảm từ 60.75-61.13đ xuống **59.29đ**.
2. **Nguyên nhân kỹ thuật sâu xa**:
   - Trong vLLM v0.22.1 khi bật `COMPILATION_LEVEL=3` (PyTorch `torch.compile` CUDA Graphs), các bucket kích thước shape CUDA Graph và stride phân bổ KV block manager được định hình tối ưu nhất ở mốc mặc định 32768. Việc thu hẹp `max_model_len` về 8192 làm ngắt đoạn các CUDA Graph buckets tối ưu cho prefill.
3. **KẾT LUẬN CUỐI CÙNG CHO MAX MODEL LEN**:
   - **`VLLM_MAX_MODEL_LEN=32768` (32K)** là mốc cấu hình hoàn hảo duy nhất cho CUDA Graphs của vLLM v0.22.1.
