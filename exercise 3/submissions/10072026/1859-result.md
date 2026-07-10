# Kết quả Benchmark - 18:59 10/07/2026 (STT 70 - INT4 KV Cache per-token-head - Đổi tên từ 1700)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v4` + `--kv-cache-dtype int4_per_token_head` + `--quantization fp8`
- **Mục đích**: Test INT4 KV cache quantization built-in vLLM v0.22.1.

## Chỉ số đo được

**Chấm điểm thất bại**

### Trace lỗi thu được:

```
spawn contestant container: wait for pod ready: contestant pod failed: container "inference" exited 2 (Error): n}]
...
api_server.py: error: argument --kv-cache-dtype: invalid choice: 'int4_per_token_head' (choose from auto, bfloat16, float16, fp8, fp8_ds_mla, fp8_e4m3, fp8_e5m2, fp8_inc, fp8_per_token_head, int8_per_token_head, nvfp4, turboquant_3bit_nc, turboquant_4bit_nc, turboquant_k3v4_nc, turboquant_k8v4)
```

## Nhận xét & Phát hiện vô giá

1. Cờ `int4_per_token_head` **không được hỗ trợ** trên phiên bản vLLM này của portal BTC.
2. Tuy nhiên, parser của vLLM trên portal đã chỉ ra các cờ thay thế cực kỳ giá trị:
   - **`turboquant_4bit_nc`** (4-bit MSE Keys + 4-bit Values + Norm Correction) 🔥
   - **`turboquant_k8v4`** (FP8 Keys + 4-bit Values) 🔥
   - **`turboquant_k3v4_nc`** (3-bit MSE Keys + 4-bit Values + NC)
   - **`turboquant_3bit_nc`** (3-bit MSE Keys + 3-bit Values + NC)
   - **`int8_per_token_head`** (Chúng ta đã nộp ở STT 71)
   - **`fp8_per_token_head`** (Chúng ta đã nộp ở STT 72)
3. **Ý nghĩa:** `turboquant_4bit_nc` chính là cờ nén **INT4 KV Cache** thực tế của hệ thống BTC! Nó mang lại hiệu quả nén ~3.8x (gần như tương đương 4x của INT4 thông thường) và tích hợp sẵn Norm Correction để bảo toàn độ chính xác (perplexity/accuracy).
4. **Hành động:** Chuyển hướng test ngay cờ `turboquant_4bit_nc` và `turboquant_k8v4` trong các slot của ngày mai (11/07) thay thế cho cờ `int4_per_token_head` bị lỗi.
