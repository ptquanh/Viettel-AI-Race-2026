# Kết quả Benchmark - 20:36 08/07/2026 (STT 49 - Custom LMDeploy Hijacked v3 Test)

- **Cấu hình**: Custom image `ptquanh/sandbox-runtime:lmd-bf16-v3` (Base `openmmlab/lmdeploy:v0.7.0-cu12` + Tích hợp model AWQ `/app/qwen_awq` + Python3 hijack bằng Bash script).
- **Cấu hình runtime**: `HIJACK_ENGINE=lmdeploy` + `LMDEPLOY_MODEL=/app/qwen_awq` + `LMDEPLOY_FORMAT=awq` + `LMDEPLOY_QUANT_POLICY=4` + `LMDEPLOY_CACHE_MAX=0.92` + `LMDEPLOY_SESSION_LEN=43008` + `LMDEPLOY_MAX_BATCH_SIZE=64` + `LMDEPLOY_PREFIX_CACHING=1` + `LMDEPLOY_PREFILL_TOKENS=8192`.
- **Mục đích**: Chạy thử nghiệm cấu hình tối ưu hóa tài nguyên khởi động và sửa triệt để lỗi đệ quy shebang.

## Chỉ số đo được

**Chấm điểm thất bại**

```
spawn contestant container: wait for pod ready: timed out waiting for contestant pod to be ready: context deadline exceeded
```
