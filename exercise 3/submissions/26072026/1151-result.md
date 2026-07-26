# Kết quả chấm điểm Slot 10 (1151) - THÀNH CÔNG KHỞI ĐỘNG & CHẤM ĐIỂM (52.79đ)

- **Thời gian nộp**: 11:51 AM
- **Chiến lược**: Custom CUDA C++ Kernel Fusion (`v16.3`) + Hạ `GPU_MEMORY_UTILIZATION=0.90`
- **Cấu hình**: Champion Config ngoại trừ `GPU_MEMORY_UTILIZATION=0.90`
- **Điểm số**: **52.7900 điểm** (Thành công hoàn tất 420 requests!)
- **Số request lỗi (Failed count)**: 5

## Chỉ số chi tiết (Benchmark Metrics)

| Chỉ số Metric         |   Giá trị   | Nhận xét                                                        |
| :-------------------- | :---------: | :-------------------------------------------------------------- |
| **Final Score**       | **52.7900** | Chạy mượt mà, không còn lỗi Engine crash!                       |
| **TTFT P50**          |  **67 ms**  | Tăng +9ms so với Champion (58ms) do giảm `GPU_MEM` xuống `0.90` |
| **TTFT P95**          |  **94 ms**  |                                                                 |
| **TBT Median (TPOT)** |  **5 ms**   | Giữ vững mốc 5ms                                                |
| **Accuracy Drop**     |  **0.00**   | Độ chính xác nguyên bản 100%                                    |
| **Failed Requests**   |    **5**    | Tương đương mốc ổn định nhất của hệ thống Grader BTC            |
| **Tokens / sec**      | **0.0575**  |                                                                 |

---

## Phân tích chuyên sâu (Technical Insight)

1. **Bản vá `v16.3` THÀNH CÔNG RỰC RỠ**:
   Engine vLLM V1 đã khởi tạo hoàn hảo, Custom C++ CUDA Kernel được tích hợp hoàn toàn êm ái mà KHÔNG hề xảy ra bất kỳ Segmentation Fault hay Crash container nào!
2. **Nguyên nhân điểm bị tụt xuống 52.79đ**:
   - Khi ta hạ `GPU_MEMORY_UTILIZATION` từ `0.94` xuống `0.90`, vLLM bị cắt bớt **4% dung lượng KV Cache RAM GPU**.
   - Việc thiếu hụt KV Cache này buộc vLLM phải tăng tần suất Re-computation / Queueing làm cho **TTFT P50 bị đẩy từ 58ms lên 67ms (+9ms)** và P95 đẩy lên 94ms. TTFT tăng 9ms trực tiếp phạt điểm của bài thi nặng nề.
3. **Bài học rút ra**:
   - Việc crash ở các bản v16 trước hoàn toàn là do lỗi Undefined Tensor (`None`) mà ta đã vá xong ở `v16.3`.
   - Do đó, ở **Slot 11**, ta hoàn toàn có thể tự tin đẩy `GPU_MEMORY_UTILIZATION` trở lại mốc Champion **`0.94`** trên nền Image `v16.3` để kéo TTFT về lại 58ms (hoặc thấp hơn)!
