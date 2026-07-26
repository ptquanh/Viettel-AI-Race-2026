# Kết quả Benchmark - 08:52 26/07/2026 (Slot 05 - Khai phá sức mạnh 3 Core CPU)

- **Cấu hình**: Image `v14` (Champion) + `OMP_NUM_THREADS=3` + `VLLM_LOGGING_LEVEL=ERROR` + `VLLM_NO_USAGE_STATS=1`.
- **Mục đích**: Chẩn đoán xem nút thắt cổ chai khiến TPOT kẹt ở 4ms có phải do vLLM Scheduler và PyTorch bị giới hạn trong 1 nhân CPU hay không. Mở khóa toàn bộ 3 nhân CPU của máy chấm.

### Chỉ số chi tiết:

- **Final Score**: **58.32**
- **TPOT (Median)**: 4ms
- **TTFT (P50)**: 60ms
- **TTFT (P95)**: 79ms
- **Failed / Total**: 5 / 420
- **Accuracy Drop**: 0%

### Đánh giá:

1. **TTFT P50 tăng vọt (45ms -> 60ms)**: Thay vì giải phóng tài nguyên, việc mở rộng `OMP_NUM_THREADS=3` trên một CPU quá yếu (3 Cores dùng chung cho toàn bộ OS, I/O, API Server, Scheduler và CUDAGraph) đã gây ra hiện tượng **Thread Contention (Tranh chấp tài nguyên) và Context Switching**. API Server và Scheduler phải liên tục nhường CPU cho các thread tính toán của OpenMP, dẫn đến độ trễ quản lý hàng đợi tăng cao.
2. **TPOT không đổi (4ms)**: Lại một lần nữa chứng minh: vLLM với LFM2.5 trên H200 không hề bị nghẽn ở CPU lúc đẩy lệnh Decode. Nó bị nghẽn hoàn toàn ở **Băng thông bộ nhớ VRAM (Memory Bandwidth Bound)** khi phải bốc 1.2GB weights cho mỗi token.
3. **OMP_NUM_THREADS=1 là tối ưu**: Thực tế việc giới hạn `OMP_NUM_THREADS=1` như trong Champion Config là một nước cờ cực kỳ thông minh để nhốt PyTorch backend vào 1 core, nhường 2 core còn lại cho API Async I/O và Scheduler hoạt động mượt mà.

### Kết luận:

- Thử nghiệm **THẤT BẠI**.
- Cấu hình Champion (62.67đ) chính là giới hạn vật lý tuyệt đối của Native FP8 trên hệ thống này nếu không có Speculative Decoding hoặc INT4. Mọi tinh chỉnh Hyper-parameters đều chỉ làm kết quả tệ đi.
- **Hướng tới Slot 06 (Chốt sổ)**: Trả lại toàn bộ về nguyên mẫu `1012-docker-compose.yml` (Champion Config) và lợi dụng "Golden Hour" (ít nhiễu hạ tầng) để nộp lần cuối cùng.
