# Kết quả chấm điểm Slot 05 (0919 - 27/07/2026) - KẾT QUẢ VĂN BẢN RÁC (0% ACCURACY)

- **Thời gian nộp**: 09:19 AM (27/07/2026)
- **Chiến lược**: Custom CUDA C++ Kernel Fusion (`v17.2` Dual-Type Dispatch)
- **Cấu hình**: Champion Config (`MAX_LEN=32768`, `GPU_MEM=0.94`)
- **Điểm số**: `0.0000 điểm` (Protocol Aborted)
- **Thông báo lỗi**: `protocol aborted: text quality too low (0%) — likely garbage decode / dual-path`

## Phân tích chiến lược (Strategic Analysis & Pivot)

Mặc dù bản `v17.2` đã xử lý ép kiểu Dual-Type Dispatch giữa Float32 và BFloat16, kết quả đầu ra vẫn bị hỏng (Text Quality 0%).

### Đánh giá nguyên nhân hệ thống:

1. **Rủi ro của C++ PyBind11 AOT Compilation trong Docker**:
   - Việc tự biên dịch C++ qua `setup.py` trong môi trường Docker làm xuất hiện các sai lệch ABI (Application Binary Interface) ẩn với PyTorch/vLLM runtime của NVIDIA.
   - Thao tác truyền con trỏ thủ công (`data_ptr`) ở C++ rất dễ bị sai lệch khi vLLM V1 thực hiện tối ưu hóa bố cục bộ nhớ (Memory Layout) trên GPU H200.
2. **Ưu thế vượt trội của Triton Compiler (`v14`)**:
   - Ở bản **`v14` (Triton)**, mô hình đạt **62.67 điểm (100% Accuracy)** và không bao giờ gặp lỗi rác chữ hay ABI.
   - Triton được tích hợp sẵn trong PyTorch/vLLM, tự động quản lý kiểu dữ liệu, con trỏ bộ nhớ và tối ưu hóa câu lệnh CUDA PTX ở mức phần cứng.

### Quyết định chuyển hướng chiến lược (Strategic Pivot):

- Từ bỏ phương pháp C++ AOT PyBind11 đầy rủi ro.
- Quay trở lại nền tảng **Triton JIT Compiler** vô địch của `v14`, phát triển tiếp phiên bản **`v18` Triton Mega Fusion Kernel** (`InProj + ShortConv + OutProj`) để vừa đảm bảo **100% độ chính xác văn bản** vừa **giảm TPOT < 2ms**!
