# Kết Quả Thử Nghiệm 1053 (Slot 04 - 22/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1053`
- **File Compose**: `04-docker-compose.yml`
- **Thời gian chấm**: 22/07/2026 10:53
- **Cấu hình**: Image v10.2 + Speculative Decoding Flags (`--speculative-model [ngram]`, `--num-speculative-tokens 3`, `--ngram-prompt-lookup-max 4`, `--ngram-prompt-lookup-min 1`)

## Kết Quả Chấm Điểm

- **Trạng thái**: ❌ **LỖI KHỞI ĐỘNG (Container Exit 2)**
- **Điểm số**: `0.00`
- **Error Trace**:
  ```text
  api_server.py: error: unrecognized arguments: --speculative-model --num-speculative-tokens 3 --ngram-prompt-lookup-max 4 --ngram-prompt-lookup-min 1
  ```

## Phân Tích Nguyên Nhân & Bài Học Kỹ Thuật

1. **Phân tích Nguyên nhân thất bại**:
   - Base Image `vllm/vllm-openai:v0.22.1` quá cũ nên CLI Parser của `api_server.py` **chưa hỗ trợ các cờ Prompt Lookup / Speculative Decoding** (`--speculative-model [ngram]`, `--ngram-prompt-lookup-max`, v.v.).
   - Việc truyền các tham số này vào `v0.22.1` khiến Python `argparse` báo lỗi `unrecognized arguments` và exit code 2 ngay khi boot.

2. **Hướng Khắc Phục (Nâng cấp lên Image v11 - vLLM Version Upgrade)**:
   - Chuyển ngay sang **Nhánh B (Buổi chiều)** trong `plan-2207.md`: Build **Custom Image v11** dựa trên phiên bản vLLM mới hơn (`v0.24.x` / `v0.25.x` hoặc `latest`) có hỗ trợ đầy đủ Speculative Decoding và Prompt Lookup Decoding!
