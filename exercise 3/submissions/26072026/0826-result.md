# Kết quả Benchmark - 08:26 26/07/2026 (Slot 04 - Tuning VRAM & Block)

- **Cấu hình**: Image `v14` (Champion) + `VLLM_MAX_MODEL_LEN=4700` + `VLLM_MAX_NUM_SEQS=48` + `VLLM_BLOCK_SIZE=64` + `VLLM_GPU_MEMORY_UTILIZATION=0.96` + `VLLM_CUDAGRAPH_CAPTURE_SIZES=[1,2,4,8,16,32,48]`.
- **Mục đích**: Thay vì tập trung giảm TPOT (đã kẹt cứng ở 4ms), dùng lượng VRAM dư thừa từ việc cắt bớt context dư thừa để nhồi thêm Sequences (48), hy vọng hút trọn burst request và đẩy TTFT xuống đáy.

### Chỉ số chi tiết:

- **Final Score**: **60.41**
- **TPOT (Median)**: 4ms
- **TTFT (P50)**: 54ms
- **TTFT (P95)**: 69ms
- **Failed / Total**: 5 / 420
- **Accuracy Drop**: 0%

### Đánh giá:

1. **TTFT đội ngược (45ms -> 54ms)**: Việc nhồi nhét `SEQS=48` kết hợp `BLOCK=64` không mang lại hiệu năng cao hơn. Ngược lại, nó khiến giai đoạn Prefill phải tính toán một batch khổng lồ, làm "nghẽn" (starve) Scheduler và Decode, đẩy TTFT P50 vọt lên 54ms (so với 45ms của Champion Config).
2. **TPOT không đổi**: Vẫn 4ms. Việc tăng lượng Sequence lên 48 làm lượng dữ liệu KV Cache cần đọc tăng 50%, nhưng vì `1g.18gb` H200 có giới hạn cứng về băng thông bộ nhớ nên TPOT cũng không bị ảnh hưởng quá nặng (ở mức median), tuy nhiên độ ổn định chung đã bị giảm (Failed tăng lên 5).

### Kết luận:

- Cấu hình Champion `SEQS=32` và `BLOCK=32` thực sự là "điểm ngọt" hoàn hảo giữa PagedAttention overhead và GPU memory bandwidth cho LFM2.5 trên instance MiG này.
- **Hủy bỏ hướng Tuning VRAM/Queue.** Chuyển trọng tâm sang tối ưu hóa CPU host với `OMP_NUM_THREADS=3` cho Slot 05.
