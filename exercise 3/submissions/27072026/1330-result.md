# Kết quả chấm điểm Slot 09 (1330 - 27/07/2026) - KẾT QUẢ KHỞI ĐỘNG VÂN HÀNH THÀNH CÔNG V18.1 (56.68đ)

- **Thời gian nộp**: 01:30 PM (27/07/2026)
- **Chiến lược**: Multi-Step Scheduling Injector (`v18.1`) + `MAX_NUM_SEQS=64`
- **Cấu hình**: Image `v18.1` + `NUM_SCHEDULER_STEPS=4` + `MAX_NUM_SEQS=64` + `WARMUPS=10`
- **Điểm số**: **56.6800 điểm** (Khởi động mượt mà 100%, 0% Accuracy Drop!)
- **Số request lỗi (Failed count)**: 4 (Duy trì mốc thấp 4 lỗi!)

## Chỉ số chi tiết (Benchmark Metrics)

| Chỉ số Metric         |   Giá trị   | Nhận xét                                                                                |
| :-------------------- | :---------: | :-------------------------------------------------------------------------------------- |
| **Final Score**       | **56.6800** | Container chạy hoàn hảo, khắc phục 100% lỗi CLI ArgParse!                               |
| **TTFT P50**          |  **62 ms**  | ❌ Tăng +8ms so với Slot 06 (54ms) do `MAX_NUM_SEQS=64` làm phình CUDA Graph batch size |
| **TTFT P95**          |  **89 ms**  |                                                                                         |
| **TBT Median (TPOT)** |  **4 ms**   | Giữ vững mốc 4ms                                                                        |
| **Accuracy Drop**     |  **0.00**   | Độ chính xác nguyên bản 100%                                                            |
| **Failed Requests**   |    **4**    | 🔥 **Giữ vững 4 lỗi**                                                                   |
| **Tokens / sec**      | **0.0553**  |                                                                                         |

---

## Phân tích chuyên sâu & Phát hiện tối ưu (Technical Insights)

1. **Thành công rực rỡ của Bản vá `v18.1`**:
   - Phương pháp inject `num_scheduler_steps` trực tiếp qua Dataclass `EngineArgs` trong `sitecustomize.py` đã hoạt động **hoàn hảo 100%**, hoàn toàn giải quyết lỗi sập container do CLI ArgParse.

2. **Nguyên nhân TTFT P50 bị tăng từ 54ms lên 62ms**:
   - Khi tăng `VLLM_MAX_NUM_SEQS` từ **32 lên 64**, vLLM phải mở rộng các khối CUDA Graph Memory Bucketing. Việc này làm tăng overhead phân bổ VRAM trong giai đoạn Prefill, khiến TTFT P50 bị trễ từ 54ms lên 62ms (+8ms).
   - **Bài học rút ra**: Mốc **`VLLM_MAX_NUM_SEQS=32` chính là điểm cân bằng vàng (Golden Sweet-spot)** giúp đạt TTFT P50 kỷ lục 54ms!

3. **Hướng đi tối ưu hóa cho Slot 10**:
   - Đưa `VLLM_MAX_NUM_SEQS` trở lại **`32`** (lấy lại TTFT P50 = 54ms).
   - Tăng `VLLM_GPU_MEMORY_UTILIZATION` lên **`0.95`** (mốc VRAM Champion) để tăng thêm KV Cache RAM GPU, giảm thiểu tối đa cache eviction dưới tải nặng.
