# Kết Quả Thử Nghiệm 1509 (Slot 10 - 20/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1509`
- **File Compose**: `10-docker-compose.yml` (bản đầu tiên)
- **Thời gian chấm**: 20/07/2026 15:09
- **Cấu hình**: Image v7 Lean + `--num-scheduler-steps=8` + Golden Base (`32K`, `Seqs=32`, `Level 3`)

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `Fail`
- **Chi tiết lỗi**: `exited 2 (Error): api_server.py: error: unrecognized arguments: --num-scheduler-steps`

## Phân Tích & Kết Luận

1. **vLLM v0.22.1 chưa hỗ trợ `--num-scheduler-steps`**: Cờ cắm `--num-scheduler-steps` chỉ có ở các bản vLLM mới hơn (từ v0.6.0+). Trên vLLM v0.22.1 của BTC, cờ này không tồn tại khiến server crash khi khởi động.
2. **Hành động khắc phục**: Đã gỡ bỏ cờ `--num-scheduler-steps` khỏi `python3_hijack` và rebuild lại `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v7`.
3. **Chuyển hướng thử nghiệm**: Nộp thử nghiệm Image v7 Lean (đã fix, không `--num-scheduler-steps`) cho Slot 11 (`11-docker-compose.yml`).
