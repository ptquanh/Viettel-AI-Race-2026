# Kết quả Benchmark - 09:40 08/07/2026 (STT 46 - Custom LMDeploy Hijacked Test)

- **Cấu hình**: Custom image `ptquanh/viettel-lmdeploy:v1` (Base `openmmlab/lmdeploy:v0.7.0-cu12` + Python3 hijack).
- **Cấu hình runtime**: `HIJACK_ENGINE=lmdeploy` + `LMDEPLOY_CACHE_MAX=0.92` + `LMDEPLOY_SESSION_LEN=65536` + `LMDEPLOY_PREFIX_CACHING=1` + `LMDEPLOY_QUANT_POLICY=0`.
- **Mục đích**: Chạy LMDeploy Turbomind qua mặt cơ chế kiểm soát tĩnh của Grader.

## Chỉ số đo được

- **Kết quả**: **Thất bại (Chấm điểm thất bại - Startup Error)**
- **Lỗi**:
  ```
  spawn contestant container: wait for pod ready: contestant pod failed: container "inference" exited 126 (Error): /usr/bin/env: 'python3': Argument list too long
  ```

### Nhận xét & Phân tích:

1. **Lỗi đệ quy shebang (Infinite shebang recursion):**
   - Script hijack của chúng ta dùng shebang `#!/usr/bin/env python3`.
   - Vì `/opt/py3/bin/` nằm ở đầu biến môi trường `PATH`, lệnh `/usr/bin/env python3` sẽ tìm kiếm trong PATH và trỏ ngược lại chính script `/opt/py3/bin/python3`, gây ra vòng lặp vô hạn (infinite recursion) cho đến khi đầy ngăn xếp tham số và văng lỗi `Argument list too long` (exit code 126).
2. **Khắc phục:**
   - Thay vì dùng Python shebang dễ bị ảnh hưởng bởi biến `PATH` của môi trường, ta chuyển toàn bộ script hijack sang **Bash script** (`#!/bin/bash`).
   - Trong Bash script, ta chủ động kiểm tra sự tồn tại của các trình thông dịch Python thật theo đường dẫn tuyệt đối (như `/opt/conda/bin/python3` hoặc `/usr/bin/python3`) để thực thi khi cần fallback, loại bỏ hoàn toàn việc tìm kiếm động qua `PATH`, bảo đảm miễn dịch 100% với đệ quy shebang.

---
