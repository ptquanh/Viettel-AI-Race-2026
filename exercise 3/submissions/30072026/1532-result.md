# Kết quả Slot 1532 (r25-humming-mig-persistent)

- **Điểm số**: **0.00** (Chấm điểm thất bại)
- **Thời gian chấm**: 30/07/2026 15:32
- **Cấu hình**:
  - `image`: docker.io/taze05/lfm25-h200-ers@sha256:dc9e6d3cbb0233756a3ecfaf3a913a52498d116ca1d2acaa1b4bac1da6fa3d2c
  - `--dtype=float16`
  - `--kv-cache-dtype=fp8`
  - `--mamba-cache-dtype=float16`
  - `--quantization=online_int4`

## Phân tích lỗi (Root Cause)

```
(EngineCore pid=79) ERROR 07-30 08:43:00 [core.py:1330] RuntimeError: For FP16/BF16 input, output must have the same dtype as inputs. For FP8 input, output must have dtype BF16
```

- **Nguyên nhân**: Xung đột dtype nghiêm trọng trong FlashAttention-3 (`torch.ops._vllm_fa3_C.fwd`). 
- Khi dùng `--kv-cache-dtype=fp8`, FlashAttention 3 trên H200 (Hopper) bắt buộc input tensor phải có dtype là `bfloat16` (BF16). Việc cấu hình `--dtype=float16` khiến FA3 kernel từ chối thực thi và ném `RuntimeError`, làm crash tiến trình `EngineCore`.
- **Kết luận quan trọng**: Khi dùng FP8 KV Cache trên Hopper H200, **BẮT BUỘC** phải dùng `--dtype=bfloat16`. Tuyệt đối không dùng `float16`.
