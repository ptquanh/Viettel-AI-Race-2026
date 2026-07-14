# Kết quả Benchmark - 14/07/2026 (STT 99 - Ghost v9.9: Seqs 32 + Warmup + Custom Kernel + Chunked Prefill - 1434)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=32` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + **Bật Chunked Prefill** (`VLLM_ENABLE_CHUNKED_PREFILL=1`) + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Kiểm chứng mức concurrency 32 nhằm tìm điểm giao thoa tối ưu, hy vọng TPOT giảm sâu về sát 22ms trong khi TTFT không bị vọt quá cao.

## Chỉ số đo được

- **Điểm số**: **29.06**
- **Số request vượt qua SLO**: 86/120 (passed_slo)
- **TTFT P50**: **1740 ms**
- **TTFT P95**: **5488 ms**
- **TPOT Median**: **27 ms**
- **Accuracy drop**: 0 (GPQA)

## Phân tích kết quả

1. **TPOT có sự cải thiện rõ rệt**:
   - TPOT Median giảm từ **31 ms xuống còn 27 ms** (cải thiện ~13%). Nhờ đó, điểm số tăng lên **29.06** (so với 23.29 ở Seqs 48).
   - TTFT P50 đạt **1740 ms** (tăng nhẹ so với 1358ms ở Seqs 48, và vượt trần 1500 ms nên nhận 0 điểm TTFT).
   - Số lượng request passed SLO là **86/120**.
2. **Giải thích toán học & vật lý về sự đánh đổi (Trade-off Curve)**:
   - **Với Seqs=24 (Điểm 39.83)**: Hàng đợi nghẽn nặng từ Turn 2 (do chỉ thừa 4 slot trống, 16 reqs phải xếp hàng chờ Turn 1 decode xong). TTFT P50 vọt lên **3177 ms** (0 điểm TTFT). Tuy nhiên, vì tối đa chỉ có 24 seqs đồng thời, TPOT đạt mức tối ưu **22 ms** ($s_{tpot} = 0.846 \rightarrow$ đóng góp gần 42 điểm).
   - **Với Seqs=32 (Điểm 29.06)**: Turn 2 thừa được 12 slot trống, giúp giảm hàng đợi xếp lớp. TTFT P50 giảm xuống **1740 ms**. Tuy nhiên, do số lượng seqs co-schedule tăng lên 32, TPOT tăng lên **27 ms** ($s_{tpot} = 0.518 \rightarrow$ chỉ đóng góp 25.9 điểm).
   - **Với Seqs=48 (Điểm 23.29)**: Turn 2 thừa 28 slot (chứa được toàn bộ 20 reqs mới). TTFT P50 giảm sâu về **1358 ms** (dưới trần 1.5s). Nhưng số seqs co-schedule lên tới 40+, đẩy TPOT lên **31 ms** ($s_{tpot} = 0.314 \rightarrow$ chỉ đóng góp 15.7 điểm).
3. **Kết luận Phase 1 (Seqs Sweep)**:
   - Do hàm phạt bình phương ($\gamma=2$) đánh phạt cực nặng khi latencies xa Floor, **TPOT đóng vai trò quyết định 90% điểm số**. Việc hy sinh TPOT để cứu TTFT ở Phase 1 là một giao dịch lỗ nặng (gặp điểm ngọt âm).
   - Cấu hình Seqs=24 vẫn là cấu hình cho điểm số cao nhất (39.83 điểm).
4. **Hướng đi kế tiếp (Chuyển sang Phase 2 - Chunk Size Sweep)**:
   - Chúng ta sẽ lấy **Seqs=24** làm baseline cố định cho Phase 2 (vì Seqs=24 giữ TPOT tốt nhất ở 22ms).
   - Mục tiêu của Phase 2: Quét kích thước chunk prefill (`max-num-batched-tokens`) ở các mốc 2048, 8192, 16384 để tìm cách kéo TTFT P50 của Seqs=24 xuống dưới 1500 ms mà không làm hỏng TPOT 22ms.
