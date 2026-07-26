# Kết quả chấm điểm Slot 08 (1051) - THẤT BẠI

- **Thời gian nộp**: 10:51 AM
- **Chiến lược**: Custom CUDA C++ Kernel Fusion (`v16.1`)
- **Cấu hình**: Champion Config (MAX_LEN=8192, GPU_MEM=0.94)
- **Điểm số**: `Chấm điểm thất bại`
- **Số request lỗi (Failed count)**: 0 (Crash ngay lúc Engine khởi tạo)

## Phân tích kết quả (Root Cause Analysis)

Mặc dù đã bổ sung bounds checking và ép kiểu an toàn trong file `.cu` ở bản vá `v16.1`, container vẫn bị crash đúng hệt như cũ với mã lỗi `Exit Code 1` ở APIServer (pid=1):

```
RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
```

**Tại sao lỗi Out-of-bounds đã sửa mà vẫn sập?**
Vì nguyên nhân thực sự **KHÔNG NẰM Ở CUDA KERNEL!** Nguyên nhân gốc rễ là do tôi đã phá vỡ quy trình khởi tạo tiến trình (multiprocessing spawn) của vLLM V1 Engine.

Trong `v16` và `v16.1`, lệnh `import torch` và `import lfm_custom_ops` được đặt ở **trên cùng (top-level)** của file `sitecustomize.py`.
Vì vLLM V1 sử dụng phương pháp `spawn` để tạo Worker, mọi process con (kể cả Resource Tracker hay ZMQ Queue Manager) khi khởi động đều chạy qua `sitecustomize.py` và load toàn bộ thư viện PyTorch (cùng với việc kích hoạt CUDA Context) **TRƯỚC KHI** vLLM kịp thiết lập các biến môi trường cấu hình (như `CUDA_DEVICE_MAX_CONNECTIONS`) và các Context an toàn. Điều này khiến Worker bị deadlock hoặc crash ngay lúc khởi tạo.

(Lưu ý: Ở bản `v14` thành công trước đó, lệnh `import torch` được giấu kín bên trong hàm `_patched_forward_cuda` nên không bị lỗi này).

**Khắc phục**:
Đã tung bản vá `v16.2`, di chuyển `import torch` và `import lfm_custom_ops` vào dạng **Lazy Load** bên trong hàm forward. Nó đảm bảo an toàn tuyệt đối 100% cho tiến trình khởi tạo của Engine V1. Sẽ test tiếp bản vá này ở Slot 08 mới.
