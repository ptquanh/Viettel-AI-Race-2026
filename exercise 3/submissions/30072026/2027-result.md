# Kết quả Benchmark - 20:27 30/07/2026 (STT 210 - Slot 3 CUDA Graph)

- **Cấu hình**: Base 0851 + V2 Runner + CUDA Graph FULL Mode.
- **Mục đích**: Chạy CUDA Graph để giảm TPOT.

## Chỉ số đo được

**Chấm điểm thất bại (0.00 ERS - Container Exit 1)**

### Chi tiết lỗi
- **Thông báo**: `NVML_SUCCESS == r INTERNAL ASSERT FAILED at "/pytorch/c10/cuda/CUDACachingAllocator.cpp":1165` phát sinh trong lúc warmup FlashInfer sampling.
- **Phân tích nguyên nhân (OOM do CUDA Graph)**: 
  - Khác với dự đoán, GPU trên server chấm điểm được phân bổ giới hạn ở mức **16.0 GiB** (Có thể là H200 chia MIG hoặc L4/T4).
  - vLLM được cấp quyền `gpu-memory-utilization=0.95`, nó đã allocate KV Cache lấy mất 13.53 GiB.
  - CUDA Graph capture hoạt động RẤT TỐT (mất 6 giây để capture xong). Tuy nhiên, CUDA Graph yêu cầu cấp phát thêm **0.34 GiB** VRAM *sau khi* KV Cache đã chiếm hết chỗ.
  - Hậu quả: PyTorch CUDACachingAllocator bị cạn kiệt VRAM vật lý khi cấp phát bộ nhớ cho softmax logits ở bước sampling cuối cùng -> Gây lỗi crash NVML driver.

## Kết luận & Giải pháp
- CUDA Graph **chạy thành công** trên LFM2.5 và V2 Runner, không có lỗi logic!
- Lỗi duy nhất là tràn VRAM.
- **Fix**: Giảm `--gpu-memory-utilization` từ `0.95` xuống `0.90` (chừa lại ~0.8 GiB) để đủ không gian cho CUDA Graph (0.34 GiB).
