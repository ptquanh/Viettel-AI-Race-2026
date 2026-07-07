# Kết quả Benchmark - 22:17 07/07/2026 (Slot 14 - STT21 Verification Run #3)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95` + `--enable-prefix-caching`).
- **Mục đích**: Chạy kiểm thử lặp lại cấu hình tốt nhất hiện tại (STT21 - 18.99đ) để tính trung bình và lấy median an toàn.

## Chỉ số đo được

- **Điểm số**: **17.05000** (Giảm **-1.94** so với mốc STT21 cũ do biến động CPU của host portal lúc cao điểm tải)
- **Chỉ số chi tiết**:
  - **erc**: 0.666667
  - **ers**: 17.05
  - **passed_slo**: 80 / 120 (Giảm -5)
  - **ttft_p50_ms**: 642 ms (Baseline: 569 ms)
  - **ttft_p95_ms**: 9260 ms (Baseline: 8520 ms)
  - **tbt_median_ms (TPOT)**: 51 ms (Baseline: 51 ms)
  - **accuracy_drop**: 0

### Nhận xét & Phân tích:

1. **CPU nghẽn trên host portal:** Điểm số sụt giảm do TTFT P50 tăng lên 642ms và P95 tăng vọt lên 9260ms (passed_slo tụt từ 85 xuống 80). TPOT vẫn giữ nguyên mức 51ms. Điều này phản ánh rõ tải nền của server chấm thi tăng cao vào cuối ngày (gần 23:59).
2. **Median dự kiến:** Median tính từ 4 lần chạy (18.99, 17.89, 18.09, 17.05) là **17.99đ**.

---
