# Viettel AI Race 2026 - Nhật ký thử nghiệm Vòng 2 (Logs Round 2 - LFM2.5)

Bảng ghi nhận điểm số của các đợt chạy thử nghiệm cấu hình tối ưu hóa LLM Inference cho mô hình **LiquidAI/LFM2.5-1.2B-Instruct** (Bài 3).

---

## Kết quả các đợt chạy thử nghiệm (Submissions)

| STT | Mã thử nghiệm / File        | Cấu hình & Tham số chính       |  Dự kiến  |   Điểm    | ERC | Passed SLO | TTFT P50 | TTFT P95 | TPOT | Acc Drop | Penalty | Failed/Warm | Ghi chú & Kết luận                                                                                                     |
| :-- | :-------------------------- | :----------------------------- | :-------: | :-------: | :-: | :--------: | :------: | :------: | :--: | :------: | :-----: | :---------: | :--------------------------------------------------------------------------------------------------------------------- |
| 1   | `submissions/16072026/1333` | Baseline BTC + OMP=4 + Seqs=48 | **70.0+** | **42.91** |  -  |     -      |  103ms   |  151ms   | 5ms  |    0%    |    1    |   0 / 90    | Kết quả LFM2.5 đầu tiên. TTFT P95 cực tốt (151ms) nhờ Prefix Caching, TPOT Median = 5ms. Cần giảm Seqs để tối ưu TPOT. |
| 2   | `submissions/16072026/1645` | Baseline BTC + OMP=4 + Seqs=32 | **60.0+** |     -     |  -  |     -      |    -     |    -     |  -   |    -     |    -    |      -      | **Sẵn sàng nộp.** Thu hẹp concurrency hơn để giảm CPU scheduling overhead cho TPOT.                                    |

---

## Lịch sử kỷ lục Vòng 2 (Record Progression - Round 2)

Dưới đây là tiến trình ghi nhận các mốc điểm kỷ lục mới thiết lập trong quá trình tối ưu hóa LFM2.5:

|  Mốc   |  STT  |  Điểm số  | Mã / Thư mục nộp            | Cấu hình đột phá               | TTFT P50 | TPOT | Ý nghĩa & Đột phá kỹ thuật                               |
| :----: | :---: | :-------: | :-------------------------- | :----------------------------- | :------: | :--: | :------------------------------------------------------- |
| **#1** | **1** | **42.91** | `submissions/16072026/1333` | Baseline BTC + OMP=4 + Seqs=48 |  103ms   | 5ms  | Điểm số mốc ban đầu của LFM2.5 để đánh giá các cải tiến. |
