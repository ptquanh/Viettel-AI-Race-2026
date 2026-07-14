# Kết quả Benchmark - 14/07/2026 (STT 102 - Ghost v10.2: Seqs 24 + Chunk 16384 + Warmup + Custom Kernel - 2121)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=24` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + **Bật Chunked Prefill** với chunk size **16384** (`VLLM_ENABLE_CHUNKED_PREFILL=1` + `VLLM_MAX_NUM_BATCHED_TOKENS=16384`) + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Tăng tối đa chunk size lên 16384 (ở mức Seqs=24) để giảm số lượng chunk prefill xuống mức tối thiểu (chỉ còn ~1-2 chunks cho query 20k tokens), giải phóng triệt để CPU overhead.

## Chỉ số đo được

- **Điểm số**: **42.27** 🏆 **KỶ LỤC MỚI**
- **Số request vượt qua SLO**: 20/120 (passed_slo)
- **TTFT P50**: **4268 ms**
- **TTFT P95**: **6495 ms**
- **TPOT Median**: **21 ms**
- **Accuracy drop**: 0 (GPQA)

## Phân tích kết quả

1. **Tiếp tục phá kỷ lục (42.27 điểm)**:
   - Điểm số tăng nhẹ từ **41.97 lên 42.27**, thiết lập kỷ lục mới.
   - TPOT Median giảm thêm 1ms xuống còn **21 ms** (cực kỳ tiệm cận Floor 20ms).
   - Số lượng request passed SLO tăng nhẹ lên **20/120** (so với 17/120 ở chunk 8192).
   - TTFT P50 tăng lên **4268 ms** (so với 3222 ms ở chunk 8192). Điều này xảy ra do kích thước chunk prefill lớn khiến mỗi bước tính toán prefill trên GPU chiếm dụng thời gian lâu hơn, kéo dài TTFT của các request khác đang chờ decode. Tuy nhiên, hiệu quả giảm tải CPU đã bù đắp vượt trội.
2. **Tổng kết Phase 2 (Chunk Size Sweep)**:
   - Việc tăng chunk size lên 8192 và 16384 mang lại hiệu quả vượt bậc đối với điểm số trung bình nhờ giải phóng CPU overhead của container (chỉ có 3 cores).
   - Chunk size **16384** đem lại TPOT tốt nhất (21ms) và điểm số cao nhất (42.27). Do đó, cấu hình này sẽ là baseline mới cho Phase 3.
3. **Hướng đi kế tiếp (Chuyển sang Phase 3 - Fine-tuning)**:
   - Chúng ta sẽ dùng baseline: **Seqs=24, Chunk=16384** cho Phase 3.
   - **Slot 12**: [slot12-docker-compose.yml](./slot12-docker-compose.yml) (giảm `OMP_NUM_THREADS` từ 3 xuống 2 để giảm context switching overhead).
   - Để chuẩn bị, ta cần cập nhật `slot12` đến `slot15` sử dụng `VLLM_MAX_NUM_BATCHED_TOKENS=16384`.
