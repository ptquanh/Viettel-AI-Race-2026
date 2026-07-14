# Kết quả Benchmark - 14/07/2026 (STT 96 - Ghost v9.6: Seqs 128 + Warmup + Custom Kernel + Chunked Prefill - 1348)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=128` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + **Bật Chunked Prefill** (`VLLM_ENABLE_CHUNKED_PREFILL=1`) + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Giảm `max-num-seqs` từ 256 xuống 128 để tìm điểm tối ưu giữa TTFT và TPOT.

## Chỉ số đo được

- **Điểm số**: **20.64**
- **Số request vượt qua SLO**: 95/120 (passed_slo)
- **TTFT P50**: **1438 ms**
- **TTFT P95**: **2745 ms**
- **TPOT Median**: **31 ms**
- **Accuracy drop**: 0 (GPQA)

## Phân tích kết quả

1. **TTFT lần đầu tiên chui dưới trần 1500ms**:
   - TTFT P50 đạt **1438 ms**, tức là đã vượt qua ngưỡng Ceiling 1500 ms. Lần đầu tiên chúng ta ghi nhận điểm số thực tế từ thành phần TTFT (dù rất nhỏ do hàm phạt bình phương).
   - Số lượng request passed SLO tăng lên kỷ lục: **95/120**.
2. **Lý do điểm số giảm (20.64)**:
   - Dưới tác dụng của hàm phạt bậc hai ($\gamma=2$), điểm số nhạy cảm cực hạn với khoảng cách tới Floor.
   - Với TPOT = 31 ms: $s_{tpot} = ((45-31)/25)^2 = 0.3136 \rightarrow$ đóng góp tối đa **15.68 điểm**.
   - Với TTFT P50 = 1438 ms: $s_{ttft} = ((1500-1438)/1400)^2 = 0.0019 \rightarrow$ đóng góp gần như **0 điểm**.
   - Tổng cộng lại, điểm số bị kéo tụt do TPOT tăng từ 22ms (Seqs 24) lên 31ms (Seqs 128). Sự sụt giảm 26 điểm TPOT không thể bù đắp bằng lượng điểm TTFT ít ỏi kiếm được khi mấp mé ngưỡng 1500ms.
3. **Bài học rút ra**:
   - Con đường duy nhất để đạt điểm cao (>50) là giữ TPOT ở mức cực thấp (< 25 ms) nhằm giữ vững ~35+ điểm TPOT, đồng thời ép TTFT P50 xuống vùng có điểm thực tế (< 1000 ms).
   - Tiếp tục quan sát các slot Seqs thấp hơn: `1353` (Seqs 64) và `1409` (Seqs 48).
