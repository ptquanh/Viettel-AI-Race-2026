# Kết quả Benchmark - 09:14 07/07/2026 (Slot 6 - max-num-batched-tokens=32768 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`) + `--max-num-batched-tokens=32768` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc tăng mạnh số lượng batched tokens cho chunked prefill lên 32k (gần với kích thước context thực tế 20k-42k) có giúp prefill hoàn thành trong 1-2 chunks, từ đó kéo giảm trễ TTFT P95 tail xuống dưới 3000ms hay không.

## Chỉ số đo được

- **Điểm số**: **16.73000** (Giảm **-2.26** so với Baseline 18.99)
- **Chỉ số chi tiết**:
  - **erc**: 0.1 (Giảm thảm hại từ 0.708)
  - **ers**: 16.73
  - **passed_slo**: 12 / 120 (Chỉ có 12 requests vượt qua ngưỡng TTFT SLO 1500ms!)
  - **ttft_p50_ms**: 4674 ms (Baseline: 569 ms - Tăng gần 10 lần!)
  - **ttft_p95_ms**: 9988 ms (Baseline: 8520 ms)
  - **tbt_median_ms (TPOT)**: 32 ms (Baseline: 51 ms - Cải thiện vượt bậc **-37%**)
  - **accuracy_drop**: 0

### Nhận xét & Phân tích:
1. **Mâu thuẫn cực đoan giữa TTFT và TPOT:**
   * **TPOT đạt mốc kỷ lục 32ms** (giảm sâu dưới ngưỡng 45ms). Điều này xác nhận rằng khi prefill được xử lý nguyên khối kích thước lớn, decode step được tối ưu và không bị ngắt quãng liên tục.
   * **TTFT P50 sụt giảm thảm hại lên tới 4.67 giây**! Khi cho phép prefill batch lên tới 32k tokens, một request prefill sẽ chiếm dụng GPU liên tục trong vài giây, chặn đứng toàn bộ các request khác đang chờ trong hàng đợi (Head-of-Line blocking).
2. **Passed SLO giảm còn 12/120:** Do TTFT bị đẩy lên quá cao, hầu như toàn bộ requests đều bị trễ quá 1500ms và không ăn được điểm TTFT SLO.
3. **Kết luận:** **CẤM DÙNG `--max-num-batched-tokens=32768`**. Giá trị quá lớn gây nghẽn hàng đợi nghiêm trọng. Tuy nhiên, việc TPOT giảm còn 32ms là một phát hiện cực kỳ quan trọng:
   * Bản thân GPU H200 hoàn toàn có khả năng decode ở tốc độ **32ms/token** (đạt tối đa điểm số TPOT ERS).
   * Điểm nghẽn duy nhất cản trở decode đạt tốc độ này là sự tranh chấp tài nguyên của prefill (prefill-decode contention).
   * Cần tìm một giá trị `--max-num-batched-tokens` trung gian (giữa 512 và 32768) hoặc một cơ chế khác để cân bằng giữa việc giải phóng prefill nhanh và không làm nghẽn decode.

---
