# Kết Quả Thử Nghiệm 1353 (Slot 05 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1353`
- **File Compose**: `05-docker-compose.yml`
- **Thời gian chấm**: 22/07/2026 13:53
- **Cấu hình**: Image v11 (vLLM Modern Base) + Speculative Decoding Env Flags (`VLLM_SPECULATIVE_MODEL=[ngram]`, `VLLM_NUM_SPECULATIVE_TOKENS=3`, `VLLM_NGRAM_PROMPT_LOOKUP_MAX=4`, `VLLM_NGRAM_PROMPT_LOOKUP_MIN=1`)

## Kết Quả Chấm Điểm

- **Trạng thái**: ❌ **LỖI KHỞI ĐỘNG (Container Exit 2)**
- **Điểm số**: `0.00`
- **Error Trace**:
  ```text
  api_server.py: error: unrecognized arguments: --speculative-model --num-speculative-tokens 3 --ngram-prompt-lookup-max 4 --ngram-prompt-lookup-min 1
  ```
  _(Log gợi ý từ vLLM CLI parser: `[--spec-method {ngram, draft_model, eagle, medusa, ...}]`)_

## Phân Tích Nguyên Nhân & Bài Học Kỹ Thuật

1. **Phân tích Nguyên nhân thất bại**:
   - Tên cờ CLI trong vLLM mới đã thay đổi từ `--speculative-model [ngram]` thành **`--spec-method ngram`**.
   - Do `python3_hijack` truyền sai cờ `--speculative-model` thay vì `--spec-method`, Python `argparse` đã reject toàn bộ chuỗi argument đằng sau và báo lỗi Exit 2.

2. **Hướng Khắc Phục**:
   - Cập nhật `python3_hijack` trong Image v11.1: Sử dụng đúng cờ **`--spec-method ngram`** và **`--num-speculative-tokens 3`**.
