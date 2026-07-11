# Kết quả Benchmark - 09:50 11/07/2026 (STT 80 - FlashInfer + FP8 weights (no warmup) 🔥)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-flashinfer` + `--quantization fp8` + `--max-num-seqs 256` (default) + `VLLM_ATTENTION_BACKEND=FLASHINFER` + `OMP_NUM_THREADS=3`
- **Mục đích**: Kết hợp FlashInfer attention backend với weights FP8. Loại bỏ hoàn toàn hijack warmup để tránh overhead CPU lúc startup. Cấu hình OMP_NUM_THREADS=3 để khớp với số core CPU thực tế của Grader host.

## Chỉ số đo được

Điểm: **16.91000**
Số request passed SLO: **85/120**
TTFT P50: **625ms**
TTFT P95: **8453ms**
TPOT (tbt_median): **51ms**
Accuracy drop: **1**

## Phân tích & Nhận xét

Kết quả đạt **16.91** điểm (thấp hơn so với baseline 18.99 điểm của STT 21 dùng FlashAttention mặc định).

### Phân tích nguyên nhân:

1. **FlashInfer JIT/Triton Overhead**: Đối với mô hình có số heads nhỏ như Qwen3.5-2B (8 attention heads, 2 KV heads), các kernel của FlashAttention được tối ưu hoá tốt hơn nhiều so với FlashInfer ở mức concurrency vừa phải. FlashInfer gây ra overhead lập lịch trên CPU và tài nguyên VRAM tĩnh cao hơn, dẫn tới TTFT P50 tăng nhẹ (625ms so với 615ms) và không có lợi thế về TPOT (vẫn giữ nguyên 51ms).
2. **Accuracy Drop**: Việc lượng tử hoá FP8 weights của mô hình Qwen3.5-2B gây sụt giảm nhẹ độ chính xác (accuracy drop = 1), tuy nhiên hệ số phạt f(1) vẫn là 1.0 nên không ảnh hưởng điểm số trực tiếp từ hình phạt, nhưng cho thấy việc lượng tử hoá weights FP8 có gây biến thiên nhẹ.

_Kết luận_: FlashInfer không mang lại lợi ích cho mô hình kích thước nhỏ Qwen3.5-2B trong cuộc thi này. Chúng ta sẽ quay lại sử dụng **FlashAttention (mặc định)** làm backend attention chính.
