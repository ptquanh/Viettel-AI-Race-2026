# Kết quả Benchmark - 14/07/2026 (STT 98 - Ghost v9.8: Seqs 48 + Warmup + Custom Kernel + Chunked Prefill - 1409)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=48` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + **Bật Chunked Prefill** (`VLLM_ENABLE_CHUNKED_PREFILL=1`) + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Giảm `max-num-seqs` xuống 48 để kiểm thử khoảng trung gian giữa 64 và 24, nhằm tìm điểm tối ưu giữa TTFT và TPOT.

## Chỉ số đo được

- **Điểm số**: **23.29**
- **Số request vượt qua SLO**: 90/120 (passed_slo)
- **TTFT P50**: **1358 ms**
- **TTFT P95**: **2400 ms**
- **TPOT Median**: **31 ms**
- **Accuracy drop**: 6 (GPQA)

## Phân tích kết quả

1. **TTFT và passed_slo được cải thiện**:
   - TTFT P50 đạt **1358 ms** (tốt hơn mức 1438ms của Seqs 128 và 1636ms của Seqs 64).
   - Số lượng request passed SLO đạt **90/120**. Do đó, điểm số tăng lên **23.29** (so với 20.57 và 20.64).
2. **TPOT vẫn kẹt ở 31 ms**:
   - Dù concurrency giảm xuống 48, TPOT vẫn ở mức **31 ms** (không đổi so với Seqs 128). Điều này cho thấy với 48 sequences chạy đồng thời, mức độ tranh chấp băng thông hoặc overhead chunked prefill co-scheduling vẫn tương đương với các mức concurrency cao hơn.
   - Khi TPOT = 31ms, điểm thành phần TPOT bị giới hạn.
3. **Cảnh báo về Accuracy Drop**:
   - `accuracy_drop` tăng lên **6** (sụt giảm 6 câu đúng trên bộ GPQA Diamond). Dù độ sụt giảm $\Delta = 0.06 \le 0.1$ vẫn nhận hệ số phạt $1.0$ (chưa bị trừ điểm), đây là dấu hiệu cảnh báo rằng cấu hình hoặc lượng tử hóa FP8 đang mấp mé giới hạn phạt của BTC.
4. **Hướng đi kế tiếp**:
   - Nộp tiếp **slot08 (Seqs 32)** để kiểm chứng mức concurrency tiệm cận 24.
   - Nếu Seqs 32 kéo được TPOT xuống khoảng < 25 ms mà TTFT không bị vọt lên quá cao (> 2s), đây có thể là cấu hình tối ưu nhất cho Phase 1.
