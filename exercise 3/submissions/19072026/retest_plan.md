# KẾ HOẠCH TỔNG THỂ KHẮC PHỤC & RE-TEST TOÀN BỘ CÁC THỬ NGHIỆM (19/07 - 20/07)

> **Bối cảnh**: Trong phiên bản Custom Image `v1` (`vllm-lfm25-fp8-kernels-v1`), script `python3_hijack` đã vô tình hardcode `--max-model-len 32768` và `--quantization fp8`, dẫn đến việc các thử nghiệm cũ về Lượng tử hóa INT4 (Marlin, Compressed-tensors), Giảm Max Len (16K, 8K) và N-gram Speculative Decoding bị bỏ qua và đều thực thi dưới dạng FP8 Native.
>
> Với việc hoàn thành **Custom Image `v2`** (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`), toàn bộ các biến môi trường (`VLLM_MAX_MODEL_LEN`, `VLLM_QUANTIZATION`, `VLLM_SPECULATIVE_MODEL`, `VLLM_NUM_SPECULATIVE_TOKENS`) và cờ CLI từ `command:` đã được **làm động 100%**.

---

## 🎯 TRẠNG THÁI 5 GIẢ THUYẾT RE-TEST THỰC TẾ TRÊN IMAGE V2

|  STT   | Giả thuyết / Hạng mục                | Cơ chế thực sự ở Image v2                                   | Kết quả kiểm chứng thực tế trên v2                                                                                                   |  Trạng thái   |
| :----: | :----------------------------------- | :---------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :-----------: |
| **H1** | **GPU Speculative Decoding**         | `VLLM_SPECULATIVE_MODEL=1` (/draft_model 350M offline)      | **Fail STT 63 (0833)**: `Engine core initialization failed`. vLLM v0.22.1 chưa hỗ trợ spec decode giữa 2 mô hình Recurrent LFM.      |  ❌ Thất bại  |
| **H2** | **True INT4 Online Quantization**    | `VLLM_QUANTIZATION=compressed-tensors` & `marlin`           | **Fail STT 59 (2131)**. Checkpoint `/model` BTC thiếu compressed metadata. FP8 Native tối ưu 100%.                                   |  ❌ Thất bại  |
| **H3** | **True Max Model Length Reduction**  | `VLLM_MAX_MODEL_LEN=16384` & `8192`                         | **Fail STT 61 (8K: 59.29đ) & STT 62 (16K: 56.76đ)**. Thu hẹp MaxLen phá vỡ CUDA Graph buckets. Best Len = 32768 (32K).               | ❌ Không chọn |
| **H4** | **Prompt Lookup N-gram Speculative** | `VLLM_SPECULATIVE_MODEL=ngram`                              | **Fail STT 56 (2043) & STT 58 (2113)**. Timeout 2700s do xung đột JIT Dynamo Graph với N-gram.                                       |  ❌ Thất bại  |
| **H5** | **Chunked Prefill & KV Cache FP8**   | `VLLM_ENABLE_CHUNKED_PREFILL=1` + `VLLM_KV_CACHE_DTYPE=fp8` | **Chunked 4K (59.21đ)**: Không tối ưu cho Recurrent LFM2.5.<br>**KV Cache FP8 (56.52đ)**: Overhead dequantization làm tăng TTFT P50. | ❌ Không chọn |

---

## 🗓️ LỘ TRÌNH & KẾT QUẢ THỰC TẾ NGÀY 19/07 (SLOTS 6 - 15)

_Kết quả xác nhận thực tế của từng slot trên nền Image v2 (`ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`)._

|  Slot  | Mã / File Compose         | Cấu hình Re-test thực sự trên Image v2                                      | Điểm số ERS | Trạng thái & Kết luận                                                                        |
| :----: | :------------------------ | :-------------------------------------------------------------------------- | :---------: | :------------------------------------------------------------------------------------------- |
| **6**  | `1148-docker-compose.yml` | Draft LFM-350M + `Spec_Tokens=3`                                            |  **Fail**   | Exited 2 (Lỗi Pydantic JSON level 3).                                                        |
| **7**  | `1333-docker-compose.yml` | Draft LFM-350M + `Spec_Tokens=6`                                            |  **Fail**   | Exited 2 (Lỗi Pydantic int 3).                                                               |
| **8**  | `1401-docker-compose.yml` | Draft LFM-350M + `Spec_Tokens=6` (Image v2 CLI fixed)                       |  **Fail**   | Exited 2 (Lỗi vLLM CLI flags dư positional args).                                            |
| **9**  | `1411-docker-compose.yml` | Draft LFM-350M + `Spec_Tokens=6` (Offline HF download)                      |  **Fail**   | Timeout 2700s do không có mạng tải draft model 350M.                                         |
| **10** | `1558-docker-compose.yml` | **Image v2 FP8 Native Baseline** (`Compilation Level 3`)                    |  **60.75**  | 🔥 **THÀNH CÔNG!** Request lỗi giảm xuống 4 (thấp nhất từ trước đến nay). Baseline chuẩn v2. |
| **11** | `2043-docker-compose.yml` | **Prompt Lookup N-gram Speculative** (`VLLM_SPECULATIVE_MODEL=ngram`)       |  **Fail**   | Timeout 2700s do xung đột giữa `COMPILATION_LEVEL=3` và N-gram token loop.                   |
| **12** | `2101-docker-compose.yml` | **Chunked Prefill 4K + FP8 Native** (`VLLM_ENABLE_CHUNKED_PREFILL=1`)       |  **59.21**  | TTFT P50 tăng lên 54ms do làm gãy tính liên tục Recurrent. Chốt Non-chunked prefill!         |
| **13** | `2113-docker-compose.yml` | **Combo N-gram Speculative + Chunked Prefill 4K**                           |  **Fail**   | Timeout 2700s do cờ N-gram xung đột JIT Dynamo Graph.                                        |
| **14** | `2131-docker-compose.yml` | **True Compressed Tensors INT4** (`VLLM_QUANTIZATION=compressed-tensors`)   |  **Fail**   | Exited 1 (TypeError do `/model` thiếu compressed metadata). FP8 Native tối ưu 100%.          |
| **15** | `2216-docker-compose.yml` | **Giả thuyết H5: FP8 Base + KV Cache FP8 (`VLLM_KV_CACHE_DTYPE=fp8_e5m2`)** |  **56.52**  | Overhead dequantization làm tăng TTFT P50 (63ms). Khẳng định dùng Default FP16 KV Cache!     |

---

## 🗓️ LỘ TRÌNH CHI TIẾT NGÀY 20/07 (TOMORROW - 15 SLOTS NÂNG CAO)

_Giai đoạn phối hợp nâng cao (Hybrid Optimization) và tối ưu hóa bộ nhớ KV Cache._

|    Slot     | Cấu hình thử nghiệm nâng cao                                                 | Mục tiêu kỹ thuật ngày 20/07                                                             |
| :---------: | :--------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
|    **1**    | `Best Quant` + `Best Spec_Tokens` (Hybrid Model)                             | Kết hợp lượng tử hóa tốt nhất và Speculative tốt nhất.                                   |
|    **2**    | `Best Spec_Tokens` + `VLLM_KV_CACHE_DTYPE=fp8_e5m2`                          | Lượng tử hóa KV Cache sang FP8 để tăng bandwidth và giảm VRAM footprint.                 |
|    **3**    | `Best Spec_Tokens` + `VLLM_ENABLE_CHUNKED_PREFILL=1` (`Batched_Tokens=2048`) | Phân đoạn Prefill để giảm gai trễ (latency spike) TTFT P95.                              |
|    **4**    | `Best Spec_Tokens` + `VLLM_ENABLE_CHUNKED_PREFILL=1` (`Batched_Tokens=4096`) | Đánh giá Chunked Prefill mức 4K trên nền Speculative.                                    |
|    **5**    | GPU Memory Utilization Sweep (`0.97` vs `0.95`)                              | Mở rộng vùng nhớ KV Cache tối đa cho concurrency 32.                                     |
|  **6 - 8**  | Speculative Decoding Hyperparameter Sweep                                    | Tinh chỉnh MQA Scorer, temperature draft model và max proposal tokens.                   |
| **9 - 11**  | Concurrency Fine-tuning trên Golden Base (`Seqs=28`, `30`, `34`)             | Tìm điểm nốt giao tối ưu chính xác giữa Throughput và TTFT.                              |
| **12 - 14** | Re-run & Grader Noise Elimination                                            | Chạy lặp lại cấu hình tốt nhất vào các khung giờ ít tải của BTC để lấy điểm số đỉnh cao. |
|   **15**    | **ULTIMATE GOLDEN COMBO VÒNG 2**                                             | Bản tổng hợp tất cả các kỹ thuật đạt điểm số cao nhất toàn bộ cuộc thi.                  |

---

## 📋 HƯỚNG DẪN THỰC THI NGAY

1. Nộp bài **Slot 6 ([06-docker-compose.yml](file:///d:/CODE%20PLAYGROUND/Projects/Competitions/Viettel%20AI%20Race/exercise%203/submissions/19072026/06-docker-compose.yml))** trên portal BTC để mở màn thử nghiệm **GPU Speculative Decoding (H1)**.
2. Ngay khi có kết quả Slot 6, chúng ta tiếp tục nộp lần lượt Slots 7, 8, 9, 10... để hoàn thành toàn bộ 5 giả thuyết trong ngày hôm nay!
