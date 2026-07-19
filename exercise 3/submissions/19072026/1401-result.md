# BÁO CÁO THỬ NGHIỆM SLOT 8 (1401 - ERROR)

## 1. Thông tin cấu hình

- **File nộp**: `1401-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Draft Model**: `LiquidAI/LFM2.5-350M-Instruct` (`Spec_Tokens=6`)
- **Thời gian nộp**: 14:01 (19/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Trạng thái**: `Chấm điểm thất bại` (Exited with code 2)
- **Lỗi chi tiết**:
  ```text
  api_server.py: error: unrecognized arguments: --speculative-model --num-speculative-tokens 6 --speculative-disable-mqa-scorer 0.0.0.0 8000 /model LFM2.5-1.2B-Instruct
  ```

## 3. Phân tích nguyên nhân & Giải pháp khắc phục

- **Nguyên nhân phát hiện**:
  1. Trong vLLM v0.22.1, các cờ CLI cho Speculative Decoding là `--spec-method draft_model`, `--spec-model` (thay vì `--speculative-model`), `--spec-tokens` (thay vì `--num-speculative-tokens`).
  2. Vòng lặp forward cờ CLI cũ trong `python3_hijack` khi lọc danh sách arguments bị sót giá trị (như `0.0.0.0`, `8000`, `/model`, `LFM2.5-1.2B-Instruct`) khiến chúng bị đẩy xuống cuối CLI dưới dạng positional args không hợp lệ.
- **Khắc phục**:
  1. Đã cập nhật `python3_hijack` v2 với cờ CLI chuẩn của vLLM v0.22.1: `--spec-method draft_model`, `--spec-model $SPECULATIVE_MODEL`, `--spec-tokens $NUM_SPECULATIVE_TOKENS` (và `--spec-method ngram` nếu chạy N-gram).
  2. Đã xóa bỏ vòng lặp `shift` dư thừa để triệt tiêu hoàn toàn các positional args rác ở cuối command line.
  3. Đã Rebuild & Push Image **`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`** mới (Digest `sha256:a597a800...`).
