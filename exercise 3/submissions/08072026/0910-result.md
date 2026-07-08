# Kết quả Benchmark - 09:10 08/07/2026 (STT 46 - Custom LMDeploy Hijacked Test)

- **Cấu hình**: Custom image `ptquanh/viettel-lmdeploy:v1` (Base `openmmlab/lmdeploy:v0.7.0-cu12` + Python3 hijack).
- **Cấu hình runtime**: `HIJACK_ENGINE=lmdeploy` + `LMDEPLOY_CACHE_MAX=0.92` + `LMDEPLOY_SESSION_LEN=65536` + `LMDEPLOY_PREFIX_CACHING=1` + `LMDEPLOY_QUANT_POLICY=0`.
- **Mục đích**: Chạy LMDeploy Turbomind qua mặt cơ chế kiểm soát tĩnh của Grader.

## Chỉ số đo được

TBD

---
