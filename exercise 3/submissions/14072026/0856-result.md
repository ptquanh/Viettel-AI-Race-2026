# Kết quả Benchmark - 14/07/2026 (STT 93 - Ghost v9.3: Seqs 32 + Warmup + Custom Kernel - 0856)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=32` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + Tắt Chunked Prefill + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Nộp lại cấu hình của đợt chạy 0747 ngày 12/07 nhưng bổ sung biến môi trường `VLLM_CUSTOM_KERNEL=1` để kích hoạt Monkey Patch và Triton Kernel dequantize KV Cache tối ưu, khắc phục lỗi TPOT 56ms và TTFT 3.7s.

## Chỉ số đo được

- **Điểm số**: **2.21**
- **Số request vượt qua SLO**: 4/120 (passed_slo)
- **TTFT P50**: **3730 ms**
- **TTFT P95**: **11610 ms**
- **TPOT Median**: **57 ms**
- **Accuracy drop**: 0 (GPQA)

## Phân tích kết quả

1. **Hiệu năng & So sánh**:
   - Kết quả gần như tương đương với Slot 1 (Score 2.21 vs 2.24, TPOT 57ms vs 56ms, TTFT P50 3.7s).
   - Điều này xác nhận rằng việc bật Warmup và Custom Kernel **không thể** giải quyết được vấn đề hiệu năng nếu **tắt Chunked Prefill** (`VLLM_ENABLE_CHUNKED_PREFILL=0`).
2. **Nguyên nhân cốt lõi**:
   - Dữ liệu trace chứa các request có user query rất lớn (10k-20k tokens).
   - Khi tắt Chunked Prefill, vLLM buộc phải thực hiện prefill toàn bộ câu hỏi lớn này trong một bước duy nhất, chặn đứng hoàn toàn các bước giải mã (decode) đang hoạt động.
   - Điều này làm TPOT tăng vọt lên ~57ms và gây tích lũy hàng đợi cực kỳ nặng, kéo TTFT P50 lên tới 3.7s.
3. **Kết luận**:
   - Bắt buộc phải **bật lại Chunked Prefill** (`VLLM_ENABLE_CHUNKED_PREFILL=1`) để cho phép xen kẽ prefill và decode, giữ TPOT ở mức tối ưu 30ms.
