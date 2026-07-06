---
tags:
  -  #ViettelAIRace2026
  -  #LLM
  -  #Inference_Optimization
  -  #ActionPlan
status: 🚀 Active (Updated)
date: 2026-07-03
updated: 2026-07-06
---

# 🗺️ Kế hoạch Hành động Bài 3 (Vòng 1) - Revised v2

**Mục tiêu:** Tối ưu hóa inference Qwen/Qwen3.5-2B (BF16) trên vLLM, tối đa hóa ERS.
**Hạ tầng BTC:** MiG H200 (18GB VRAM / 3 CPU cores / 8GB RAM).
**Deadline:** 30/07/2026 (Còn 24 ngày).
**Chiến lược:** Submit-as-Test (max 5 submit/ngày, không có local GPU tương đương).

---

## 0. 🔍 Phân tích Trace & Kết quả đã chạy (Tình báo hiện tại)

### Trace Profile (trace-round1.jsonl)

| Đặc điểm               | Giá trị                                                    |
| :--------------------- | :--------------------------------------------------------- |
| Tổng request           | **120**                                                    |
| Thời gian phát request | **0 → 25.5 giây** (25.5s window)                           |
| Arrival interval       | Median **25ms**, max **4525ms** (bursty)                   |
| max_tokens (output)    | **200** cho tất cả 120 request                             |
| temperature            | **0** (deterministic)                                      |
| seed                   | **Đồng nhất 1 seed**                                       |
| Số messages/request    | **2 → 12** (multi-turn conversation)                       |
| Input length (chars)   | **78k → 167k chars** (~20k → 42k tokens)                   |
| System prompt          | **1 prompt chung** (shared prefix → prefix caching CÓ LỢI) |

### Kết luận chiến lược từ Trace

1. **Input CỰC DÀI** (20k-42k tokens) → Prefill phase chiếm phần lớn TTFT. Đây là nút thắt chính.
2. **Output NGẮN** (max 200 tokens) → Decode phase rất nhẹ, TPOT không phải vấn đề lớn.
3. **System prompt chung** → `--enable-prefix-caching` là BẮT BUỘC và rất hiệu quả.
4. **Bursty arrival** → Nhiều request đến gần nhau (25ms interval), cần xử lý batch tốt.
5. **max-model-len phải ≥ input max** → 42k tokens input + 200 tokens output ≈ cần tối thiểu ~45k tokens. Giá trị 32768 có thể quá nhỏ (truncate input dài nhất).

### Kết quả 6 Submissions đã chạy

| STT | Config chính                                              |   Điểm    | Bài học rút ra                                            |
| :-- | :-------------------------------------------------------- | :-------: | :-------------------------------------------------------- |
| 1   | Baseline gốc BTC (`max-model-len=262144`, `gpu-mem=0.95`) | **15.26** | Mốc chuẩn. 84/120 passed SLO. TTFT P50=670ms, P95=10058ms |
| 2   | Custom image, tham số tương đương baseline                | **15.03** | Custom image khả thi, giảm nhẹ (có thể do pull time)      |
| 3   | Baseline + `max-num-seqs=32`                              | **2.64**  | ❌ Giới hạn concurrency quá thấp → chỉ 10/120 passed SLO  |
| 4   | Baseline + `max-num-seqs=256`                             | **14.14** | ❌ Tăng concurrency quá cao → overhead scheduler tăng     |
| 5   | `max-model-len=32768` + `gpu-mem=0.98`                    | **15.00** | Gần baseline nhưng có thể truncate input dài nhất         |
| 6   | STT5 + `max-num-batched-tokens=1024`                      | **5.21**  | ❌ Giới hạn batch quá thấp → chỉ 46/120 passed SLO        |

### Phát hiện quan trọng

- **TTFT P95 ≈ 10 giây** cho mọi config đạt ~15 điểm → ~36 requests có TTFT > SLO ceiling (1500ms). Đây chính là input dài nhất (30k-42k tokens), prefill mất rất lâu.
- **ERS hiện tại ≈ 0.1526** (15.26/100) → Rất thấp. Phần lớn điểm đến từ requests ngắn (TTFT < 1500ms) và TPOT tốt.
- **84/120 passed SLO** → 36 request bị 0 điểm do TTFT vượt ceiling 1500ms.
- **Nút thắt #1:** Prefill time cho input dài. Cần giảm TTFT cho 36 request khổng lồ kia.

---

## 1. ⚙️ Triết lý Vận hành (The Pipeline) — Revised

### Không có Local GPU → Submit = Test

Vì không có phần cứng tương đương (MiG H200), mỗi submission trên portal BTC chính là 1 lượt test. Tối đa **5 submit/ngày**, cooldown 600s.

