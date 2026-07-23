# Kết Quả Thử Nghiệm 1415 (Slot 05 - 23/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1415`
- **File Compose**: `1415-docker-compose.yml` (Slot 05)
- **Thời gian chấm**: 23/07/2026 14:15
- **Cấu hình**: Image v12.1 (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v12.1`) + Speculative Decoding Flags (`--spec-model /draft_model --spec-tokens 2`)

## Kết Quả Chấm Điểm

- **Trạng thái**: `FAIL` (Exited with code 1)
- **Điểm số**: `0`

## Chi Tiết Lỗi Log

```text
File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/async_llm.py", line 217, in from_vllm_config
RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
```

## Phân Tích & Nguyên Nhân

1. **Nguyên nhân thất bại**:
   - Traceback chỉ rõ lỗi xuất phát từ `vllm/v1/engine/async_llm.py`. Đây là **Engine V1** (kiến trúc hoàn toàn mới của vLLM v0.6+).
   - Engine V1 hiện tại đang được bật mặc định (hoặc được trigger tự động) trên nhánh mới của vLLM, nhưng nó **chưa hỗ trợ Speculative Decoding** đối với kiến trúc Recurrent của LFM2.5 (hoặc bị crash khi khởi tạo Draft Model bên trong V1).
2. **Khắc phục**:
   - Sử dụng Buffer (Slot 06) để vô hiệu hóa Engine V1 bằng cách thêm biến môi trường `VLLM_USE_V1=0` vào docker compose, ép vLLM fallback về Engine V0 (V0 hỗ trợ Speculative Decoding đầy đủ hơn).
   - Cập nhật file compose Slot 06.
