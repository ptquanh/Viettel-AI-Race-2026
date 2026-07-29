# Kết quả Benchmark - Sáng 29/07/2026 (Slot 0852 - Image v23.0 Baseline)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v23.0`
- **Mục đích**: Chạy thử nghiệm Tokenizer Caching Phase 1.

## Kết quả thử nghiệm Slot 0852

- **Điểm số (ERS)**: **60.0000**
- **f_delta**: 1
- **penalty**: 1
- **final_score**: 60.0000
- **total_count**: 420
- **TTFT P50**: **53 ms**
- **TTFT P95**: **73 ms**
- **Failed Count**: 5
- **Warmup Count**: 0
- **Accuracy Drop**: 0
- **TBT Median (TPOT)**: **4 ms**
- **Tokens per sec**: 0.0516

> **Nhận xét**: Cache Miss 100% do User Prompt thay đổi liên tục ở từng request. TTFT P50 giữ nguyên 53ms. Đã khắc phục bằng Dynamic Prefix Boundary Caching cho các slot tiếp theo.
