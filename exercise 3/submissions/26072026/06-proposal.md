# Kế hoạch Slot 06 (Cuối cùng) - Mảnh ghép cuối cùng: Chunked Prefill

Tuyệt vời! Nếu bạn muốn "khô máu" đến phút cuối, chúng ta vẫn còn một chiến thuật chưa từng được ghép nối hoàn chỉnh trên Image v14: **Chunked Prefill + Mở rộng Hàng đợi**.

### Phân tích thất bại của Slot 04:
Ở Slot 04, chúng ta ép `SEQS=48` nhưng TTFT lại bị dội ngược lên 54ms. Tại sao? 
Bởi vì khi 48 requests cùng ập vào, vLLM cố gắng **Prefill (tính toán Context)** cho toàn bộ 48 requests đó trong một nhịp CUDA Graph khổng lồ. Khối lượng tính toán khổng lồ này "chiếm đoạt" toàn bộ GPU, làm các request đang ở giai đoạn Decode bị bỏ đói (starved), và luồng Scheduler bị nghẽn, dẫn đến TTFT P50 tăng.

### Giải pháp Slot 06: Chunked Prefill
Nếu chúng ta chia nhỏ khối lượng Prefill khổng lồ đó ra thành các "mảnh" (Chunks) giới hạn ở mức 2048 tokens/nhịp, GPU sẽ có thể đan xen (interleave) giữa việc Prefill một ít cho request mới, và Decode cho request cũ.
Điều này giải quyết triệt để sự cố của Slot 04: Cho phép chúng ta nhồi `SEQS=48` để hấp thụ tối đa 70 user concurrent, mà **không làm nghẽn TTFT**!

### Cấu hình đề xuất (Dựa trên Slot 04):
- `VLLM_MAX_MODEL_LEN=4700` (Giữ nguyên để tiết kiệm VRAM)
- `VLLM_MAX_NUM_SEQS=48` (Mở rộng hàng đợi)
- `VLLM_BLOCK_SIZE=32` (Lùi về mốc 32 của Champion, vì 64 ở Slot 04 không hiệu quả)
- **THÊM MỚI**: 
  - `VLLM_ENABLE_CHUNKED_PREFILL=1`
  - `VLLM_MAX_NUM_BATCHED_TOKENS=2048`

Bạn có đồng ý tạo file `06-docker-compose.yml` với cấu hình đòn bẩy cuối cùng này không?
