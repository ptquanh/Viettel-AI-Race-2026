# Viettel AI Race 2026 - Nhật ký thử nghiệm Vòng 2 (Logs Round 2 - LFM2.5)

Bảng ghi nhận điểm số của các đợt chạy thử nghiệm cấu hình tối ưu hóa LLM Inference cho mô hình **LiquidAI/LFM2.5-1.2B-Instruct** (Bài 3).

---

## Kết quả các đợt chạy thử nghiệm (Submissions)

| STT | Mã thử nghiệm / File        | Cấu hình & Tham số chính          |  Dự kiến  |     Điểm     | ERC | Passed SLO | TTFT P50 | TTFT P95 | TPOT | Acc Drop | Penalty | Failed/Warm | Ghi chú & Kết luận                                                                                                              |
| :-- | :-------------------------- | :-------------------------------- | :-------: | :----------: | :-: | :--------: | :------: | :------: | :--: | :------: | :-----: | :---------: | :------------------------------------------------------------------------------------------------------------------------------ |
| 1   | `submissions/16072026/1333` | Baseline BTC + OMP=4 + Seqs=48    | **70.0+** |  **42.91**   |  -  |     -      |  103ms   |  151ms   | 5ms  |    0%    |    1    |   0 / 90    | Kết quả LFM2.5 đầu tiên. TTFT P95 cực tốt (151ms) nhờ Prefix Caching, TPOT Median = 5ms. Cần giảm Seqs để tối ưu TPOT.          |
| 2   | `submissions/16072026/1645` | Baseline BTC + OMP=4 + Seqs=32    | **60.0+** |  **43.08**   |  -  |     -      |  103ms   |  158ms   | 5ms  |    0%    |    1    |   0 / 90    | Điểm số tăng nhẹ lên 43.08 nhưng TPOT vẫn kẹt ở 5ms. Trễ TTFT P95 tăng nhẹ lên 158ms do hàng đợi bị hẹp lại.                    |
| 3   | `submissions/16072026/1724` | Baseline BTC + OMP=4 + Seqs=24    | **65.0+** |  **42.46**   |  -  |     -      |  102ms   |  153ms   | 5ms  |    0%    |    1    |   0 / 90    | Điểm số giảm xuống 42.46. TTFT có cải thiện nhẹ nhưng TPOT Median vẫn kẹt cứng ở 5ms. Hàng đợi bị ứ đọng khi Poisson burst.     |
| 4   | `submissions/16072026/1819` | Baseline BTC + OMP=4 + Seqs=16    | **60.0+** |  **43.31**   |  -  |     -      |  101ms   |  146ms   | 5ms  |    0%    |    1    |   0 / 90    | Kỷ lục mới 43.31 điểm. TPOT Median vẫn ở 5ms nhưng TTFT P50 (101ms) và P95 (146ms) được tối ưu hóa tốt nhất do giảm tranh chấp. |
| 5   | `submissions/16072026/2118` | Seqs=32 + Chunk=2048 (Slot 7)     | **65.0+** |  **44.63**   |  -  |     -      |   96ms   |  139ms   | 5ms  |    0%    |    1    |   0 / 90    | Kỷ lục mới 44.63 điểm. Bật Chunked Prefill giúp TTFT giảm rất mạnh (P50 96ms, P95 139ms). TPOT vẫn giữ 5ms.                     |
| 6   | `submissions/16072026/2050` | Seqs=32 + Chunk=ON (Slot 5)       | **60.0+** |  **43.69**   |  -  |     -      |   98ms   |  143ms   | 5ms  |    0%    |    1    |   0 / 90    | Chunked Prefill mặc định giúp TTFT P50/P95 giảm tốt. TPOT vẫn kẹt ở 5ms.                                                        |
| 7   | `submissions/16072026/2105` | Seqs=32 + Chunk=1024 (Slot 6)     | **60.0+** |  **43.62**   |  -  |     -      |  100ms   |  151ms   | 5ms  |    0%    |    1    |   0 / 90    | Chunk 1024 quá nhỏ làm tăng overhead lập lịch nhẹ, TTFT P95 tăng lên 151ms so với chunk mặc định.                               |
| 8   | `submissions/16072026/2133` | Seqs=32 + Chunk=4096 (Slot 8)     | **65.0+** |  **45.08**   |  -  |     -      |   91ms   |  142ms   | 5ms  |    0%    |    1    |   0 / 90    | Kỷ lục mới 45.08 điểm. Chunk 4096 là sweet-spot cho context length, TTFT P50 giảm sâu còn 91ms.                                 |
| 9   | `submissions/16072026/2145` | Seqs=32 + Chunk=8192 (Slot 9)     | **65.0+** |  **44.68**   |  -  |     -      |   90ms   |  144ms   | 5ms  |    0%    |    1    |   0 / 90    | Chunk 8192 cho TTFT P50 thấp nhất (90ms) nhưng ERS trung bình thấp hơn mốc 4096 một chút.                                       |
| 10  | `submissions/16072026/2146` | Seqs=32 + OMP=2 (Slot 10)         | **65.0+** |  **44.54**   |  -  |     -      |   95ms   |  144ms   | 5ms  |    0%    |    1    |   0 / 90    | OMP=2 giảm context switching của OpenMP trên CPU 3 cores, tăng đáng kể điểm số lên 44.54 mà không cần chunked prefill.          |
| 11  | `submissions/16072026/2147` | Seqs=32 + OMP=3 (Slot 11)         | **60.0+** |  **43.96**   |  -  |     -      |   96ms   |  145ms   | 5ms  |    0%    |    1    |   0 / 90    | OMP=3 khớp cores vật lý, tốt hơn baseline OMP=4 nhưng không tối ưu bằng OMP=2 (do cần chừa CPU cho IO/scheduler).               |
| 12  | `submissions/16072026/2158` | Seqs=32 + OMP=5 (Slot 12)         | **60.0+** |  **43.53**   |  -  |     -      |   96ms   |  156ms   | 5ms  |    0%    |    1    |   0 / 90    | OMP=5 gây nghẽn CPU do hyperthreading quá mức, TTFT P95 tăng vọt lên 156ms.                                                     |
| 13  | `submissions/16072026/2159` | Seqs=32 + MaxLen=16K (Slot 13)    | **60.0+** |  **43.03**   |  -  |     -      |   99ms   |  155ms   | 5ms  |    0%    |    1    |   0 / 90    | Giảm max-model-len xuống 16K chưa đủ tác động sâu sắc đến block allocator của vLLM scheduler.                                   |
| 14  | `submissions/16072026/2209` | Seqs=32 + MaxLen=8K (Slot 14)     | **60.0+** |  **43.62**   |  -  |     -      |   97ms   |  151ms   | 5ms  |    0%    |    1    |   0 / 90    | MaxLen=8K thu gọn KV Cache manager, giúp TTFT P50 giảm nhẹ về 97ms, điểm ERS đạt 43.62.                                         |
| 15  | `submissions/16072026/2210` | Seqs=32 + Quant FP8 (Slot 15)     | **85.0+** |  **55.04**   |  -  |     -      |   79ms   |  115ms   | 4ms  |    0%    |    1    |   0 / 90    | ĐỘT PHÁ KỶ LỤC 55.04. FP8 online giúp TPOT phá mốc 5ms xuống 4ms, TTFT P50/P95 giảm cực sâu còn 79ms/115ms.                     |
| 16  | `submissions/17072026/0844` | FP8 Base + OMP=2 (Slot 1)         | **56.00** |  **56.07**   |  -  |     -      |   78ms   |  107ms   | 4ms  |    0%    |    1    |   0 / 90    | Xác nhận OMP=2 tăng hiệu quả trên FP8. TTFT P95 cải thiện rõ rệt xuống 107ms.                                                   |
| 17  | `submissions/17072026/0845` | FP8 Base + Chunk=4096 (Slot 2)    | **56.50** |  **56.53**   |  -  |     -      |   74ms   |  106ms   | 4ms  |    0%    |    1    |   0 / 90    | KỶ LỤC MỚI 56.53. Chunked Prefill cực tốt trên FP8, kéo TTFT P50/P95 xuống 74ms/106ms.                                          |
| 18  | `submissions/17072026/1009` | FP8 Base + Seqs=16 (Slot 3)       | **55.00** |  **54.43**   |  -  |     -      |   81ms   |  124ms   | 4ms  |    0%    |    1    |   0 / 90    | Giới hạn Seqs=16 trên FP8 làm tăng trễ hàng đợi scheduler, khiến TTFT P95 tăng lên 124ms và điểm ERS sụt giảm.                  |
| 19  | `submissions/17072026/1012` | FP8 + OMP=2 + Chunk=4096 (Slot 4) | **56.50** |  **56.79**   |  -  |     -      |   73ms   |   93ms   | 4ms  |    0%    |    1    |   0 / 90    | KỶ LỤC MỚI 56.79. Kết hợp OMP=2 và Chunk=4096 cộng hưởng hoàn hảo, TTFT P95 lần đầu tiên giảm sâu xuống dưới 100ms (93ms).      |
| 20  | `submissions/17072026/1107` | FP8 + OMP=2 + MaxLen=8K (Slot 5)  | **55.50** |  **54.16**   |  -  |     -      |   83ms   |  124ms   | 4ms  |    0%    |    1    |   0 / 90    | Giới hạn MaxLen=8K trên nền FP8 gây tác dụng ngược làm tăng trễ TTFT P95 lên 124ms và giảm điểm ERS.                            |
| 21  | `submissions/17072026/1147` | FP8 + OMP=2 + swap=0 (Slot 6)     |   **-**   | **Thất bại** |  -  |     -      |    -     |    -     |  -   |    -     |    -    |      -      | Chấm điểm thất bại do vLLM v0.22.1 của BTC không nhận diện cờ `--swap-space`.                                                   |

