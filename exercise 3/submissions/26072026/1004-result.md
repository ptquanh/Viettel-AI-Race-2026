# Kết quả chấm điểm Slot 07 (1004) - THẤT BẠI

- **Thời gian nộp**: 10:04 AM
- **Chiến lược**: Custom CUDA C++ Kernel Fusion (`v16`)
- **Cấu hình**: Champion Config (MAX_LEN=8192, GPU_MEM=0.94)
- **Điểm số**: `Chấm điểm thất bại`
- **Số request lỗi (Failed count)**: 0 (Crash ngay từ lúc khởi động Engine)

## Phân tích kết quả (Root Cause Analysis)

Container đã bị crash ngay từ bước `launch_core_engines` với mã lỗi `Exit Code 1`.
Lý do: **CUDA Illegal Memory Access** trong lúc Engine Core chạy bộ KV Cache giả lập (Memory Profiling warmup).

```
spawn contestant container: wait for pod ready: contestant pod failed: container "inference" exited 1 (Error)
...
RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
```

**Nguyên nhân gốc**:
Kernel C++ của chúng ta (ở tag `v16`) chưa xử lý được trường hợp `state_idx` nằm ngoài ranh giới khi Warmup, hoặc chênh lệch kiểu dữ liệu `int64_t` và `int32_t` từ Python truyền xuống C++. Điều này dẫn đến thao tác chọc nhầm vào bộ nhớ GPU không được cấp phát, khiến Context CUDA bị hỏng và PyTorch ném lỗi làm sập toàn bộ Engine V1.

**Khắc phục**:
Đã tung bản vá cực mạnh bằng tag `v16.1` để bắt lỗi out-of-bounds và ép kiểu an toàn. Sẽ test tiếp bản vá này ở **Slot 08**.
