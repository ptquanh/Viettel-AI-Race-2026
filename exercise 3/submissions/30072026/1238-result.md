# Kết quả Slot 1238 (Config F2)

- **Điểm số**: 66.2600
- **Thời gian chấm**: 30/07/2026
- **Cấu hình (Config F2)**: 
  - `image`: docker.io/taze05/lfm25-h200-ers@sha256:2f1c (Humming W4)
  - `max-model-len`: 8192
  - `gpu-memory-utilization`: 0.95
  - `VLLM_USE_V2_MODEL_RUNNER`: 1
  - `quantization`: online_int4 + fp8 KV cache

## Chỉ số chi tiết
- ers: 66.26
- f_delta: 1
- penalty: 1
- final_score: 66.26
- total_count: 420
- ttft_p50_ms: 46
- ttft_p95_ms: 69
- failed_count: 6
- warmup_count: 0
- accuracy_drop: 0
- tbt_median_ms: 3
- tokens_per_sec: 0.0494

## Đánh giá
- **Thất bại trong việc giảm TPOT**: Việc hạ `max-model-len` xuống 8192 để giải phóng VRAM không hề giúp giảm TPOT. TPOT vẫn ở mức 3ms.
- **Độ ổn định giảm nhẹ**: Số lượng failed_count tăng từ 4 (slot 1148) lên 6, khiến điểm số rớt 1.35 điểm so với cấu hình 32K context.
- **Kết luận**: Tối ưu bằng flag (flag-only optimization) đã chính thức chạm trần cứng. Bắt buộc phải chuyển sang can thiệp kernel và mã nguồn vLLM (Phase 1, 2, 3) để ép TPOT xuống dưới 3ms.
