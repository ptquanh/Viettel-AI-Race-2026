# Kết quả Benchmark - 14/07/2026 (STT 95 - Ghost v9.5: Seqs 256 + Warmup + Custom Kernel + Chunked Prefill - 1138)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=256` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + **Bật Chunked Prefill** (`VLLM_ENABLE_CHUNKED_PREFILL=1`) + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Tăng `max-num-seqs` lên 256 để kiểm chứng giả thuyết: việc tăng tối đa concurrency sẽ giúp giải phóng hàng đợi xếp lớp khi 20 requests đồng thời ập vào mỗi 5 giây, từ đó giảm thiểu TTFT P50 về mức có điểm (< 1500 ms).

## Chỉ số đo được

- **Điểm số**: **23.98**
- **Số request vượt qua SLO**: 91/120 (passed_slo)
- **TTFT P50**: **1764 ms**
- **TTFT P95**: **2585 ms**
- **TPOT Median**: **30 ms**
- **Accuracy drop**: 1 (GPQA)

## Phân tích kết quả

1. **Hiệu ứng giảm TTFT cực mạnh**:
   - TTFT P50 giảm sâu từ **3177 ms xuống còn 1764 ms** (giảm 1.4s so với Seqs=24).
   - TTFT P95 giảm rất mạnh từ **5681 ms xuống còn 2585 ms** (giảm hơn 3s!).
   - Số lượng request passed SLO tăng vọt từ **32 lên 91** (chiếm 75.8% tổng số request). Điều này chứng minh giả thuyết tăng `max-num-seqs` để giải phóng hàng đợi xếp lớp là hoàn toàn chính xác.
2. **Tại sao điểm số lại giảm xuống 23.98 (so với 39.83)?**:
   - Dù passed SLO tăng mạnh và TTFT giảm đáng kể, TTFT P50 (1764 ms) và P95 (2585 ms) **vẫn nằm trên trần 1500 ms (Ceiling)**. Tức là các requests có TTFT > 1500 ms vẫn bị nhận **0 điểm** cho thành phần TTFT!
   - Trong khi đó, việc tăng concurrency lên 256 làm tăng nhẹ TPOT từ **22 ms lên 30 ms**.
   - Do TPOT tăng (từ 22ms lên 30ms) làm giảm điểm TPOT, trong khi TTFT vẫn bị 0 điểm vì > 1500ms, dẫn đến tổng điểm giảm từ 39.83 xuống 23.98.
3. **Hướng đi kế tiếp**:
   - Chúng ta cần đẩy TTFT P50 xuống dưới mốc **1500 ms** để bắt đầu ghi nhận điểm số cho TTFT (nếu TTFT P50 đạt < 1500ms, điểm số sẽ bứt phá dữ dội nhờ 91+ request passed SLO).
   - Tiếp tục theo dõi kết quả của các slot Phase 1 tiếp theo (Seqs=128, 64, 48, 32) để tìm điểm cân bằng tốt nhất giữa TTFT và TPOT.
