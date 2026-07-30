# Kết quả Benchmark - Slot 1204 (8K Context + INT4 Marlin + FP8 KV Cache + V2 Runner OFF)

- **Cấu hình**: `docker-compose.slot03-8k-int4-humming-v2off.submission.yml` (Đã đổi tên thành `1204-docker-compose.yml`)

## Kết quả chi tiết (Slot 1204)

- **Điểm chung cuộc (ERS / Final Score)**: **62.2600**
- **TTFT P50**: **53ms**
- **TTFT P95**: **78ms**
- **TBT Median (TPOT)**: **4ms**
- **Failed Count**: **6** / 420
- **Warmup Count**: 0
- **Accuracy Drop**: 0
- **Tokens/sec**: 0.0494

## Nhận xét & Đánh giá

- **Đã khắc phục lỗi OOM**: Việc hạ `gpu-memory-utilization=0.94` giúp container khởi tạo thành công 100% không còn bị crash CUDA Graph Capture.
- **TPOT tăng lên 4ms**: V2 Model Runner = 0 khiến TPOT bị tăng từ 3ms lên 4ms (sụt điểm từ ~67.6đ xuống 62.26đ).
- **TTFT tăng**: TTFT P50 tăng từ 43-45ms lên 53ms, P95 tăng lên 78ms khi tắt V2 Model Runner.
- **Kết luận**: V2 Model Runner (`VLLM_USE_V2_MODEL_RUNNER=1`) là yếu tố bắt buộc để đạt TPOT 3ms và TTFT P50 < 45ms.
