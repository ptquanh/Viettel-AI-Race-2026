# Kết Quả Thử Nghiệm 2032 (Slot 10 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2032`
- **File Compose**: `2032-docker-compose.yml` (Slot 10)
- **Thời gian chấm**: 22/07/2026 20:32
- **Cấu hình**: Image v11 (Modern vLLM Engine Base) + **`VLLM_QUANTIZATION=none` (BF16 Native)** + `OMP_NUM_THREADS=1` + `VLLM_GPU_MEMORY_UTILIZATION=0.95` + `VLLM_CUDAGRAPH_MODE=FULL` + `FLASHINFER` + `VLLM_BLOCK_SIZE=32`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `46.83` (❌ Sụt giảm nghiêm trọng -10.92 điểm so với FP8 ở Slot 09!)
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `46.83`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `62 ms`
- **TTFT P95**: `94 ms`
- **TPOT Median**: **`6 ms`** (⚠️ Tăng từ 4ms lên 6ms!)
- **Failed Count**: `6`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận Cốt Lõi

1. **Phát Hiện Vật Lý Quan Trọng**:
   - Khi chuyển sang **BF16 thuần** (bỏ `VLLM_QUANTIZATION=fp8`), dung lượng weights cần load mỗi token tăng gấp 2 lần (từ 1.2 GB lên 2.4 GB).
   - Trên phân vùng 1/4 MiG H200 (băng thông HBM ~1.2 TB/s), việc đọc 2.4 GB weights chiếm tới **2.0ms pure HBM transfer time** cho mỗi token (thay vì 1.0ms ở FP8).
   - Hậu quả: TPOT tăng từ **4ms → 6ms** (+50% trễ decode!), kéo điểm ERS sụt giảm thảm hại từ 57.75đ xuống **46.83đ**.
2. **Bài Học Vô Giá Về Kiến Trúc & Quantization**:
   - **FP8 là BẮT BUỘC (MANDATORY)** cho LFM2.5 trên MiG H200 để giữ TPOT ≤ 4ms.
   - Giả thuyết cho rằng FP8 Dynamic có dequantization overhead lớn hơn chi phí đọc HBM là **SAI**. Việc tiết kiệm 50% băng thông HBM của FP8 quan trọng hơn nhiều so với dequantization computation.
3. **Bước Tiếp Theo**:
   - **Tái lập FP8** (`VLLM_QUANTIZATION=fp8`).
   - Thử nghiệm **Multi-Step Scheduling** (`--num-scheduler-steps=2/4`) trên nền FP8 để giảm CPU↔GPU sync overhead mà vẫn giữ nguyên lợi thế 50% băng thông HBM của FP8!
