# Kết quả Benchmark - 17:01 10/07/2026 (STT 71 - INT8 KV Cache per-token-head)

- **Cấu hình**: Image `vllm-v0.22.1-hijack-v4` + `--kv-cache-dtype int8_per_token_head` + `--quantization fp8`
- **Mục đích**: Fallback nếu INT4 gây accuracy drop > 10%. INT8 giảm 2x KV bandwidth, kỳ vọng TPOT ~30ms.

## Chỉ số đo được

- **Score (Điểm số)**: **0.13** (Passed SLO: 5/120)
- **erc**: 0.041667
- **ers**: 0.13
- **penalty**: 1
- **ttft_p50_ms**: 2598 ms
- **ttft_p95_ms**: 32842 ms
- **tbt_median_ms (TPOT)**: 220 ms
- **failed_count**: 0
- **accuracy_drop**: 4

### Nhận xét & Phân tích

- Kết quả benchmark cực tệ (0.13 điểm).
- TPOT tăng vọt từ 51ms lên **220ms** (gấp hơn 4 lần). TTFT P50 vọt lên **2.6 giây** và P95 vọt lên **32.8 giây** làm hầu hết các request bị timeout quá SLO.
- Mặc dù cờ `--kv-cache-dtype int8_per_token_head` không báo lỗi cú pháp lúc khởi động, nhưng nó gây ra dequantization/scheduling overhead cực lớn trên vLLM v0.22.1 với cấu hình CPU 3 cores.
- Kernel cho int8_per_token_head trên GPU H200 có vẻ chưa được tối ưu hóa tốt trong phiên bản này hoặc bị fallback chạy giải mã tính toán scale factor chậm chạp trên CPU.
- Accuracy drop chỉ là 4% (nằm trong ngưỡng cho phép < 10%), nhưng hiệu năng là không thể chấp nhận được. Loại bỏ hoàn toàn cờ này khỏi các thử nghiệm tiếp theo.
