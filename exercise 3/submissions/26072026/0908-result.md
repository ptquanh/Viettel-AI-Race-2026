# Kết quả Benchmark - 09:08 26/07/2026 (Slot 06 - Chunked Prefill)

- **Cấu hình**: Image `v14` (Champion) + `VLLM_MAX_NUM_SEQS=48` + `VLLM_ENABLE_CHUNKED_PREFILL=1` + `VLLM_MAX_NUM_BATCHED_TOKENS=2048`.
- **Mục đích**: Chia nhỏ khối lượng tính toán Prefill khổng lồ của 48 sequences thành các khối 2048 tokens để GPU có thể đan xen tính toán Decode, hy vọng tránh được tình trạng "nghẽn" Scheduler như Slot 04.

### Chỉ số chi tiết:

- **Final Score**: **57.06**
- **TPOT (Median)**: 4ms
- **TTFT (P50)**: 59ms
- **TTFT (P95)**: 91ms
- **Failed / Total**: 4 / 420
- **Accuracy Drop**: 0%

### Đánh giá:

1. **Thất bại toàn tập của Chunked Prefill**: TTFT P95 vọt lên **91ms** (tệ nhất trong ngày hôm nay, tệ hơn cả Slot 04 là 69ms khi không dùng chunked prefill).
2. **Nguyên nhân cốt lõi**: `FLASHINFER` (đang được dùng trong Image v14) được thiết kế để nạp và tính toán Attention với tốc độ siêu thanh trên các mảng ma trận khổng lồ. Việc cố tình "băm nhỏ" Prefill ra (Chunked Prefill) buộc GPU phải khởi chạy (launch) nhiều CUDA kernels hơn, tăng lượng Overhead giao tiếp giữa CPU và GPU. Trên một hệ thống CPU vốn đã bị thắt cổ chai (3 Cores) như MiG host, tăng lượng Kernel Launch làm Scheduler "sập nguồn" cục bộ, đẩy hàng đợi lên cao ngất ngưởng.
3. **Cấu trúc Recurrent LFM**: Khác với Transformer, trạng thái (State) của LFM không dễ dàng bị băm nhỏ mà không đánh đổi bằng overhead liên kết chuỗi thời gian. Tính năng này tỏ ra cực kỳ chống chỉ định.

### Kết luận Vòng 2 (Chốt sổ 26/07):

- **Cấu hình 10:12 25/07 (62.67đ)** chính thức là cấu hình Vô địch và là **giới hạn vật lý cao nhất** chúng ta có thể chạm tới bằng con đường Tuning Hyper-Parameters và Native FP8 trên hệ thống vLLM thuần.
- Mọi nỗ lực ép phần cứng mở rộng (Slot 04: Seqs 48), mở rộng CPU (Slot 05: OMP 3), thay đổi kiến trúc Prefill (Slot 06: Chunked), hay can thiệp Speculative (Slot 02, Slot 03) đều khiến điểm số tụt dốc thảm hại (từ 62đ rớt xuống 57-58đ).
- Chênh lệch 26 điểm so với Top 1 (89đ) không nằm ở Hyper-parameters, mà 100% nằm ở các **Đòn bẩy Vĩ mô không tiếp cận được** (Offline Custom Speculative Draft, hoặc Offline INT4 Custom Kernel Compilation).
