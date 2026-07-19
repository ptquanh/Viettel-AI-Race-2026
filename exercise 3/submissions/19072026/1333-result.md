# BÁO CÁO THỬ NGHIỆM SLOT 7 (1333 - ERROR)

## 1. Thông tin cấu hình

- **File nộp**: `1333-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Draft Model**: `LiquidAI/LFM2.5-350M-Instruct` (`Spec_Tokens=6`)
- **Baseline**: FP8 Native, `Seqs=32`, `Len=32768`

## 2. Kết quả chấm từ BTC Portal

- **Trạng thái**: `Chấm điểm thất bại` (Exited with code 2)
- **Lỗi chi tiết**:
  ```text
  api_server.py: error: argument --compilation-config/-cc: 1 validation error for CompilationConfig
    Input should be an object [type=dataclass_type, input_value=3, input_type=int]
  ```

## 3. Phân tích nguyên nhân & Giải pháp khắc phục

- **Nguyên nhân**: Cờ `--compilation-config` trong Pydantic v2 của vLLM v0.22.1 không chấp nhận số nguyên trực tiếp (`3`) mà yêu cầu một JSON object có trường `mode` (`{"mode": 3}`).
- **Khắc phục**:
  1. Đã sửa `python3_hijack` v2: Đổi từ `CMD+=("--compilation-config" "$COMPILATION_LEVEL")` sang `CMD+=("--compilation-config" "{\"mode\": $COMPILATION_LEVEL}")`.
  2. Đã rebuild & push lại image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2` với digest mới `sha256:140de0764e5231741b3827cfa2d94fc61ed358f79aab9bfd254d7ad7a1f20ced`.
  3. Tiến hành nộp lại Slot 7.
