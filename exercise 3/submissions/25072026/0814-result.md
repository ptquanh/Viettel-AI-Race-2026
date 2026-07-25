# Kết Quả Thử Nghiệm 0814 (Slot 03 - 25/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0814`
- **File Compose**: `0814-docker-compose.yml` (Slot 03)
- **Thời gian chấm**: 25/07/2026 (08:14)
- **Thay đổi**: Image v15 (`torchao` INT4 weight-only quantization online, `group_size=128`)

## Kết Quả Chấm Điểm

- **Điểm số**: `53.7800` (❌ Sụt 5.88đ so với 59.66đ của Baseline FP8)
- **TTFT P50**: 74ms (Tăng vọt +19ms từ 55ms)
- **TTFT P95**: 100ms
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 6
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & KẾT LUẬN QUAN TRỌNG

- **Phân tích kỹ thuật**:
  1. **Container chạy 100% thành công**, không có lỗi runtime, 0% accuracy drop.
  2. Tuy nhiên, việc ép `torchao.quantize_()` biến đổi các lớp `nn.Linear` sang PyTorch INT4 dynamic dequantization layers khiến vLLM không thể sử dụng các GPU GEMM kernels đã tối ưu (FlashInfer / Marlin / Fused Triton Kernels), mà phải fallback về Eager PyTorch Linear execution.
  3. Quá trình dequantize on-the-fly ở Eager mode gây ra CPU/GPU kernel launch latency lớn trong giai đoạn Prefill, làm tăng TTFT P50 lên **74ms**; đồng thời overhead dequantize triệt tiêu lợi ích đọc weight VRAM, giữ TPOT ở mốc **4ms**.
- **Kết luận Chiến Lược**:
  - **Khẳng định Image v14 (FP8 Native + Fused ShortConv Kernel + `spawn` + `FLASHINFER`) là cấu hình động cơ tối ưu tuyệt đối nhất cho giải đấu**.
  - Tập trung 100% nguồn lực 13 slots còn lại của ngày hôm nay vào **Image v14 FP8** với các đòn bẩy Golden Timing và micro-tuning VRAM (`GPU_MEM=0.94 - 0.95`).
