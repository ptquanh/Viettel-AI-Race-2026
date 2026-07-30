# Kết quả Benchmark - Slot 1152 (8K Context + INT4 Marlin + FP8 KV Cache)

- **Cấu hình**: `docker-compose.slot02-8k-int4-humming.submission.yml` (Nộp lúc 11:52 30/07/2026)

## Kết quả chi tiết (Slot 1152)
- **Trạng thái**: **Chấm điểm thất bại (CRASH - 0 điểm)**
- **Nguyên nhân lỗi**:
  - `RuntimeError: NVML_SUCCESS == r INTERNAL ASSERT FAILED at CUDACachingAllocator.cpp:1165`
  - Lỗi xảy ra trong quá trình **Capturing CUDA graphs (FULL)**.
  - Do đẩy `gpu-memory-utilization=0.98` kết hợp với `max-model-len=8192`, vLLM cấp phát tới 14.42 GiB (2,500,512 tokens KV cache).
  - Khi CUDA Graph tiến hành capture cho FULL capture sizes (tới 512), PyTorch CUDACachingAllocator hết VRAM vật lý trên MIG H200 (18GB VRAM), gây ra sập container.

## Bài học rút ra & Khắc phục
- **VRAM Utilization**: Mức `0.98` là quá cao khi dùng CUDA Graph Full Capture. Cần trả về mức an toàn **`0.94` - `0.95`**.
- **Max Model Len**: Giảm `max-model-len` xuống 8192 là đúng đắn (tạo được 2.5 triệu token KV cache), nhưng cần giới hạn VRAM utilization để dành headroom cho CUDA Graph capture.
- **Tầm quan trọng của việc chờ Slot 02**: Nhờ chờ Slot 02 mà ta tránh được việc nộp trùng lỗi OOM cho Slot 03!
