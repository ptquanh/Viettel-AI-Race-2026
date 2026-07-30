# Kết quả Slot 1510 (Phase 1 Image - CUDA Graph Capture Sizes Optimization)

- **Điểm số**: 66.2700
- **Thời gian chấm**: 30/07/2026
- **Cấu hình (Phase 1 Image)**:
  - `image`: docker.io/ptquanh/sandbox-runtime:phase1 (CUDA Graph capture sizes [1..70])
  - `max-model-len`: 32768
  - `gpu-memory-utilization`: 0.95
  - `VLLM_USE_V2_MODEL_RUNNER`: 1
  - `quantization`: online_int4 + fp8 KV cache

## Chỉ số chi tiết

- ers: 66.27
- f_delta: 1
- penalty: 1
- final_score: 66.27
- total_count: 420
- ttft_p50_ms: 47
- ttft_p95_ms: 72
- failed_count: 6
- warmup_count: 0
- accuracy_drop: 0
- tbt_median_ms: 4
- tokens_per_sec: 0.0492

## Đánh giá

- **Thử nghiệm Custom Image Phase 1**: Đã giảm CUDA graph capture sizes từ 76 xuống 12 sizes `[1..70]`.
- **Kết quả**: Server khởi tạo thành công và chạy ổn định, tuy nhiên `tbt_median_ms` (TPOT) lại bị tăng nhẹ lên 4ms (so với 3ms của baseline Humming W4), khiến ERS đạt 66.27.
- **Nguyên nhân**: Custom capture sizes chưa bao phủ tối ưu hết các batch size biến động trong benchmark hoặc V2 model runner bị overhead khi lookup graph size.
- **Hướng tiếp theo**: Tiến hành Phase 2 (Fused Decode Kernel) để tối ưu trực tiếp kernel launch overhead.
