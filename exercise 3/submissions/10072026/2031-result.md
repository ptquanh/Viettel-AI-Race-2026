# Kết quả Benchmark - 17:02 10/07/2026 (STT 72 - FP8 per-token-head KV Cache)

- **Cấu hình**: Image `vllm-v0.22.1-hijack-v4` + `--kv-cache-dtype fp8_per_token_head` + `--quantization fp8`
- **Mục đích**: So sánh fp8 per-token-head (mới) vs fp8 per-tensor (cũ - STT 17/61 bị tăng TPOT).

## Chỉ số đo được

- **Score (Điểm số)**: **0.08** (Passed SLO: 4/120)
- **erc**: 0.033333
- **ers**: 0.08
- **penalty**: 1
- **ttft_p50_ms**: 2674 ms
- **ttft_p95_ms**: 33677 ms
- **tbt_median_ms (TPOT)**: 227 ms
- **failed_count**: 0
- **accuracy_drop**: 0

### Nhận xét & Phân tích

- Kết quả benchmark thất bại hoàn toàn (0.08 điểm).
- Tương tự như cờ INT8, cờ `--kv-cache-dtype fp8_per_token_head` làm TPOT vọt lên tới **227ms** (tệ hơn cả baseline 51ms và thậm chí tệ hơn cả fp8 per-tensor cũ ở STT 61 là 63ms).
- Khẳng định chắc chắn: Toàn bộ cơ chế lượng tử hóa KV cache động theo dạng _per-token-head_ (cả INT8 và FP8) trên bản vLLM v0.22.1 này đều bị lỗi tối ưu hóa kernel nghiêm trọng, tạo ra một bottleneck xử lý khổng lồ, khiến các requests bị hàng đợi dồn ứ (TTFT P95 lên đến 33.6 giây).
- Điểm tích cực duy nhất là accuracy không bị sụt giảm (accuracy drop = 0%). Nhưng hiệu năng quá tệ làm cờ này không thể sử dụng.
