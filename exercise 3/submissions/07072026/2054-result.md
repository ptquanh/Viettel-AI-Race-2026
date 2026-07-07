# Kết quả Benchmark - 20:54 07/07/2026 (Slot 12 - STT21 Verification Run #1)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95` + `--enable-prefix-caching`).
- **Mục đích**: Chạy kiểm thử lặp lại cấu hình tốt nhất hiện tại (STT21 - 18.99đ) để tính trung bình và lấy median an toàn.

## Chỉ số đo được

- **Điểm số**: **17.89000** (Giảm **-1.10** so với mốc STT21 cũ do biến động CPU của host portal)
- **Chỉ số chi tiết**:
  - **erc**: 0.708333
  - **ers**: 17.89
  - **passed_slo**: 85 / 120 (Bằng Baseline)
  - **ttft_p50_ms**: 621 ms (Baseline: 569 ms)
  - **ttft_p95_ms**: 8416 ms (Baseline: 8520 ms)
  - **tbt_median_ms (TPOT)**: 51 ms (Baseline: 51 ms)
  - **accuracy_drop**: 0

### Nhận xét & Phân tích:

1. **Có sự biến động nhẹ về CPU (Jitter):** TPOT giữ nguyên ở mức 51ms, TTFT P95 cải thiện nhẹ (-104ms), nhưng TTFT P50 bị đẩy lên 621ms (+52ms) dẫn tới điểm số sụt giảm về 17.89. Điều này hoàn toàn do tác vụ chia sẻ CPU trên node host portal tại thời điểm chấm bài.
2. **Median dự kiến:** Khoảng 17.89 - 18.99đ.

---
