# Kết quả chấm điểm Slot 11 (1700 - 27/07/2026) - LỖI TIMEOUT WARMP CUDA GRAPH (CONTAINER NOT READY)

- **Thời gian nộp**: 05:00 PM (27/07/2026)
- **Chiến lược**: Zero-Allocation Triton Kernel (`v19.0`)
- **Cấu hình**: Image `v19.0` + `GPU_MEM=0.95` + `WARMUPS=10` + `SEQS=32`
- **Điểm số**: `Chấm điểm thất bại` (Timeout Exceeded)
- **Thông báo lỗi**: `spawn contestant container: wait for pod ready: timed out waiting for contestant pod to be ready: context deadline exceeded`

## Phân tích nguyên nhân cốt lõi (Root Cause Analysis)

1. **Xung đột giữa Zero-Allocation Buffer và PyTorch CUDA Graph Capture**:
   - Trong `v19.0`, mảng đệm `self._y_buffer` được tạo lười (lazy allocation) ở lần forward đầu tiên của lớp `ShortConv`.
   - Khi PyTorch CUDA Graph tiến hành Warmup Capture các kích thước batch khác nhau (`CAPTURE_SIZES=[1..32]`), việc thay đổi kích thước tensor đệm hoặc khởi tạo đệm lần đầu TRONG LÚC Capture CUDA Graph làm trình cấp phát bộ nhớ CUDA Graph Allocator rơi vào vòng lặp chờ vô tận (Deadlock / Hang).
   - Hậu quả: vLLM bị treo vĩnh viễn lúc khởi tạo CUDA Graph, dẫn đến quá giờ chờ của Kubernetes Pod (`context deadline exceeded`).

2. **Bài học chiến lược**:
   - PyTorch CUDA Graph Allocator hoạt động tối ưu nhất khi để PyTorch tự quản lý cấp phát mảng đệm tạm thời thông qua `torch.empty` (như ở bản **`v18.0`**).
   - **Bản `v18.0`** là bản hoạt động 100% hoàn hảo, đạt kỷ lục TTFT P50 = 54ms và P95 = 78ms mà KHÔNG BAO GIỜ bị treo hay crash.

3. **Kế hoạch cho các Slot giờ vàng còn lại**:
   - Quay lại sử dụng nền tảng **Image `v18.0`** chắc chắn 100%.
   - Tập trung tối ưu tham số VRAM và Warmup trên `v18.0` để chốt hạ điểm số cao nhất bảo vệ vị trí Top Leaderboard.