### Nguyên tắc vận hành

- **Kỷ luật đơn biến:** Mỗi submit chỉ thay đổi **DUY NHẤT 1 tham số** so với config tốt nhất hiện tại.
- **Config gốc (Reference):** Luôn giữ 1 slot/ngày để chạy lại config tốt nhất → xác nhận variance.
- **Ghi chép cẩn thận:** Mỗi submit tạo file `HHMM-docker-compose.yml` + `HHMM-result.md` trong folder `submissions/DDMMYYYY/`.

---

## 2. 🎯 Chiến lược Tối ưu (Ưu tiên theo ROI)

### Tier 1: Giảm TTFT cho input dài (Impact cao nhất)

Đây là con đường duy nhất để tăng điểm đáng kể. 36/120 request đang bị 0 điểm vì TTFT > 1500ms.

| Hướng tối ưu                                     | Cơ chế                                                                 | Kỳ vọng                                    | Ưu tiên |
| :----------------------------------------------- | :--------------------------------------------------------------------- | :----------------------------------------- | :-----: |
| **Chunked Prefill** (`--enable-chunked-prefill`) | Chia nhỏ prefill phase, xen kẽ với decode → giảm head-of-line blocking | Giảm TTFT P95 đáng kể                      |  🔴 P0  |
| **FP8 KV Cache** (`--kv-cache-dtype fp8`)        | Giảm 50% bộ nhớ KV cache → fit nhiều request hơn trong VRAM            | Tăng throughput, giảm queuing time         |  🔴 P0  |
| **FP8 Quantization** (`--quantization fp8`)      | Giảm 50% model weight → prefill nhanh hơn nhờ giảm memory bandwidth    | Giảm TTFT 20-30%                           |  🔴 P0  |
| **Speculative Decoding**                         | Draft model sinh token nhanh hơn                                       | Chỉ giúp decode (ít impact vì output ngắn) |  🟡 P2  |

### Tier 2: Tối ưu Scheduling & CPU (Impact trung bình)

| Hướng tối ưu                                        | Cơ chế                                      | Kỳ vọng                               | Ưu tiên |
| :-------------------------------------------------- | :------------------------------------------ | :------------------------------------ | :-----: |
| **Multi-step Scheduling** (`--num-scheduler-steps`) | Batch nhiều decode step → giảm CPU overhead | Giảm TPOT, giải phóng CPU cho prefill |  🟠 P1  |
| **CPU Thread Limits** (`OMP_NUM_THREADS=1`)         | Tránh thrashing 3 cores                     | Ổn định hóa, giảm variance            |  🟠 P1  |
| **max-num-seqs tuning**                             | Tìm sweet spot (default vs. custom)         | Tối ưu batch scheduling               |  🟠 P1  |

### Tier 3: Tối ưu Docker & Hệ thống (Impact thấp)

| Hướng tối ưu                      | Cơ chế                         | Kỳ vọng                | Ưu tiên |
| :-------------------------------- | :----------------------------- | :--------------------- | :-----: |
| **Custom Docker Image** (nhẹ hơn) | Giảm pull time, giảm RAM usage | Tăng nhẹ startup speed |  🟢 P2  |
| **shm_size tuning**               | Tối ưu shared memory           | Minor                  |  🟢 P2  |

### ❌ Hướng KHÔNG nên đi (đã chứng minh)

- `--max-num-seqs=32` hoặc quá thấp → Giết throughput (STT3: 2.64 điểm)
- `--max-num-seqs=256` hoặc quá cao → Overhead scheduler (STT4: 14.14 điểm)
- `--max-num-batched-tokens=1024` hoặc quá thấp → Nghẽn pipeline (STT6: 5.21 điểm)
- `--max-model-len=32768` → Có thể truncate input dài nhất (42k tokens). Cần test kỹ.

---

## 3. 📝 Nguyên tắc sử dụng 5 Slot/Ngày

| Slot       | Vai trò                                           | Ví dụ                                   |
| :--------- | :------------------------------------------------ | :-------------------------------------- |
| **Slot 1** | **Reference**: Chạy lại config tốt nhất hiện tại  | Xác nhận variance, đảm bảo điểm ổn định |
| **Slot 2** | **Test Biến A**: Thay đổi 1 tham số duy nhất      | Ví dụ: thêm `--enable-chunked-prefill`  |
| **Slot 3** | **Test Biến B**: Thay đổi 1 tham số khác          | Ví dụ: thêm `--kv-cache-dtype fp8`      |
| **Slot 4** | **Test Biến C**: Thay đổi 1 tham số khác          | Ví dụ: thêm `--num-scheduler-steps 8`   |
| **Slot 5** | **Verify / Combo**: Config kết hợp các biến thắng | Hoặc test edge case                     |

