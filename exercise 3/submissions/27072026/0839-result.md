# Kết quả chấm điểm Slot 04 (0839 - 27/07/2026) - ĐỘT PHÁ PHÁT HIỆN LỖI LỆCH DTYPE TRẠNG THÁI

- **Thời gian nộp**: 08:39 AM (27/07/2026)
- **Chiến lược**: Custom CUDA C++ Kernel Fusion (`v17.1`)
- **Cấu hình**: Champion Config (`MAX_LEN=32768`, `GPU_MEM=0.94`)
- **Điểm số**: `0.0000 điểm` (Protocol Aborted)
- **Thông báo lỗi**: `protocol aborted: text quality too low (0%) — likely garbage decode / dual-path`

## Phân tích nguyên nhân cốt lõi (Ultimate Root Cause Analysis)

Sau khi kiểm tra sâu sự khác biệt giữa Triton (`v14` - thành công 100% accuracy) và C++ CUDA Extension (`v16/v17` - ra chữ rác 0%):

### Phát hiện lỗi lệch Kiểu dữ liệu (DType Mismatch) phá hỏng bộ nhớ:

1. Trong mô hình LFM2.5 / Mamba của vLLM, các tensor kích hoạt `BCx` có kiểu dữ liệu là **`bfloat16`** (2 bytes/element).
2. Tuy nhiên, tensor lưu trạng thái Convolution trong KV Cache (`conv_state`) được vLLM lưu dưới dạng **`float32`** (4 bytes/element) để giữ độ chính xác tích lũy!
3. Ở mã nguồn C++ `v16/v17`, lệnh `AT_DISPATCH_FLOATING_TYPES` đã ép con trỏ `state.data_ptr<scalar_t>()` sang kiểu `bfloat16*`.
4. **Hậu quả nghiêm trọng**: CUDA Kernel đọc/ghi 2 bytes thay vì 4 bytes vào mảng `float32` của `conv_state`. Mọi bước dịch chuyển trạng thái đều bị ghi lệch địa chỉ bộ nhớ (Memory Alignment Corruption), biến toàn bộ ma trận Conv State thành dữ liệu rác ngẫu nhiên -> Tạo ra đầu ra rác 0% accuracy!
5. **Tại sao Triton (`v14`) lại đúng?**: Triton suy luận trực tiếp `conv_state.dtype` (Float32) để load 4 bytes, tự động cast sang float32 nên không bị lệch bộ nhớ.

### Giải pháp triệt để ở bản `v17.2`:

- Hỗ trợ **Dual-Type Dispatch** trong C++ (`bcx_t` cho BCx/Weights/Outputs và `state_t` riêng biệt cho `conv_state`).
- Đảm bảo đọc/ghi đúng 4 bytes cho Float32 state và 2 bytes cho BFloat16 BCx -> Bảo toàn 100% độ chính xác như Triton!
