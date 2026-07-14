# Kết quả Benchmark - 14/07/2026 (STT 97 - Ghost v9.7: Seqs 64 + Warmup + Custom Kernel + Chunked Prefill - 1353)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=64` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + **Bật Chunked Prefill** (`VLLM_ENABLE_CHUNKED_PREFILL=1`) + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Giảm `max-num-seqs` xuống 64 để tìm điểm cân bằng tốt nhất giữa TTFT và TPOT.

## Chỉ số đo được

- **Điểm số**: **20.57**
- **Số request vượt qua SLO**: 74/120 (passed_slo)
- **TTFT P50**: **1636 ms**
- **TTFT P95**: **2884 ms**
- **TPOT Median**: **30 ms**
- **Accuracy drop**: 0 (GPQA)

## Phân tích kết quả

1. **Hiệu ứng khi Seqs giảm xuống 64**:
   - TTFT P50 tăng lên **1636 ms** (vượt trần 1500 ms) so với 1438 ms ở Seqs 128.
   - Số request passed SLO giảm xuống **74/120** (do hàng đợi bị nghẽn nhẹ vì giới hạn Seqs=64 không đủ chứa toàn bộ requests khi burst 20 reqs mới ập vào và các reqs cũ chưa decode xong).
   - TPOT Median đạt **30 ms** (chỉ giảm 1ms so với Seqs 128, vẫn rất cao so với 22ms ở Seqs 24).
2. **Giải thích cơ chế ngầm (Nút thắt cổ chai Co-scheduling)**:
   - Khi `max-num-seqs` lớn (≥ 64), toàn bộ hoặc phần lớn burst 20 requests mới sẽ được admit ngay lập tức vào engine.
   - Điều này bắt buộc vLLM phải lập lịch đồng thời (co-schedule) cho rất nhiều prefill chunks của các request mới cùng với decode steps của các request cũ.
   - Sự tranh chấp băng thông bộ nhớ (memory bandwidth) cực mạnh khi chạy đồng thời nhiều prefill chunks + decode steps khiến TPOT của decode steps bị kéo dài lên **30-31 ms**.
   - Khi `max-num-seqs` nhỏ (ví dụ 24), chỉ có tối đa 4 requests mới được admit, phần còn lại bị xếp hàng đợi (queue). Điều này vô hình trung làm giảm số lượng prefill chunks chạy song song với decode, giúp decode chạy nhanh hơn và TPOT đạt mức tối ưu **22 ms**.
3. **Hướng đi kế tiếp**:
   - Chờ kết quả của **1409 (Seqs 48)** để xem xu hướng TPOT và TTFT ở khoảng trung gian này.
   - Nếu Seqs 48 vẫn không cải thiện được TPOT về mức < 25ms, chúng ta sẽ hướng tới tinh chỉnh kích thước chunk (Phase 2) hoặc các tham số phụ (Phase 3).
