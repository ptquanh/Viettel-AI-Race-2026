# Kết quả Benchmark - 14/07/2026 (STT 100 - Ghost v10.0: Seqs 24 + Chunk 2048 + Warmup + Custom Kernel - 2051)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=24` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + **Bật Chunked Prefill** với chunk size **2048** (`VLLM_ENABLE_CHUNKED_PREFILL=1` + `VLLM_MAX_NUM_BATCHED_TOKENS=2048`) + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Giảm chunk size xuống 2048 (ở mức Seqs=24) để xem việc chia nhỏ prefill hơn nữa có giúp giải phóng bước decode và giữ TPOT tối ưu hay không.

## Chỉ số đo được

- **Điểm số**: **3.33**
- **Số request vượt qua SLO**: 4/120 (passed_slo)
- **TTFT P50**: **6721 ms**
- **TTFT P95**: **12416 ms**
- **TPOT Median**: **44 ms**
- **Accuracy drop**: 0 (GPQA)

## Phân tích kết quả

1. **Hiệu năng sụp đổ hoàn toàn (Điểm 3.33)**:
   - TPOT tăng vọt từ **22 ms lên 44 ms** (tăng gấp đôi!).
   - TTFT P50 tăng cực mạnh từ **3177 ms lên 6721 ms** (tăng hơn gấp đôi!).
   - Số lượng request passed SLO giảm thê thảm từ **32 xuống còn 4/120**.
2. **Nguyên nhân sâu xa (Cổ chai CPU Scheduling Overhead)**:
   - Trong môi trường Grader của BTC chỉ phân bổ **3 CPU Cores** cho container.
   - Khi chia nhỏ kích thước prefill chunk xuống 2048, số lượng chunk cần xử lý của các user query lớn (10k-20k tokens) bị tăng lên gấp đôi (từ 5 chunks lên 10 chunks).
   - vLLM phải thực hiện lập lịch (scheduling) và phối hợp (co-schedule) các chunks này liên tục trên CPU. Context switching và coordination overhead trên 3 cores CPU bị quá tải nghiêm trọng, dẫn đến nghẽn cổ chai CPU.
   - Kết quả là GPU bị "đói" lệnh, khiến cả TTFT (do prefill bị kéo dài) lẫn TPOT (do bước decode bị trì hoãn) đều sụt giảm nghiêm trọng.
3. **Bài học rút ra**:
   - **Không được chia nhỏ chunk size xuống dưới 4096** trên môi trường 3 cores CPU của BTC. Việc chia nhỏ chunk size mang lại hiệu ứng ngược do overhead lập lịch CPU vượt quá năng lực xử lý.
   - Giả thuyết tăng kích thước chunk size lên **8192 (slot 10)** hoặc **16384 (slot 11)** để giảm số lượng chunk và giảm tải cho CPU có khả năng cao sẽ đem lại hiệu năng tốt hơn.
