# BÁO CÁO THỬ NGHIỆM SLOT 2 - NGÀY 20/07 (0814 - SUCCESS)

## 1. Thông tin cấu hình

- **File nộp**: `0814-docker-compose.yml` (Slot 2 ngày 20/07)
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Cấu hình chính**: `Seqs=32`, `MaxModelLen=16384` (Re-test 16K thực sự trên v2), `Compilation Level 3`, `Quant=fp8`
- **Thời gian nộp**: 08:14 (20/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Điểm số cuối cùng (Final Score)**: **56.76 điểm**
- **TTFT P50**: **67 ms**
- **TTFT P95**: **95 ms**
- **TPOT (tbt_median_ms)**: **4 ms**
- **Failed Requests**: **4 requests** (Tỷ lệ thành công 99.0%)
- **Accuracy Drop / Penalty**: `0` / `1.0`

## 3. Phân tích nguyên nhân & Đánh giá Kỹ thuật

1. **So sánh 3 mốc Max Model Len trên nền Image v2**:
   - **8K (`8192`)**: TTFT P50 = **54 ms**, P95 = **82 ms** $\rightarrow$ **59.29 điểm**
   - **16K (`16384`)**: TTFT P50 = **67 ms**, P95 = **95 ms** $\rightarrow$ **56.76 điểm**
   - **32K (`32768`)**: TTFT P50 = **46 - 48 ms**, P95 = **72 - 76 ms** $\rightarrow$ **60.75 - 61.13 điểm** 🔥
2. **Nguyên nhân kỹ thuật sâu xa**:
   - Mốc 16K làm xáo trộn các bucket căn chỉnh CUDA Graph lớn nhất trong vLLM scheduler, đẩy TTFT P50 lên mốc xấu nhất (67ms).
3. **KẾT LUẬN CUỐI CÙNG HOÀN TOÀN KHÓA CHỌT**:
   - Mọi mốc thu hẹp `max-model-len` đều gây tác dụng ngược. **`VLLM_MAX_MODEL_LEN=32768` (32K)** là mốc cấu hình hoàn hảo duy nhất cho CUDA Graphs của vLLM v0.22.1 trên LFM2.5!
