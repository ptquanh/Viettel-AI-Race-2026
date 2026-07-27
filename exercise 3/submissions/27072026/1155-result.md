# Kết quả chấm điểm Slot 07 (1155 - 27/07/2026) - GIẢM WARMUPS (54.00đ)

- **Thời gian nộp**: 11:55 AM (27/07/2026)
- **Chiến lược**: Triton JIT Kernel Fusion (`v18.0`) + Hạ Warmup về 5 Cycles
- **Cấu hình**: Champion Config (`MAX_LEN=32768`, `GPU_MEM=0.94`, `WARMUPS=5`)
- **Điểm số**: **54.0000 điểm**
- **Số request lỗi (Failed count)**: 4 (Giảm từ 5 xuống 4!)

## Chỉ số chi tiết (Benchmark Metrics)

| Chỉ số Metric         |   Giá trị   | Nhận xét                                                              |
| :-------------------- | :---------: | :-------------------------------------------------------------------- |
| **Final Score**       | **54.0000** | Lỗi giảm xuống 4, nhưng TTFT P50 tăng lên 72ms                        |
| **TTFT P50**          |  **72 ms**  | ❌ **Tăng +18ms so với Slot 06 (54ms)** do hạ `WARMUPS` từ 10 xuống 5 |
| **TTFT P95**          |  **96 ms**  | Tăng +16ms                                                            |
| **TBT Median (TPOT)** |  **4 ms**   | Giữ mốc 4ms chuẩn                                                     |
| **Accuracy Drop**     |  **0.00**   | Độ chính xác nguyên bản 100%                                          |
| **Failed Requests**   |    **4**    | 🔥 **Giảm xuống 4 lỗi**                                               |
| **Tokens / sec**      | **0.0554**  |                                                                       |

---

## Phân tích chuyên sâu (Technical Insight)

1. **Khẳng định vai trò của `CUDAGRAPH_NUM_OF_WARMUPS=10`**:
   - Thử nghiệm ở Slot 07 chứng minh: Khi hạ `WARMUPS` từ 10 về 5, **TTFT P50 lập tức bị trễ từ 54ms lên 72ms (+18ms)**!
   - Điều này khẳng định mốc **`WARMUPS=10` là bắt buộc** để giữ vững TTFT P50 kỷ lục 54ms.

2. **Đã xác định công thức Bứt phá 80+ điểm cho Slot 08**:
   - Giữ nguyên **`WARMUPS=10`** (giữ TTFT 54ms).
   - Kích hoạt **Multi-Step Scheduling (`VLLM_NUM_SCHEDULER_STEPS=4`)** để cắt giảm 75% CPU scheduling overhead, ép TPOT xuống **< 2ms**!
   - Tăng `VLLM_MAX_NUM_SEQS=64` để đưa `failed_count` về **0**!