---

## 4. 🗓️ Lộ trình 24 Ngày Còn lại (06/07 → 30/07)

### ✅ Tuần 1 (03/07 – 06/07): HOÀN THÀNH

_Đã hoàn thành: Setup pipeline, baseline 15.26 điểm, custom image 15.03 điểm, phân tích trace._

**Kết quả Tuần 1:**

- Baseline BTC = 15.26 điểm (84/120 passed SLO)
- Custom image hoạt động tốt (15.03 điểm)
- Đã xác định: TTFT input dài là nút thắt chính
- Đã xác định: Prefix caching có lợi (shared system prompt)
- Đã loại: max-num-seqs quá thấp/cao, max-num-batched-tokens quá thấp

---

### Tuần 2 (07/07 – 13/07): Chunked Prefill & FP8 — Hai Đòn Quyết Định

_Mục tiêu: Giảm TTFT cho 36 request input dài. Tăng từ 15→20+ điểm._

#### Ngày 07/07 (5 slots)

| Slot | Config                                                                   | Mục đích                                |
| :--- | :----------------------------------------------------------------------- | :-------------------------------------- |
| 1    | Baseline gốc (reference)                                                 | Xác nhận điểm ổn định 15.26             |
| 2    | Baseline + `--enable-chunked-prefill`                                    | **Đòn chính #1**: Xen kẽ prefill/decode |
| 3    | Baseline + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096`  | Giới hạn chunk size                     |
| 4    | Baseline + `--enable-chunked-prefill` + `--max-num-batched-tokens=8192`  | Chunk size lớn hơn                      |
| 5    | Baseline + `--enable-chunked-prefill` + `--max-num-batched-tokens=16384` | Chunk size lớn nhất                     |

#### Ngày 08/07 (5 slots)

| Slot | Config                                                       | Mục đích                       |
| :--- | :----------------------------------------------------------- | :----------------------------- |
| 1    | Config thắng ngày 07 (reference)                             | Xác nhận                       |
| 2    | Config thắng + `--kv-cache-dtype fp8`                        | **Đòn chính #2**: FP8 KV cache |
| 3    | Config thắng + `--quantization fp8`                          | **Đòn chính #3**: FP8 weights  |
| 4    | Config thắng + `--quantization fp8` + `--kv-cache-dtype fp8` | Combo FP8 toàn diện            |
| 5    | Config thắng + `--num-scheduler-steps 8`                     | Multi-step scheduling          |

#### Ngày 09/07 (5 slots) — Tối ưu max-model-len

| Slot | Config                                  | Mục đích                            |
| :--- | :-------------------------------------- | :---------------------------------- |
| 1    | Config thắng ngày 08 (reference)        | Xác nhận                            |
| 2    | Config thắng + `--max-model-len=65536`  | Vừa đủ cho input dài nhất + output  |
| 3    | Config thắng + `--max-model-len=49152`  | Thử giới hạn chặt hơn (sát 42k+200) |
| 4    | Config thắng + `--max-model-len=131072` | Trung gian giữa 65k và 262k         |
| 5    | Best combo so far                       | Xác nhận combo tối ưu               |

#### Ngày 10-11/07 — CPU & Scheduling tuning

- Test `--num-scheduler-steps` (1, 4, 8, 12)
- Test environment variables: `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`
- Test `--disable-log-requests` (giảm CPU overhead)
- Test `--swap-space 0` vs default

#### Ngày 12-13/07 — Tổng kết & Đóng băng Tuần 2

- Chạy lại combo tốt nhất 3 lần ở các khung giờ khác nhau → đo variance
- Viết "Decision Memo Tuần 2"
- Đóng băng "Reference Config v2"

---

### Tuần 3 (14/07 – 20/07): Fine-tuning & Alternatives

_Mục tiêu: Squeeze thêm 2-5 điểm từ config hiện tại. Thử nghiệm SGLang nếu vLLM đã bão hòa._

#### Ngày 14-15/07 — Fine-tuning tham số

- Grid search: `--gpu-memory-utilization` (0.90, 0.92, 0.95, 0.98)
- Grid search: `--max-num-seqs` (64, 96, 128) kết hợp chunked prefill
- Test: `--enforce-eager` vs CUDA graphs (nếu chưa test)

#### Ngày 16-17/07 — Docker Image Optimization

- Build custom image nhẹ hơn (loại bỏ package không cần thiết)
- Test base image `nvidia/cuda:12.4.1-runtime-ubuntu22.04` + vLLM pip install
- Đo impact của image size lên pull time → startup time

#### Ngày 18-19/07 — Alternative Framework (nếu cần)

- Nếu vLLM đã bão hòa (~20 điểm), thử **SGLang** làm serving engine
- SGLang có RadixAttention (prefix caching tiên tiến hơn) và scheduling khác
- So sánh head-to-head với config vLLM tốt nhất

#### Ngày 20/07 — Tổng kết Tuần 3

- Chốt framework (vLLM vs SGLang)
- Đóng băng "Reference Config v3"

---

### Tuần 4 (21/07 – 27/07): Advanced Techniques

_Mục tiêu: Các kỹ thuật nâng cao nếu còn headroom._

#### Ngày 21-23/07 — Kỹ thuật nâng cao

- **Speculative Decoding** (nếu TPOT vẫn cao): Draft model nhỏ hơn
- **Disaggregated Prefill/Decode** (nếu framework hỗ trợ)
- **Custom entrypoint script** với warmup request trước khi benchmark bắt đầu

#### Ngày 24-25/07 — Variance Testing

- Submit config tốt nhất 5 lần/ngày ở các khung giờ khác nhau
- Vẽ biểu đồ phân phối điểm → xác nhận độ ổn định
- Nếu variance > 2 điểm → điều tra nguyên nhân

#### Ngày 26-27/07 — Tổng kết Tuần 4

- Đóng băng "Final Candidate Config"
- Chuẩn bị backup config (BF16 thuần) đề phòng

---

### Tuần 5 (28/07 – 30/07): Final Submission

_Mục tiêu: Nộp bài an toàn._

#### Ngày 28/07

- Submit Final Candidate 2-3 lần → xác nhận lần cuối
- Chuẩn bị backup config

#### Ngày 29/07

- **Buffer day**: Fix bug cuối cùng nếu có
- Clean up code, rà soát docker-compose, image tags

#### Ngày 30/07

- **🏁 SUBMIT FINAL** trước deadline
- Nộp config có điểm cao nhất và ổn định nhất

---

## 5. 🧮 Ước tính Điểm số Mục tiêu

### Phân tích cơ hội

Hiện tại: **15.26 điểm** (ERS = 0.1526)

```
Điểm = 100 × ERS × f(Δ)
     = 100 × (1/120 × Σ S_request) × 1.0  (vì accuracy_drop = 0)
