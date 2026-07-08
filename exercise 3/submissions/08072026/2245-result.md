# Kết quả Benchmark - 22:45 08/07/2026 (STT 52 - Custom LMDeploy AWQ v3 Test - Loop Broken)

- **Cấu hình**: Custom image `ptquanh/sandbox-runtime:lmd-bf16-v3` (Base `openmmlab/lmdeploy:v0.7.0-cu12` + Tích hợp model AWQ `/app/qwen_awq` + Python3 hijack định tuyến qua `/usr/bin/python3` và `PYTHONPATH`).
- **Cấu hình runtime**: `HIJACK_ENGINE=lmdeploy` + `LMDEPLOY_MODEL=/app/qwen_awq` + `LMDEPLOY_FORMAT=awq` + `LMDEPLOY_QUANT_POLICY=4` + `LMDEPLOY_CACHE_MAX=0.92` + `LMDEPLOY_SESSION_LEN=43008` + `LMDEPLOY_MAX_BATCH_SIZE=64` + `LMDEPLOY_PREFIX_CACHING=1` + `LMDEPLOY_PREFILL_TOKENS=8192`.
- **Mục đích**: Chạy thử nghiệm sau khi bẻ gãy hoàn toàn vòng lặp đệ quy của hijack script.

## Chỉ số đo được

TBD