---

## Lịch sử kỷ lục Vòng 2 (Record Progression - Round 2)

Dưới đây là tiến trình ghi nhận các mốc điểm kỷ lục mới thiết lập trong quá trình tối ưu hóa LFM2.5:

|  Mốc   |  STT   |  Điểm số  | Mã / Thư mục nộp            | Cấu hình đột phá               | TTFT P50 | TPOT | Ý nghĩa & Đột phá kỹ thuật                                                    |
| :----: | :----: | :-------: | :-------------------------- | :----------------------------- | :------: | :--: | :---------------------------------------------------------------------------- |
| **#1** | **1**  | **42.91** | `submissions/16072026/1333` | Baseline BTC + OMP=4 + Seqs=48 |  103ms   | 5ms  | Điểm số mốc ban đầu của LFM2.5 để đánh giá các cải tiến.                      |
| **#2** | **2**  | **43.08** | `submissions/16072026/1645` | Baseline BTC + OMP=4 + Seqs=32 |  103ms   | 5ms  | Tăng nhẹ điểm số nhờ phân phối TPOT tối ưu hơn dù Median giữ nguyên.          |
| **#3** | **4**  | **43.31** | `submissions/16072026/1819` | Baseline BTC + OMP=4 + Seqs=16 |  101ms   | 5ms  | Kỷ lục mới nhờ TTFT được tối ưu sâu (P95 146ms) khi chạy ở Seqs=16.           |
| **#4** | **5**  | **44.63** | `submissions/16072026/2118` | Seqs=32 + Chunk=2048           |   96ms   | 5ms  | Chunked Prefill giúp triệt tiêu prefill interference, hạ TTFT P95 còn 139ms.  |
| **#5** | **8**  | **45.08** | `submissions/16072026/2133` | Seqs=32 + Chunk=4096           |   91ms   | 5ms  | Sweet-spot chunk size 4096 tối ưu hóa số lượng chunk prefill trên hàng đợi.   |
| **#6** | **15** | **55.04** | `submissions/16072026/2210` | Seqs=32 + FP8 Quantization     |   79ms   | 4ms  | Bẻ gãy mốc TPOT 5ms xuống 4ms, TTFT P95 xuống 115ms nhờ lượng tử hóa FP8.     |
| **#7** | **16** | **56.07** | `submissions/17072026/0844` | FP8 Base + OMP=2               |   78ms   | 4ms  | Kỷ lục mới 56.07 nhờ giảm context switching của OpenMP trên nền FP8.          |
| **#8** | **17** | **56.53** | `submissions/17072026/0845` | FP8 + Chunk=4096               |   74ms   | 4ms  | Kỷ lục mới 56.53 nhờ Chunked prefill 4096 giảm thiểu nghẽn prefill trên FP8.  |
| **#9** | **19** | **56.79** | `submissions/17072026/1012` | FP8 + OMP=2 + Chunk=4096       |   73ms   | 4ms  | Kỷ lục mới 56.79. Cộng hưởng OMP=2 và Chunk=4096 giúp TTFT P95 phá mốc 100ms. |
