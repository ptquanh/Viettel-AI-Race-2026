# Kết quả Benchmark - 10:26 08/07/2026 (STT 47 - Custom LMDeploy Hijacked v2 Test)

- **Cấu hình**: Custom image `ptquanh/viettel-lmdeploy:v1` (Base `openmmlab/lmdeploy:v0.7.0-cu12` + Python3 hijack bằng Bash script).
- **Cấu hình runtime**: `HIJACK_ENGINE=lmdeploy` + `LMDEPLOY_CACHE_MAX=0.92` + `LMDEPLOY_SESSION_LEN=65536` + `LMDEPLOY_PREFIX_CACHING=1` + `LMDEPLOY_QUANT_POLICY=0` + `LMDEPLOY_PREFILL_TOKENS=8192`.
- **Mục đích**: Chạy LMDeploy Turbomind qua mặt cơ chế kiểm soát tĩnh của Grader.

## Chỉ số đo được

- **Kết quả**: **Thất bại (Chấm điểm thất bại - Startup Timeout)**
- **Lỗi**:
  ```
  spawn contestant container: wait for pod ready: timed out waiting for contestant pod to be ready: context deadline exceeded
  ```

### Nhận xét & Phân tích:

1. **Lỗi định dạng CRLF (Windows line endings) trên Linux:**
   - Script `python3_hijack` được viết trên môi trường Windows chứa các ký tự xuống dòng CRLF (`\r\n`).
   - Khi đưa vào Linux container, các ký tự `\r` (carriage return) ẩn ở cuối các dòng lệnh làm sai lệch shebang `#!/bin/bash\r` (Linux tìm kiếm file interpreter tên `/bin/bash\r` và báo lỗi không thấy), hoặc gây lỗi cú pháp Bash làm container crash liên tục (CrashLoopBackOff).
   - Vì container crash liên tục ngay khi khởi động nên nó không bao giờ mở port 8000. Grader chờ 5-10 phút và kết luận quá thời hạn chờ pod ready.
2. **Lỗi đường dẫn thực thi (PATH):**
   - Lệnh gọi `lmdeploy` trong script chưa sử dụng đường dẫn tuyệt đối, có thể gây lỗi `command not found` trong môi trường non-interactive shell của Kubernetes pod.
3. **Giải pháp khắc phục (v3):**
   - Thêm lệnh `sed -i 's/\r$//' /opt/py3/bin/python3` vào `Dockerfile.lmdeploy` để tự động dọn dẹp toàn bộ ký tự CRLF thừa khi đóng gói.
   - Sử dụng đường dẫn tuyệt đối cho LMDeploy (`/opt/conda/bin/lmdeploy`) để bảo đảm gọi chính xác trong môi trường của grader.

---
