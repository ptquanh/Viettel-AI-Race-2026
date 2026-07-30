# Kết quả Benchmark - 17:40 30/07/2026 (STT 207 - r28-humming-v2-fullgraph)

- **Cấu hình**: Image `sha256:2f1c` + `--compilation-config={"level":3,"cudagraph_mode":"FULL",...}`.
- **Mục đích**: Thử nghiệm Full CUDA Graph cho cả Prefill & Decode với V2 Model Runner.

## Chỉ số đo được

**Chấm điểm thất bại (0.00 ERS - Container Exit 2)**

### Chi tiết lỗi
- **Lỗi Arg Parsing Pydantic**: 
  `api_server.py: error: argument --compilation-config/-cc: 1 validation error for CompilationConfig level Unexpected keyword argument [type=unexpected_keyword_argument, input_value=3, input_type=int]`
- **Nguyên nhân**: Trường `level` không phải là keyword argument hợp lệ trong object JSON của `--compilation-config` trên vLLM (level là cờ riêng `--optimization-level 3`).

## Kết luận
- Thử nghiệm `--compilation-config` bằng JSON string thất bại do sai schema Pydantic.
- Không thể truyền `level` bên trong dict `--compilation-config`.
