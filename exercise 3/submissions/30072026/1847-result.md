# Kết quả Benchmark - 18:47 30/07/2026 (STT 209 - final-lastshot-75)

- **Cấu hình**: Image `sha256:2f1c` (Champion 0851 Base) + `--dtype=float16` + `--kv-cache-dtype=fp8` + V2=1 + `--stream-interval=4`.
- **Mục đích**: Teammate thử kết hợp stream coalescing (interval 4) và V2=1 để giảm overhead.

## Chỉ số đo được

**Chấm điểm thất bại (0.00 ERS - Container Exit 1)**

### Chi tiết lỗi

- **Thông báo**: `RuntimeError: For FP16/BF16 input, output must have the same dtype as inputs. For FP8 input, output must have dtype BF16`
- **Nơi phát sinh**: `torch.ops._vllm_fa3_C.fwd()` (Flash Attention 3 kernel).
- **Phân tích**:
  - Teammate sử dụng `--dtype=float16` (FP16) cùng với `--kv-cache-dtype=fp8`.
  - Flash Attention 3 (FA3) có ràng buộc cứng: Khi dùng KV Cache dạng FP8, kiểu dữ liệu tính toán (dtype) của model bắt buộc phải là **BF16** (BFloat16).
  - Vì teammate set FP16, FA3 crash ngay lập tức ở bước compile/warmup.

## Kết luận

- **Quy tắc mới**: Mọi config dùng `kv-cache-dtype=fp8` trên Engine v0.26 (có FA3) **BẮT BUỘC** phải đi kèm `--dtype=bfloat16`.
- Tuyệt đối không dùng `--dtype=float16` khi bật FP8 KV Cache.
