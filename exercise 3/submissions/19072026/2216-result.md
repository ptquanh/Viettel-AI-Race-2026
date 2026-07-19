# BÁO CÁO THỬ NGHIỆM SLOT 15 (2216 - SUCCESS)

## 1. Thông tin cấu hình

- **File nộp**: `2216-docker-compose.yml` (Slot 15)
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Cấu hình chính**: `Seqs=32`, `Len=32768`, `Compilation Level 3`, `Quant=fp8`, `VLLM_KV_CACHE_DTYPE=fp8_e5m2`
- **Thời gian nộp**: 22:16 (19/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Điểm số cuối cùng (Final Score)**: **56.52 điểm**
- **TTFT P50**: **63 ms**
- **TTFT P95**: **95 ms**
- **TPOT (tbt_median_ms)**: **4 ms**
- **Failed Requests**: **5 requests**
- **Accuracy Drop / Penalty**: `0` / `1.0`

## 3. Phân tích nguyên nhân & Đánh giá Kỹ thuật

1. **Tác động của KV Cache FP8 (`fp8_e5m2`) trên LFM2.5-1.2B**:
   - Đối với mô hình kích thước nhỏ như `LFM2.5-1.2B`, băng thông VRAM không phải là cổ chai chính khi lưu trữ KV Cache (do FP8 Native model weights chỉ chiếm ~1.2GB VRAM).
   - Việc ép KV Cache về FP8 E5M2 bắt buộc vLLM phải thực hiện casting/dequantization động từ FP8 về FP16 ở mỗi bước Attention layer. Overhead tính toán của phép dequantization này làm tăng trễ TTFT P50 từ 48ms lên 63ms và TTFT P95 từ 76ms lên 95ms.
2. **KẾT LUẬN CUỐI CÙNG CHO KV CACHE**:
   - **Duy trì KV Cache mặc định (`VLLM_KV_CACHE_DTYPE=auto` / FP16)** là tối ưu nhất cho LFM2.5-1.2B.
   - **FP8 Native Weights (`VLLM_QUANTIZATION=fp8`) + Default KV Cache + `COMPILATION_LEVEL=3` + Non-chunked Prefill** chính là CÔNG THỨC VÀNG ĐỈNH CAO NHẤT (đạt 60.75đ - 61.13đ)!
