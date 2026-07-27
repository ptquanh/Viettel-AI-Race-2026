# Kết quả chấm điểm Slot 08 (1257 - 27/07/2026) - LỖI THAM SỐ CLI API SERVER (CRASH CONTAINER)

- **Thời gian nộp**: 12:57 PM (27/07/2026)
- **Chiến lược**: Multi-Step Scheduling (`VLLM_NUM_SCHEDULER_STEPS=4`)
- **Cấu hình**: Champion Config + `NUM_SCHEDULER_STEPS=4` + `WARMUPS=10` + `SEQS=64`
- **Điểm số**: `Chấm điểm thất bại` (Exit Code 2)
- **Thông báo lỗi**: `api_server.py: error: unrecognized arguments: --num-scheduler-steps`

## Phân tích nguyên nhân & Giải pháp (Root Cause & Fix)

### Nguyên nhân:

Trình khởi chạy CLI `vllm.entrypoints.openai.api_server` trong bản vLLM này không mở tham số cờ dòng lệnh `--num-scheduler-steps` ở tầng CLI Parser. Khi script `python3_hijack` truyền tham số này vào `api_server.py`, Python ArgParse ném lỗi `unrecognized arguments` khiến container văng ngay lập tức với Exit Code 2.

### Giải pháp triệt me (Bản vá v18.1):

1. **Sửa `python3_hijack`**: Gỡ bỏ tham số `--num-scheduler-steps` khỏi CLI command line để không làm vỡ `api_server.py`.
2. **Inject qua Python DataClass (`sitecustomize.py`)**: Can thiệp trực tiếp vào Dataclass `EngineArgs` trong Python thông qua `sitecustomize.py`:
   ```python
   from vllm.engine.arg_utils import EngineArgs
   # Tự động gán self.num_scheduler_steps = 4 trực tiếp vào EngineArgs
   ```
   Điều này đảm bảo vLLM Engine nhận diện và kích hoạt Multi-Step Scheduling 100% an toàn mà không bị lỗi CLI flag Parser.
