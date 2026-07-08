# Kết quả Benchmark - 21:50 08/07/2026 (STT 51 - Custom LMDeploy Hijacked v3 Test - Fixed Runner)

- **Cấu hình**: Custom image `ptquanh/sandbox-runtime:lmd-bf16-v3` (Base `openmmlab/lmdeploy:v0.7.0-cu12` + Tích hợp model AWQ `/app/qwen_awq` + Python3 hijack bằng Bash script đã sửa cách gọi CLI).
- **Cấu hình runtime**: `HIJACK_ENGINE=lmdeploy` + `LMDEPLOY_MODEL=/app/qwen_awq` + `LMDEPLOY_FORMAT=awq` + `LMDEPLOY_QUANT_POLICY=4` + `LMDEPLOY_CACHE_MAX=0.92` + `LMDEPLOY_SESSION_LEN=43008` + `LMDEPLOY_MAX_BATCH_SIZE=64` + `LMDEPLOY_PREFIX_CACHING=1` + `LMDEPLOY_PREFILL_TOKENS=8192`.
- **Mục đích**: Kiểm tra image sửa lỗi chạy thực thi `lmdeploy` qua script hijack, hạ session len và max batch size để boot siêu tốc.

## Chỉ số đo được

**Chấm điểm thất bại**

```
spawn contestant container: wait for pod ready: timed out waiting for contestant pod to be ready: context deadline exceeded
```

---

_Kết luận: Thất bại do script python3_hijack cũ bị rơi vào vòng lặp đệ quy vô hạn (khi import lmdeploy, PyTorch/Triton gọi subprocess python3/python3.10 trỏ ngược về hijack script). Bản sửa lỗi triệt để bằng cách dùng system python /usr/bin/python3 và PYTHONPATH vừa được push lên Docker Hub._
