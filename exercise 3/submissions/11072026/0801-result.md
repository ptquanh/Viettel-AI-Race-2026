# Kết quả Benchmark - 08:01 11/07/2026 (STT 77 - FlashInfer Backend + BF16 gốc, seqs 128 🔥)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-flashinfer` + `--max-num-seqs 128` + BF16 gốc
- **Mục đích**: Tinh chỉnh hàng đợi tối đa `--max-num-seqs=128` kết hợp FlashInfer attention backend nhằm tìm kiếm điểm cân bằng tối ưu giữa TTFT và TPOT.

## Chỉ số đo được

Điểm: **17.72000**
Số request passed SLO: **86/120**
TTFT P50: **627ms**
TTFT P95: **8311ms**
TPOT (tbt_median): **51ms**
Accuracy drop: **0**

## Phân tích & Nhận xét

Việc giảm `max-num-seqs` từ 256 xuống 128 không làm thay đổi đáng kể chỉ số hiệu năng (TTFT P50 chỉ tăng nhẹ từ 622ms lên 627ms và TPOT giữ nguyên ở 51ms). Điều này xác nhận rằng hàng đợi không bị nghẽn ở mức concurrency này và bottleneck chính vẫn nằm ở memory bandwidth.
