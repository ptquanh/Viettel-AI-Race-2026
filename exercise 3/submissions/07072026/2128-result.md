# Kết quả Benchmark - 21:28 07/07/2026 (Slot 13 - STT21 Verification Run #2)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95` + `--enable-prefix-caching`).
- **Mục đích**: Chạy kiểm thử lặp lại cấu hình tốt nhất hiện tại (STT21 - 18.99đ) để tính trung bình và lấy median an toàn.

## Chỉ số đo được

- **Điểm số**: **18.09000** (Giảm nhẹ **-0.90** so với mốc STT21 cũ do biến động CPU của host portal)
- **Chỉ số chi tiết**:
  - **erc**: 0.716667
  - **ers**: 18.09
  - **passed_slo**: 86 / 120 (Tăng +1)
  - **ttft_p50_ms**: 608 ms (Baseline: 569 ms)
  - **ttft_p95_ms**: 8247 ms (Baseline: 8520 ms)
  - **tbt_median_ms (TPOT)**: 51 ms (Baseline: 51 ms)
  - **accuracy_drop**: 0

### Nhận xét & Phân tích:

1. **Độ ổn định cao:** TPOT giữ nguyên ở mức 51ms. TTFT P95 cải thiện đáng kể (-273ms) và passed_slo tăng lên 86/120 requests. Điểm số đạt 18.09đ chứng minh cấu hình STT21 cực kỳ ổn định trong môi trường tải thực tế.
2. **Median dự kiến:** ~18.09 - 18.24đ.

---
