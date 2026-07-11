# Kết quả Benchmark - 07:50 11/07/2026 (STT 76 - FlashInfer Backend + BF16 gốc, seqs 256 🔥)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-flashinfer` + `--max-num-seqs 256` + BF16 gốc
- **Mục đích**: Chạy thử nghiệm FlashInfer Attention backend trên model gốc BF16, so sánh hiệu năng trực tiếp với baseline STT 21 (FlashAttention, đạt 18.99 điểm).

## Chỉ số đo được

Điểm: **17.80000**
Số request passed SLO: **86/120**
TTFT P50: **622ms**
TTFT P95: **8276ms**
TPOT (tbt_median): **51ms**
Accuracy drop: **0**

## Phân tích & Nhận xét

FlashInfer trên BF16 gốc cho kết quả tương đối giống baseline STT 21 (18.99 điểm). Tuy nhiên, do mô hình chạy ở BF16 thay vì FP8, điểm số sụt giảm nhẹ (~1.2 điểm) so với baseline do prefill/decode ở BF16 chậm hơn đôi chút so với FP8. Chỉ số TPOT vẫn bị giới hạn ở 51ms.
