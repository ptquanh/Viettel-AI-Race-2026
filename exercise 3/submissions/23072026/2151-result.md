# Kết Quả Thử Nghiệm 2151 (Slot 08 - 23/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2151`
- **File Compose**: `08-docker-compose.yml` (Slot 08)
- **Thời gian chấm**: 23/07/2026
- **Thay đổi**: v12 + `VLLM_NUM_SCHEDULER_STEPS=4`

## Kết Quả Chấm Điểm

- **Trạng thái**: THẤT BẠI (FAIL)
- **Lỗi**: `api_server.py: error: unrecognized arguments: --num-scheduler-steps`

## Phân Tích & Kết Luận

- Cờ `--num-scheduler-steps` (Multi-step Scheduler) không được hỗ trợ trên phiên bản vLLM này (v0.6.x), hoặc không tương thích với LFM.
- Thử nghiệm Multi-step thất bại hoàn toàn. Kết luận: Bỏ qua hướng tối ưu Multi-step, dồn toàn lực vào Fused Kernel Triton (Slot 11).
