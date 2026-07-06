# Kết quả Benchmark - 14:35 06/07/2026 (Slot 5 - Multi-step Scheduling Test)

- **Cấu hình**: Baseline mới (STT19: `--enable-chunked-prefill` + `--no-enable-log-requests`) + `--num-scheduler-steps=8` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Tối ưu hóa TPOT (TBT) bằng cách cho phép scheduler lập lịch trước 8 bước cùng lúc, giảm CPU overhead trong quá trình decode.

## Chỉ số đo được

**Chấm điểm thất bại**

- Container "inference" exited 2 (Error)
- Log lỗi: `api_server.py: error: unrecognized arguments: --num-scheduler-steps=8`

### Nhận xét & Phân tích:

1. **Flag không được hỗ trợ:** Mặc dù phiên bản vLLM này rất mới (có các tham số mới như `--performance-mode`, `deep_gemm`), nhưng flag `--num-scheduler-steps` vẫn không khả dụng trên build này của BTC.
2. **Cấu hình cấm bổ sung:** Đưa `--num-scheduler-steps` vào danh mục cấm/tránh sử dụng trực tiếp để tránh crash.
3. **Kết luận ngày 06/07:** Chúng ta đã chạy đủ 5 lượt submit trong ngày. Kết quả tối ưu nhất ngày hôm nay thuộc về **STT19 (Slot 4 - 13:59)** với điểm số **15.97** (Baseline + `--enable-chunked-prefill` + `--no-enable-log-requests`).

---
