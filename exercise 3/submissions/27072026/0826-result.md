# Kết quả chấm điểm Slot 03 (0826 - 27/07/2026) - LỖI RÁC ĐẦU RA (0% ACCURACY)

- **Thời gian nộp**: 08:26 AM (27/07/2026)
- **Chiến lược**: Custom CUDA C++ Kernel Fusion (`v17.0`)
- **Cấu hình**: Champion Config (`MAX_LEN=32768`, `GPU_MEM=0.94`)
- **Điểm số**: `0.0000 điểm` (Protocol Aborted)
- **Thông báo lỗi**: `protocol aborted: text quality too low (0%) — likely garbage decode / dual-path`

## Phân tích nguyên nhân gốc rễ (Pinpoint Root Cause Analysis)

Mặc dù container đã khởi động thành công và sinh ra câu trả lời, chất lượng văn bản bị trả về rác 100% (Text quality 0%) dẫn đến việc Trọng tài BTC dừng cuộc thi.

### Phát hiện lỗi logic trong C++ Kernel `v17.0`:

1. **Lỗi truyền CPU Tensor cho Bias**:
   - Trong `sitecustomize.py` của `v17.0`, khi `self.conv.bias` là `None`, câu lệnh `self.conv.bias if ... else torch.empty(0)` đã tạo ra một **CPU empty tensor** (`torch.empty(0)` trên CPU RAM).
   - Trong C++ (`lfm_fused_kernels.cu`), câu lệnh `bias.defined()` kiểm tra tensor này và trả về `TRUE` (vì CPU empty tensor vẫn là một tensor hợp lệ).
   - Tiếp đó, C++ lấy `bias.data_ptr()` - lúc này là một **con trỏ bộ nhớ CPU RAM** (chứ không phải GPU VRAM)!
   - CUDA Kernel trên GPU cố gắng đọc giá trị bias từ con trỏ CPU RAM này -> Nhận về **dữ liệu rác (Garbage Values)** -> Mỗi token decode ra bị biến dạng hoàn toàn thành rác!

### Giải pháp khắc phục ở bản `v17.1`:

1. **Sửa tầng C++ (`lfm_fused_kernels.cu`)**: Kiểm tra nghiêm ngặt `bias.defined() && bias.numel() > 0 && bias.is_cuda()`. Nếu không phải CUDA tensor hoặc rỗng, bắt buộc đặt `bias_ptr = nullptr`.
2. **Sửa tầng Python (`sitecustomize.py`)**: Truyền trực tiếp `self.conv.bias` (nếu `None` thì giữ nguyên `None`/Undefined Tensor) thay vì khởi tạo `torch.empty(0)`.
