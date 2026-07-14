# Kết quả Benchmark - 14/07/2026 (STT 101 - Ghost v10.1: Seqs 24 + Chunk 8192 + Warmup + Custom Kernel - 2101)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=24` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + **Bật Chunked Prefill** với chunk size **8192** (`VLLM_ENABLE_CHUNKED_PREFILL=1` + `VLLM_MAX_NUM_BATCHED_TOKENS=8192`) + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Tăng chunk size lên 8192 (ở mức Seqs=24) để giảm số lượng chunk prefill, qua đó giảm CPU scheduling overhead trên hệ thống 3 cores và cải thiện hiệu năng chung.

## Chỉ số đo được

- **Điểm số**: **41.97** 🏆 **KỶ LỤC MỚI**
- **Số request vượt qua SLO**: 17/120 (passed_slo)
- **TTFT P50**: **3222 ms**
- **TTFT P95**: **6194 ms**
- **TPOT Median**: **22 ms**
- **Accuracy drop**: 4 (GPQA)

## Phân tích kết quả

1. **Thiết lập kỷ lục mới (41.97 điểm)**:
   - Điểm số tăng từ **39.83 lên 41.97**, vượt qua baseline 1058 (chunk 4096) để trở thành kỷ lục mới của bài thi.
   - TPOT Median duy trì xuất sắc ở mức **22 ms** (sát Floor 20ms).
   - Số lượng request passed SLO giảm xuống **17/120** (do TTFT P50 tăng nhẹ lên 3222 ms so với 3177 ms ở chunk 4096), nhưng tổng điểm trung bình (ERS) lại tăng lên. Điều này chứng tỏ phân phối TPOT của các request được cải thiện đáng kể (ít bị kéo dài do CPU scheduling jitter hơn).
2. **Xác nhận giả thuyết CPU Scheduling**:
   - Khi tăng chunk size lên 8192, số lượng chunk prefill cho query 20k tokens giảm từ 5 chunks xuống còn 3 chunks.
   - Ít chunk hơn đồng nghĩa với CPU overhead lập lịch nhẹ hơn, giúp luồng điều phối của vLLM hoạt động mượt mà hơn trên CPU 3 cores của portal.
   - Kết quả này chứng minh rằng việc giảm CPU scheduling overhead có tác động cực kỳ tích cực đến hiệu năng tổng thể của Serving Engine.
3. **Hướng đi kế tiếp**:
   - Nộp tiếp **slot 11: [slot11-docker-compose.yml](./slot11-docker-compose.yml) (Seqs=24, Chunk=16384)** để xem việc tăng tiếp chunk size lên 16k (chỉ còn 2 chunks cho prefill 20k) có giúp tối ưu thêm CPU overhead và nâng điểm số hay không.
