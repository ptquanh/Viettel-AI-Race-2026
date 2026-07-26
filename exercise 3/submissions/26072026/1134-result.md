# Kết quả chấm điểm Slot 09 (1134) - THẤT BẠI

- **Thời gian nộp**: 11:34 AM
- **Chiến lược**: Custom CUDA C++ Kernel Fusion (`v16.2`)
- **Cấu hình**: Champion Config (MAX_LEN=8192, GPU_MEM=0.94)
- **Điểm số**: `Chấm điểm thất bại`
- **Số request lỗi (Failed count)**: 0 (Crash ngay lúc Engine khởi tạo)

## Phân tích kết quả thực sự (Breakthrough Root Cause Analysis)

Sau khi kiểm tra sâu sự khác biệt giữa Triton (`v14` - thành công) và PyBind11 C++ Extension (`v16/v16.1/v16.2` - thất bại):

```
RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
```

### Phát hiện nguyên nhân cốt lõi:

1. Trong quá trình Engine V1 Profiling/Warmup, một số tensor như `state_indices` hoặc `self.conv.bias` có thể bằng `None` (hoặc `kv_cache` rỗng).
2. Ở bản **`v14` (Triton)**: Khi truyền `None` vào Triton Python wrapper, Python gọi `None.data_ptr()`, lập tức quăng lỗi `AttributeError`. Lỗi này được khối `try...except` trong Python bắt trọn vẹn và tự động **Fallback** về `_orig_forward_cuda` của vLLM.
3. Ở bản **`v16` (PyBind11 C++)**: PyBind11 nhận giá trị `None` từ Python và tự động chuyển đổi nó thành một `at::Tensor()` chưa khởi tạo (`undefined tensor`). Khi C++ gọi `.to(...)` hay `.data_ptr()` trên undefined tensor này, nó gây ra **Segmentation Fault (Hard Crash)** ở tầng C++. Vì là Segfault ở tầng C++, Python không bắt được qua `try...except`, khiến Worker process chết ngay lập tức (exit code 1).

### Giải pháp triệt để (Bản vá v16.3):

- **Ở phía Python (`sitecustomize.py`)**: Kiểm tra trực tiếp `if state_indices is None or self.conv.bias is None:` trước khi gọi kernel C++. Nếu `None`, trả về `_orig_forward_cuda` ngay lập tức!
- **Ở phía C++ (`lfm_fused_kernels.cu`)**: Thêm kiểm tra `!bcx.defined() || !state_indices.defined() ...`. Nếu undefined, ném văng ra `std::invalid_argument` để PyBind11 biến thành Python exception an toàn thay vì crash process.
