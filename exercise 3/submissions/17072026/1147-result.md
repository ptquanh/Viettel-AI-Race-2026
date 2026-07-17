# Kết quả Benchmark - 11:47 17/07/2026 (STT 21 - Slot 6 - Seqs=32 + FP8 Base + OMP=2 + swap=0)

- **Cấu hình**: Image `vllm/vllm-openai:v0.22.1` + `--max-num-seqs=32` + `OMP_NUM_THREADS=2` + `--enable-prefix-caching` + `--quantization=fp8` + `--no-enable-log-requests` + `--disable-log-stats` + `--swap-space=0`.
- **Trạng thái**: **Chấm điểm thất bại (Error)**

## Nguyên nhân lỗi
* Grader log: `api_server.py: error: unrecognized arguments: --swap-space=0`
* Cờ `--swap-space` không được nhận diện bởi vLLM v0.22.1 chạy trên hệ thống của BTC, dẫn đến container `inference` crash lập tức khi start.

## Bài học & Khắc phục
* Loại bỏ hoàn toàn cờ `--swap-space=0` khỏi tất cả các cấu hình chưa nộp (Slot 6, 7, 9, 10, 12).
* Để đảm bảo không phí lượt chạy, Slot 6 được thiết kế cấu hình mới thay thế: `OMP=2 + gpu=0.98` và lưu lại trong file `slot6-docker-compose.yml` để thí sinh nộp lại.
