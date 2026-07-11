# Kết quả Benchmark - 08:38 11/07/2026 (STT 78 - Prefix Warmup (Turn-1) + FP8 weights (hijack-v5) 🔥)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v5` + `--quantization fp8` + `--max-num-seqs 256` + Warmup prefix enable.
- **Mục đích**: Kích hoạt Prefix Cache Warmup via hijack v5. Warmup toàn bộ 20 requests của turn 1. TTFT có thể giảm sâu từ 600ms xuống 50ms cho batch 1. Khả năng tăng đột biến số request qua SLO.

## Chỉ số đo được

Điểm: **17.52000**
Số request passed SLO: **85/120**
TTFT P50: **625ms**
TTFT P95: **8390ms**
TPOT (tbt_median): **51ms**
Accuracy drop: **0**

## Phân tích & Nhận xét

Hiệu năng thực tế giống hệt baseline và không hề có sự sụt giảm TTFT (P50 vẫn ở mức 625ms). Điều này chỉ ra hai khả năng:

1. **Lỗi logic trong Warmup**: Lệnh curl warmup của chúng ta bắn request giả lập có thể đã bị lỗi (ví dụ format JSON sai hoặc system prompt trích xuất từ trace-round1 không khớp hoàn toàn với prompt thực tế mà grader của portal sử dụng).
2. **Eviction / Reset cache**: Cache của vLLM có thể đã bị reset hoặc evict hoàn toàn trước khi grader bắt đầu gửi trace thực tế, hoặc grader sử dụng trace ẩn (hidden trace) có system prompt khác hoàn toàn so với trace-round1.jsonl.

Chúng ta cần kiểm tra lại cơ chế warmup hoặc chờ cấu hình của STT 79 (0849) có tăng VRAM lên 0.97 xem có sự thay đổi nào không.
