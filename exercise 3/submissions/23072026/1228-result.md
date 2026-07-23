# Kết Quả Thử Nghiệm 1228 (Slot 04 - 23/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1228`
- **File Compose**: `1228-docker-compose.yml` (Slot 04)
- **Thời gian chấm**: 23/07/2026 12:28
- **Cấu hình**: Image v12 (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v12`) + Speculative Decoding Flags (`--speculative-model /draft_model --num-speculative-tokens 2 --use-v2-block-manager`)

## Kết Quả Chấm Điểm

- **Trạng thái**: `FAIL` (Exited with code 2)
- **Điểm số**: `0`

## Chi Tiết Lỗi Log

```text
api_server.py: error: unrecognized arguments: --speculative-model --num-speculative-tokens 2 --use-v2-block-manager
```

## Phân Tích & Nguyên Nhân

1. **Nguyên nhân thất bại**:
   - Engine vLLM v0.6+ đã đổi tên các cờ CLI liên quan tới Speculative Decoding.
   - Cờ `--speculative-model` bị đổi thành `--spec-model`.
   - Cờ `--num-speculative-tokens` bị đổi thành `--spec-tokens`.
   - Cờ `--use-v2-block-manager` đã bị loại bỏ vì Block Manager v2 đã là mặc định.
2. **Khắc phục**:
   - Cập nhật script `python3_hijack` trong `vllm_lfm25_fp8_kernels_v12`.
   - Rebuild và push Image mới dưới tag `vllm-lfm25-fp8-kernels-v12.1`.
   - Đổi slot tiếp theo thành `v12.1` để nộp lại.
