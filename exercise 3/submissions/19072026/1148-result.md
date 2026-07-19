# BÁO CÁO THỬ NGHIỆM SLOT 6 (1148 - ERROR)

## 1. Thông tin cấu hình

- **File nộp**: `1148-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2` (digest v2-alpha)
- **Draft Model**: `LiquidAI/LFM2.5-350M-Instruct` (`Spec_Tokens=3`)
- **Baseline**: FP8 Native, `Seqs=32`, `Len=32768`

## 2. Kết quả chấm từ BTC Portal

- **Trạng thái**: `Chấm điểm thất bại` (Exited with code 2)
- **Lỗi chi tiết**:
  ```text
  api_server.py: error: argument --compilation-config/-cc: 1 validation error for CompilationConfig
  level
    Unexpected keyword argument [type=unexpected_keyword_argument, input_value=3, input_type=int]
  ```

## 3. Phân tích nguyên nhân & Giải pháp khắc phục

- **Nguyên nhân**: Cờ `--compilation-config={\"level\":3}` được truyền theo dạng JSON dictionary string, tuy nhiên Pydantic model `CompilationConfig` của vLLM v0.22.1 không có trường tên là `level` mà nhận trực tiếp giá trị số nguyên (`3`).
- **Khắc phục**:
  1. Đã sửa `python3_hijack` v2: Đổi từ `CMD+=("--compilation-config={\"level\":$COMPILATION_LEVEL}")` sang `CMD+=("--compilation-config" "$COMPILATION_LEVEL")`.
  2. Đã rebuild & push lại image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2` với digest mới `sha256:17a8aebe3a77b40ced22c45f91137b5991ec140d1d054b6b5596e11d2d9ea0bf`.
  3. Tiến hành nộp lại Slot 6.
