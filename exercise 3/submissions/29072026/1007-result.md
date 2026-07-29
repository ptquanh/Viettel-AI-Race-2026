# Kết quả Benchmark - Sáng 29/07/2026 (Slot 1007 - Speculative N-gram GPU k=2)

- **Cấu hình**: `r4-ngram-k2` (Speculative Decoding N-gram GPU, `num_speculative_tokens=2`, `prompt_lookup_min=2`, `prompt_lookup_max=4`, Mamba Cache bfloat16)

## Kết quả chi tiết (Slot 1007)
- **Điểm chung cuộc (ERS / Final Score)**: **37.3900**
- **TTFT P50**: 54ms
- **TTFT P95**: 93ms
- **TBT Median (TPOT)**: 10ms (Tăng từ 4ms lên 10ms do N-gram GPU overhead)
- **Failed Count**: 6 / 420
- **Accuracy Drop**: 0%
- **Tokens/sec**: 0.0514

## Nhận xét
- Speculative Decoding dạng `ngram_gpu` làm tăng trễ TPOT lên 10ms (gấp 2.5 lần bình thường), khiến tổng điểm giảm thảm hại xuống 37.39đ. Loại bỏ phương án này.
