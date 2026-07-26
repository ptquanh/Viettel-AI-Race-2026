# Kế hoạch Z1 (INT4 torchao) - Rủi ro & Đề xuất

Theo kế hoạch, Slot 04 sẽ là Z1 (Image v15 - INT4 torchao online quantization). 
Tuy nhiên, tra cứu lại log ngày 25/07 (Slot 03 - `0814-result.md`), Image v15 đã từng được nộp và **THẤT BẠI NẶNG NỀ (53.78đ)**.

**Lý do:** 
Khi dùng `torchao` ép weights xuống INT4 on-the-fly, vLLM không nhận diện được lớp layer lượng tử hóa này nên đã **fallback (trả về) chạy bằng PyTorch Eager thuần túy** (không dùng được GPU Fused Kernels/Triton). 
Hậu quả: 
- TTFT P50 vọt lên 74ms (do overhead dequantize trên CPU/GPU).
- TPOT không hề giảm (vẫn 4ms) vì tốc độ tính toán chậm chạp của Eager đã triệt tiêu hoàn toàn lợi ích băng thông của INT4.

### Đề xuất cho Slot 04 & 05
Vì việc viết lại Native C++ Kernel cho INT4 AWQ/Marlin ngay lúc này là bất khả thi (không can thiệp được source code vLLM C++ từ bên ngoài container), và mọi đòn bẩy Speculative/Compiler đều đã bị bẻ gãy, chúng ta chỉ còn cách:

**VẮT KIỆT SỨC MẠNH CỦA CHAMPION CONFIG (FP8) BẰNG HYPER-PARAMETERS:**
1. **Slot 04 (VRAM & Block Size)**: Dùng lại cấu hình 62.67đ nhưng thay đổi `VLLM_BLOCK_SIZE=64` (giúp giảm số lượng block cần quản lý trong Paged Attention) và `VLLM_GPU_MEMORY_UTILIZATION=0.96` (trước đó 0.94 là an toàn, 0.98 là OOM, 0.96 có thể là điểm ngọt).
2. **Slot 05 (Max Seq & Chunk)**: Thử ép `VLLM_MAX_NUM_SEQS=48` (kết hợp với `VLLM_MAX_MODEL_LEN=4700` để không bị OOM) nhằm nuốt trọn số lượng concurrent request, giảm tối đa hàng đợi.

Bạn có đồng ý hủy Z1 để dùng Slot 04 cho việc **Tuning Hyper-Parameters (Block Size = 64, Max Len = 4700, Seqs = 48)** không? Nếu đồng ý tôi sẽ tạo file compose ngay!
