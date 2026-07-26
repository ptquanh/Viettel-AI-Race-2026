# Kế hoạch Slot 05 - Khai phá sức mạnh 3 Core CPU (OMP_NUM_THREADS=3)

Qua kết quả của Slot 04 (60.41đ, TTFT tăng lên 54ms), chúng ta thấy rõ việc tăng `MAX_NUM_SEQS=48` và `BLOCK_SIZE=64` không mang lại hiệu quả mà còn gây thêm gánh nặng cho Scheduler.
TPOT vẫn kẹt cứng ở 4ms. Các đòn bẩy vĩ mô (Speculative, INT4) đều đã bị bẻ gãy.

**VẬY TOP 1 LÀM THẾ NÀO ĐỂ ĐẠT 89 ĐIỂM?**
Một khả năng chưa được khai thác triệt để: **Nút thắt cổ chai không nằm ở GPU VRAM, mà nằm ở 3 Core CPU siêu yếu của MiG host!**
Trong cấu hình Champion (62.67đ), chúng ta đang để `OMP_NUM_THREADS=1`. Điều này có nghĩa là vLLM Scheduler và PyTorch backend chỉ được dùng đúng 1 nhân CPU để quản lý vòng lặp Event Loop, PagedAttention, và đẩy CUDAGraph lên GPU. 2 nhân CPU còn lại hoàn toàn bị bỏ phí!

### Chiến lược Slot 05:

Chúng ta sẽ quay về **nguyên bản cấu hình Champion Config (Image v14)** (giữ nguyên Max Len 8192, Seqs 32, Block 32), nhưng thay đổi 2 tham số:

1. `OMP_NUM_THREADS=3` (Khai thác 100% tài nguyên CPU của host).
2. Tắt logging triệt để để giảm I/O block CPU: `VLLM_NO_USAGE_STATS=1` và `VLLM_LOGGING_LEVEL=ERROR`.

Nếu CPU thực sự là điểm nghẽn ngầm khiến TPOT bị đội lên 4ms (do CPU submit lệnh CUDA chậm hơn tốc độ GPU xử lý), việc mở khóa 3 Core CPU có thể kéo TPOT xuống 2ms!

Bạn đồng ý tạo Slot 05 chứ?
