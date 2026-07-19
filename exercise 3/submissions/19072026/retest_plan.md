# KẾ HOẠCH TỔNG THỂ KHẮC PHỤC & RE-TEST TOÀN BỘ CÁC THỬ NGHIỆM (19/07 - 20/07)

> **Bối cảnh**: Trong phiên bản Custom Image `v1` (`vllm-lfm25-fp8-kernels-v1`), script `python3_hijack` đã vô tình hardcode `--max-model-len 32768` và `--quantization fp8`, dẫn đến việc các thử nghiệm cũ về Lượng tử hóa INT4 (Marlin, Compressed-tensors), Giảm Max Len (16K, 8K) và N-gram Speculative Decoding bị bỏ qua và đều thực thi dưới dạng FP8 Native.
> 
> Với việc hoàn thành **Custom Image `v2`** (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`), toàn bộ các biến môi trường (`VLLM_MAX_MODEL_LEN`, `VLLM_QUANTIZATION`, `VLLM_SPECULATIVE_MODEL`, `VLLM_NUM_SPECULATIVE_TOKENS`) và cờ CLI từ `command:` đã được **làm động 100%**.

---

## 🎯 5 GIẢ THUYẾT CẦN RE-TEST THỰC TẾ TRÊN IMAGE V2

| STT | Giả thuyết / Hạng mục | Cơ chế thực sự ở Image v2 | Mục tiêu kỳ vọng |
| :--: | :--- | :--- | :--- |
| **H1** | **GPU Speculative Decoding** | `VLLM_SPECULATIVE_MODEL=LiquidAI/LFM2.5-350M-Instruct` | Giảm TPOT từ 4ms xuống dải **2.0 - 3.0ms** nhờ draft model 350M trên GPU. |
| **H2** | **True INT4 Online Quantization** | `VLLM_QUANTIZATION=compressed-tensors` & `marlin` | Giảm 50% Memory Bandwidth weight reads, bứt phá TPOT và giảm trễ TTFT. |
| **H3** | **True Max Model Length Reduction** | `VLLM_MAX_MODEL_LEN=16384` & `8192` | Tiết kiệm VRAM cho KV Cache, tăng khả năng xử lý concurrency không bị trễ. |
| **H4** | **Prompt Lookup N-gram Speculative** | `VLLM_SPECULATIVE_MODEL=[ngram]` | Tận dụng lặp từ trong prompt để sinh token nhanh mà không mất overhead GPU compute. |
| **H5** | **Chunked Prefill & KV Cache FP8** | `VLLM_ENABLE_CHUNKED_PREFILL=1` + `VLLM_KV_CACHE_DTYPE=fp8` | Tối ưu hóa TTFT P95 cho câu lệnh dài và tăng gấp đôi KV Cache capacity. |

---

## 🗓️ LỘ TRÌNH CHI TIẾT NGÀY 19/07 (TODAY - 10 SLOTS CÒN LẠI)

_Giai đoạn xác nhận độc lập từng giả thuyết trên nền Baseline FP8 Native 61.13đ (Compile L3 + Warmup v2)._

| Slot | File Compose | Cấu hình Re-test thực sự trên Image v2 | Giả thuyết kiểm chứng | Mục tiêu |
| :--: | :--- | :--- | :--: | :--- |
| **6** | `06-docker-compose.yml` | Draft LFM-350M + `Spec_Tokens=3` + `Quant=fp8` | **H1** | Step 1 (Lower Bound Speculative Decoding). |
| **7** | `07-docker-compose.yml` | Draft LFM-350M + `Spec_Tokens=6` + `Quant=fp8` | **H1** | Step 2 (Upper Bound Speculative Decoding). |
| **8** | `08-docker-compose.yml` | Draft LFM-350M + `Spec_Tokens=[Sweet Spot]` + `Quant=fp8` | **H1** | Step 3 (Sweet Spot Speculative Decoding). |
| **9** | `09-docker-compose.yml` | **True Compressed Tensors INT4** (`VLLM_QUANTIZATION=compressed-tensors`) | **H2** | Đo đạc tác động thực sự của Compressed Tensors INT4 trên v2. |
| **10** | `10-docker-compose.yml` | **True Marlin INT4** (`VLLM_QUANTIZATION=marlin`) | **H2** | Đo đạc tác động thực sự của Marlin INT4 kernels trên v2. |
| **11** | `11-docker-compose.yml` | **True Max Model Len 16K** (`VLLM_MAX_MODEL_LEN=16384`) | **H3** | Đo đạc thực sự việc giảm Max Len xuống 16K tác động đến TTFT P50. |
| **12** | `12-docker-compose.yml` | **True Max Model Len 8K** (`VLLM_MAX_MODEL_LEN=8192`) | **H3** | Đo đạc thực sự việc giảm Max Len xuống 8K xem có hạ P50 về < 40ms. |
| **13** | `13-docker-compose.yml` | **Prompt Lookup N-gram** (`VLLM_SPECULATIVE_MODEL=[ngram]`) | **H4** | Đánh giá N-gram Speculative Decoding thực sự hoạt động trên v2. |
| **14** | `14-docker-compose.yml` | Dự phòng khắc phục sự cố / Fine-tuning | - | Tinh chỉnh tham số phát sinh từ kết quả Slots 6-13. |
| **15** | `15-docker-compose.yml` | **Golden Combo Ngày 19/07** (Tích hợp Best từ Slots 6-13) | **H1+H2+H3** | Tích hợp Speculative + Quantization + MaxLen tối ưu nhất. |

---

## 🗓️ LỘ TRÌNH CHI TIẾT NGÀY 20/07 (TOMORROW - 15 SLOTS NÂNG CAO)

_Giai đoạn phối hợp nâng cao (Hybrid Optimization) và tối ưu hóa bộ nhớ KV Cache._

| Slot | Cấu hình thử nghiệm nâng cao | Mục tiêu kỹ thuật ngày 20/07 |
| :--: | :--- | :--- |
| **1** | `Best Quant` + `Best Spec_Tokens` (Hybrid Model) | Kết hợp lượng tử hóa tốt nhất và Speculative tốt nhất. |
| **2** | `Best Spec_Tokens` + `VLLM_KV_CACHE_DTYPE=fp8_e5m2` | Lượng tử hóa KV Cache sang FP8 để tăng bandwidth và giảm VRAM footprint. |
| **3** | `Best Spec_Tokens` + `VLLM_ENABLE_CHUNKED_PREFILL=1` (`Batched_Tokens=2048`) | Phân đoạn Prefill để giảm gai trễ (latency spike) TTFT P95. |
| **4** | `Best Spec_Tokens` + `VLLM_ENABLE_CHUNKED_PREFILL=1` (`Batched_Tokens=4096`) | Đánh giá Chunked Prefill mức 4K trên nền Speculative. |
| **5** | GPU Memory Utilization Sweep (`0.97` vs `0.95`) | Mở rộng vùng nhớ KV Cache tối đa cho concurrency 32. |
| **6 - 8** | Speculative Decoding Hyperparameter Sweep | Tinh chỉnh MQA Scorer, temperature draft model và max proposal tokens. |
| **9 - 11** | Concurrency Fine-tuning trên Golden Base (`Seqs=28`, `30`, `34`) | Tìm điểm nốt giao tối ưu chính xác giữa Throughput và TTFT. |
| **12 - 14** | Re-run & Grader Noise Elimination | Chạy lặp lại cấu hình tốt nhất vào các khung giờ ít tải của BTC để lấy điểm số đỉnh cao. |
| **15** | **ULTIMATE GOLDEN COMBO VÒNG 2** | Bản tổng hợp tất cả các kỹ thuật đạt điểm số cao nhất toàn bộ cuộc thi. |

---

## 📋 HƯỚNG DẪN THỰC THI NGAY
1. Nộp bài **Slot 6 ([06-docker-compose.yml](file:///d:/CODE%20PLAYGROUND/Projects/Competitions/Viettel%20AI%20Race/exercise%203/submissions/19072026/06-docker-compose.yml))** trên portal BTC để mở màn thử nghiệm **GPU Speculative Decoding (H1)**.
2. Ngay khi có kết quả Slot 6, chúng ta tiếp tục nộp lần lượt Slots 7, 8, 9, 10... để hoàn thành toàn bộ 5 giả thuyết trong ngày hôm nay!
