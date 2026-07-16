# Viettel AI Race 2026 - Nhật ký thử nghiệm Vòng 2 (Logs Round 2 - LFM2.5)

Bảng ghi nhận điểm số của các đợt chạy thử nghiệm cấu hình tối ưu hóa LLM Inference cho mô hình **LiquidAI/LFM2.5-1.2B-Instruct** (Bài 3).

---

## Kết quả các đợt chạy thử nghiệm (Submissions)

| STT | Mã thử nghiệm / File         | Cấu hình & Tham số chính                                                                                                                                         |  Dự kiến  |   Điểm   | ERC | Passed SLO | TTFT P50 | TTFT P95 | TPOT | Acc Drop | Penalty | Failed/Warm | Ghi chú & Kết luận                                                                                            |
| :-- | :--------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------: | :------: | :-: | :--------: | :------: | :------: | :--: | :------: | :-----: | :---------: | :------------------------------------------------------------------------------------------------------------ |
| 1   | `submissions/16072026/slot1` | Image gốc BTC, `--model=/model`, `--served-model-name=LFM2.5-1.2B-Instruct`, `--max-model-len=32768`, `--gpu-memory-utilization=0.95`, `--enable-prefix-caching` |     -     | **Skip** |  -  |     -      |    -     |    -     |  -   |    -     |    -    |      -      | Quyết định bỏ qua (Skip) để tiết kiệm lượt nộp, áp dụng thẳng tối ưu hóa hệ thống.                            |
| 2   | `submissions/16072026/slot2` | Base Slot 1 + `OMP_NUM_THREADS=4` + `--no-enable-log-requests` + `--disable-log-stats`                                                                           |     -     |    -     |  -  |     -      |    -     |    -     |  -   |    -     |    -    |      -      | Chuẩn bị sẵn cấu hình tối ưu hóa CPU và Logging nhưng bỏ qua để test trực tiếp concurrency giới hạn.          |
| 3   | `submissions/16072026/1333` | Base Slot 2 + `--max-num-seqs=48`                                                                                                                                | **70.0+** | **13.88** | 0.7 |   84/120   |  742ms   | 10271ms  |  58ms  |    0%    |    1    |    0 / 0    | Hệ thống chấm vẫn chạy trace Qwen3.5 cũ (120 reqs, TPOT 58ms), chưa cập nhật sang LFM2.5 và trace mới.         |
| 4   | `submissions/16072026/slot4` | Base Slot 2 + `--max-num-seqs=32`                                                                                                                                | **60.0+** |    -     |  -  |     -      |    -     |    -     |  -   |    -     |    -    |      -      | **Sẵn sàng nộp.** Thu hẹp concurrency hơn để bảo đảm an toàn cho TPOT dưới 10ms nếu Slot 3 bị nghẽn.          |

---

## Lịch sử kỷ lục Vòng 2 (Record Progression - Round 2)

Dưới đây là tiến trình ghi nhận các mốc điểm kỷ lục mới thiết lập trong quá trình tối ưu hóa LFM2.5:

|  Mốc   | STT | Điểm số | Mã / Thư mục nộp | Cấu hình đột phá                  | TTFT P50 | TPOT | Ý nghĩa & Đột phá kỹ thuật |
| :----: | :-: | :-----: | :--------------- | :-------------------------------- | :------: | :--: | :------------------------- |
| **#1** |  -  |    -    | -                | Baseline BTC (Chưa chạy/Dự phòng) |    -     |  -   | Mốc đo lường ban đầu       |