```

Với 84/120 passed SLO (TTFT < 1500ms):

- 84 request đang đóng góp điểm (trung bình S_request ≈ 0.218)
- 36 request bị 0 điểm (TTFT > 1500ms)

**Nếu chunked prefill giảm TTFT cho 20 request thêm xuống < 1500ms:**

- 104/120 passed → ERS ≈ 0.20+ → **Điểm ≈ 20+**

**Nếu FP8 + chunked prefill giảm TTFT cho 30 request thêm:**

- 114/120 passed → ERS ≈ 0.25+ → **Điểm ≈ 25+**

**Mục tiêu thực tế:** **20-30 điểm** (tăng 50-100% so với baseline)
**Stretch goal:** **30+ điểm** (nếu gần như tất cả request đạt TTFT < 1500ms)

---

## 6. ⚠️ Rủi ro & Giải pháp

| Rủi ro                                       | Xác suất | Impact | Giải pháp                                                        |
| :------------------------------------------- | :------: | :----: | :--------------------------------------------------------------- |
| **FP8 quantization gây accuracy drop > 10%** | Thấp-TB  |  Cao   | Giữ BF16 fallback. Kiểm tra `accuracy_drop` trong kết quả submit |
| **Chunked prefill không cải thiện TTFT**     |   Thấp   |  Cao   | Chuyển sang SGLang hoặc thử max-model-len nhỏ hơn                |
| **max-model-len nhỏ gây truncate input**     |    TB    |  Cao   | Luôn test với giá trị > 45k tokens (an toàn: 49152 hoặc 65536)   |
| **Variance cao giữa các lần submit**         |    TB    |   TB   | Submit nhiều lần cùng config, chọn median                        |
| **vLLM v0.22.1 không hỗ trợ flag mới**       |    TB    |   TB   | Kiểm tra `--help` trước khi submit. Fallback về tham số an toàn  |
| **CPU 3 cores quá tải**                      |   Cao    |   TB   | Giới hạn threads, bật CUDA graphs, tăng num-scheduler-steps      |

---

## 7. 📋 Checklist Trước Mỗi Submit

- [ ] Chỉ thay đổi **1 biến** so với Reference Config
- [ ] Ghi lại docker-compose vào `submissions/DDMMYYYY/HHMM-docker-compose.yml`
- [ ] Sau khi có kết quả → ghi vào `submissions/DDMMYYYY/HHMM-result.md`
- [ ] Cập nhật `submissions/logs.md`
- [ ] Nếu điểm tăng → cập nhật Reference Config
