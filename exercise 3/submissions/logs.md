# Viettel AI Race 2026 - Nhật ký thử nghiệm (Logs)

Bảng ghi nhận điểm số của các đợt chạy thử nghiệm cấu hình tối ưu hóa LLM Inference (Bài 3).

## Kết quả các đợt chạy thử nghiệm (Submissions)

| STT | Mã thử nghiệm / File        | Mô tả & Tham số chính                                                                           | Điểm số đạt được | Ghi chú                                | Kết luận                                         |
| :-- | :-------------------------- | :---------------------------------------------------------------------------------------------- | :--------------: | :------------------------------------- | :----------------------------------------------- |
| 1   | `submissions/03072026/2052` | Image gốc `vllm/vllm-openai:v0.22.1`, `--max-model-len=262144`, `--gpu-memory-utilization=0.95` |    **15.26**     | Baseline gốc ban đầu của BTC           | Làm mốc so sánh (Baseline)                       |
| 2   | `submissions/04072026/0643` | Custom image `ptquanh/viettel-qwen35-2b:bf16-v1`, tham số tương đương baseline                  |    **15.03**     | Kiểm tra tương thích của custom image  | Có thể dùng custom image                         |
| 3   | `submissions/04072026/0814` | Image gốc BTC, thêm giới hạn xử lý đồng thời `--max-num-seqs=32` để giảm tải CPU                |     **2.64**     | Thử nghiệm phanh luồng xử lý đồng thời | Hiệu năng giảm sâu (không nên giới hạn quá thấp) |

---
