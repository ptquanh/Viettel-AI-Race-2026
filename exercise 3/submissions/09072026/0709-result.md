# Kết quả Benchmark - 07:09 09/07/2026 (STT 53 - Custom LMDeploy AWQ v4 Test - System Python loop failure)

- **Cấu hình**: Custom image `ptquanh/sandbox-runtime:lmd-bf16-v3` (Base `openmmlab/lmdeploy:v0.7.0-cu12` + Tích hợp model AWQ `/app/qwen_awq` + Python3 hijack định tuyến qua `/usr/bin/python3` và `PYTHONPATH`).
- **Cấu hình runtime**: `HIJACK_ENGINE=lmdeploy` + `LMDEPLOY_MODEL=/app/qwen_awq` + `LMDEPLOY_FORMAT=awq` + `LMDEPLOY_QUANT_POLICY=4` + `LMDEPLOY_CACHE_MAX=0.92` + `LMDEPLOY_SESSION_LEN=43008` + `LMDEPLOY_MAX_BATCH_SIZE=64` + `LMDEPLOY_PREFIX_CACHING=1` + `LMDEPLOY_PREFILL_TOKENS=8192`.

## Chỉ số đo được

**Chấm điểm thất bại**

```
spawn contestant container: wait for pod ready: contestant pod failed: container "inference" exited 126 (Error): [Antigravity Hijack] Intercepted BTC's vLLM call! Waking up Engine...
[Antigravity Hijack] Selected engine: lmdeploy
[Antigravity Hijack] Executing LMDeploy: /usr/bin/python3 /opt/py3/bin/lmdeploy serve api_server /app/qwen_awq --server-name 0.0.0.0 --server-port 8000 --model-name Qwen3.5-2B --backend turbomind --model-format awq --cache-max-entry-count 0.92 --session-len 43008 --max-prefill-token-num 8192 --max-batch-size 64 --enable-prefix-caching --quant-policy 4
/usr/bin/python3: line 89: /usr/bin/python3: Argument list too long
/usr/bin/python3: line 89: /usr/bin/python3: Success

--- last container logs ---
[Antigravity Hijack] Intercepted BTC's vLLM call! Waking up Engine...
[Antigravity Hijack] Selected engine: lmdeploy
[Antigravity Hijack] Executing LMDeploy: /usr/bin/python3 /opt/py3/bin/lmdeploy serve api_server /app/qwen_awq --server-name 0.0.0.0 --server-port 8000 --model-name Qwen3.5-2B --backend turbomind --model-format awq --cache-max-entry-count 0.92 --session-len 43008 --max-prefill-token-num 8192 --max-batch-size 64 --enable-prefix-caching --quant-policy 4
/usr/bin/python3: line 89: /usr/bin/python3: Argument list too long
/usr/bin/python3: line 89: /usr/bin/python3: Success
```

---

_Kết luận: /usr/bin/python3 thực chất là một symlink trỏ tới /opt/py3/bin/python3 (qua trung gian python3.10), nghĩa là lệnh gọi system python vẫn quay ngược về script hijack, tạo thành vòng lặp đệ quy. Trong mỗi vòng lặp, biến PYTHONPATH được append liên tục làm tràn giới hạn bộ nhớ đối số (Argument list too long - Error 126)._
