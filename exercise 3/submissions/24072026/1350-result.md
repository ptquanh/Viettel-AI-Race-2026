# Kết Quả Thử Nghiệm 1350 (Slot 06 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1350`
- **File Compose**: `1350-docker-compose.yml` (Slot 06)
- **Thời gian chấm**: 24/07/2026 (13:50)
- **Thay đổi**: Best v14 FP8 + `VLLM_WORKER_MULTIPROC_METHOD=spawn`

## Kết Quả Chấm Điểm

- **Điểm số**: `61.5900` (🔥 KỶ LỤC MỚI TOÀN GIẢI! +0.35đ so với kỷ lục cũ 61.24đ!)
- **TTFT P50**: 47ms (Giảm 4ms từ 51ms!)
- **TTFT P95**: 68ms (Giảm 2ms từ 70ms! - Cân bằng kỷ lục P95 thấp nhất!)
- **TPOT (TBT Median)**: 4ms
- **Số request lỗi (Failed count)**: 5
- **Penalty**: 1
- **Accuracy Drop**: 0%

## Phân Tích & Kết Luận

- **Hiệu quả của Multiprocessing Spawn Method**: Thêm `VLLM_WORKER_MULTIPROC_METHOD=spawn` giúp vLLM worker process được khởi tạo với context hoàn toàn sạch, tránh được rủi ro copy-on-write memory fragmentation và lock contention kế thừa từ parent process khi dùng `fork`.
- Nhờ đó, TTFT P50 giảm sâu xuống **47ms** và TTFT P95 giảm xuống kịch sàn **68ms**, đưa tổng điểm đạt **61.59đ** (Kỷ lục điểm số cao nhất toàn giải!).
- **Kết luận**: Khóa cờ `VLLM_WORKER_MULTIPROC_METHOD=spawn` làm chuẩn cố định cho các thử nghiệm tiếp theo.
