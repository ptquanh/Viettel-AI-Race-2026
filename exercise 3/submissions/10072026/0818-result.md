# Kết quả Benchmark - 08:18 10/07/2026 (STT 61 - FP8 Weights + FP8 KV Cache Combo)

- **Cấu hình**: Image gốc `vllm/vllm-openai:v0.22.1` + `--quantization=fp8` + `--kv-cache-dtype=fp8` (cấu hình STT 21 + thêm FP8 KV Cache).
- **Mục đích**: Kiểm chứng combo: FP8 model weights + FP8 KV cache. Kỳ vọng giảm KV Cache bandwidth đọc từ VRAM 50% (~31GB→~15GB per decode step), giảm TPOT từ 51ms xuống ~27-30ms.

## Chỉ số đo được

- **Điểm số**: `10.88` (Passed SLO: `73/120`)
- **TTFT P50**: `986 ms`
- **TTFT P95**: `11013 ms`
- **failed_count**: `0`
- **warmup_count**: `0`
- **accuracy_drop**: `1`
- **tbt_median_ms**: `63 ms`

## Phân tích kết quả

Combo FP8 Weights + FP8 KV Cache cho thấy **hiệu năng sụt giảm nghiêm trọng** (từ `18.11` xuống còn `10.88` điểm).

### Đánh giá nguyên nhân sụt giảm:

1.  **Overhead Lượng tử/Giải lượng tử KV Cache:** Ở phiên bản vLLM cũ `v0.22.1`, các kernel phục vụ việc quantize/dequantize KV cache sang FP8 vẫn chưa được tối ưu hóa tốt, sinh ra overhead xử lý trên CPU/GPU lớn hơn nhiều so với lượng băng thông bộ nhớ tiết kiệm được.
2.  **TPOT tăng vọt:** tbt_median tăng từ `51ms` (chỉ lượng tử weights) lên `63ms` (combo weights + KV cache). Điều này xác nhận việc bật thêm FP8 KV cache làm chậm hẳn từng bước decode.
3.  **TTFT tăng nghiêm trọng:** TTFT P50 tăng lên `986ms` và TTFT P95 đạt `11s` (so với `611ms` và `8.3s` của STT 59). Điều này do các prefill chunks phải chịu thêm tải tính toán quy đổi KV cache.

**Kết luận:** Tuyệt đối loại bỏ `--kv-cache-dtype=fp8` khỏi mọi chiến lược phục vụ Qwen3.5 trên phiên bản vLLM v0.22.1 này.
