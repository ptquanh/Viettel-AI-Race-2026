# Kết Quả Thử Nghiệm 1406 (Slot 06 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1406`
- **File Compose**: `06-docker-compose.yml`
- **Thời gian chấm**: 22/07/2026 14:06
- **Cấu hình**: Image v11.1 (vLLM Modern Base) + `--spec-method ngram` + `VLLM_NUM_SPECULATIVE_TOKENS=3` + `VLLM_NGRAM_PROMPT_LOOKUP_MAX=4` + `VLLM_NGRAM_PROMPT_LOOKUP_MIN=1`

## Kết Quả Chấm Điểm

- **Trạng thái**: ❌ **LỖI KHỞI ĐỘNG (Container Exit 2)**
- **Điểm số**: `0.00`
- **Error Trace**:
  ```text
  api_server.py: error: unrecognized arguments: --num-speculative-tokens --ngram-prompt-lookup-max 4 --ngram-prompt-lookup-min 1
  ```

## Phân Tích & Tiến Triển Đáng Chú Ý

1. **Đột phá lớn**:
   - Cờ `--spec-method ngram` đã được vLLM `api_server.py` **chấp nhận thành công 100%** (không còn bị báo lỗi unrecognized argument như ở Slot 04/05!).
2. **Nguyên nhân còn lại**:
   - Các cờ phụ `--num-speculative-tokens`, `--ngram-prompt-lookup-max` và `--ngram-prompt-lookup-min` đứng riêng lẻ chưa đúng tên hoặc cần gom vào cấu hình JSON `--speculative-config` hoặc cờ `--num-speculative-tokens`.
3. **Hướng Khắc Phục (Slot 07 - Image v11.2)**:
   - Sửa `python3_hijack` để truyền cờ `--spec-method ngram` kết hợp `--speculative-config` dạng JSON hoặc cờ chuẩn `--num-speculative-tokens 3`.
