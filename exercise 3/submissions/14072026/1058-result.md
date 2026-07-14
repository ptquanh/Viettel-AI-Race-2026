# Kết quả Benchmark - 14/07/2026 (STT 94 - Ghost v9.4: Seqs 24 + Warmup + Custom Kernel + Chunked Prefill - 1058)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=24` + `quantization=fp8` + `kv-cache-dtype=fp8` + Prefix Warmup (JIT compile + prefix cache) + **Bật Chunked Prefill** (`VLLM_ENABLE_CHUNKED_PREFILL=1`) + Bật `VLLM_CUSTOM_KERNEL=1`.
- **Mục đích**: Khắc phục lỗi của Slot 1 và Slot 2. Kích hoạt Chunked Prefill (chunk 4096) để cho phép xen kẽ prefill và decode, giúp giải quyết triệt để vấn đề hàng đợi bị nghẽn bởi các user query khổng lồ (10k-20k tokens) trong trace, đưa TPOT về lại 30ms và cải thiện mạnh TTFT.

## Chỉ số đo được

- **Điểm số**: **39.83**
- **Số request vượt qua SLO**: 32/120 (passed_slo)
- **TTFT P50**: **3177 ms**
- **TTFT P95**: **5681 ms**
- **TPOT Median**: **22 ms**
- **Accuracy drop**: 3 (GPQA)

## Phân tích kết quả

1. **Hiệu ứng bứt phá kỷ lục**:
   - Điểm số vọt từ **2.21 lên 39.83**, thiết lập kỷ lục mới cho bài thi!
   - TPOT Median giảm sâu xuống còn **22 ms** (so với 57 ms của slot trước), thậm chí còn tốt hơn cả baseline FP8 (30 ms). Điều này chứng minh sự kết hợp giữa Custom Kernel và Chunked Prefill hoạt động vô cùng hiệu quả.
   - Số lượng request passed SLO tăng vọt từ **4 lên 32**.
2. **Hạn chế còn tồn tại**:
   - TTFT P50 vẫn ở mức **3.17s** và TTFT P95 là **5.68s**. Điều này có nghĩa là mặc dù Chunked Prefill giải quyết cực tốt decode step, nhưng do hàng đợi ban đầu vẫn rất đông (20 requests/5s), các prefill của query độc nhất vẫn tạo ra hàng đợi xếp lớp.
   - `accuracy_drop` tăng lên **3** (có thể do lượng tử hóa FP8 gây suy giảm nhẹ độ chính xác trên một số câu hỏi khó của GPQA).
3. **Hướng đi kế tiếp**:
   - Cần tối ưu hơn nữa TTFT bằng cách điều chỉnh `max-num-seqs` hoặc tinh chỉnh kích thước chunk của prefill để xử lý prefill nhanh hơn, hoặc xem xét tác động của lượng tử hóa đến accuracy.
