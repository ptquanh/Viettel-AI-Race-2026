# Kết Quả Thử Nghiệm 2220 (Slot 10 - 23/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `2220`
- **File Compose**: `10-docker-compose.yml` (Slot 10)
- **Thời gian chấm**: 23/07/2026 (22:20)
- **Thay đổi**: v12 + `VLLM_CUDAGRAPH_MODE=DECODE_ONLY`

## Kết Quả Chấm Điểm

- **Trạng thái**: THẤT BẠI (FAIL)
- **Lỗi**: `KeyError: 'DECODE_ONLY'` tại `vllm/config/compilation.py`

## Phân Tích & Kết Luận

- Cờ `VLLM_CUDAGRAPH_MODE=DECODE_ONLY` không phải là một Enum giá trị hợp lệ trong Enum `CUDAGraphMode` của vLLM v0.6+.
- vLLM yêu cầu các giá trị như `FULL`, `PIECEWISE`, hoặc `NONE`.
- **Kết luận**: Giữ nguyên `VLLM_CUDAGRAPH_MODE=FULL`.
