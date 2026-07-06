---
tags:
  -  #ViettelAIRace2026
  -  #LLM
  -  #Inference_Optimization
  -  #ActionPlan
status: 🚀 Active (Revised v3)
date: 2026-07-03
updated: 2026-07-06
---

# 🗺️ Kế hoạch Hành động Bài 3 (Vòng 1) - Revised v3

**Mục tiêu:** Tối ưu hóa inference Qwen/Qwen3.5-2B (BF16) trên vLLM, tối đa hóa ERS.
**Hạ tầng BTC:** MiG H200 (18GB VRAM / 3 CPU cores / 8GB RAM).
**Deadline:** 30/07/2026 (Còn 24 ngày).
**Chiến lược:** Submit-as-Test (max 5 submit/ngày, không có local GPU tương đương).

---

## 0. 🔍 Tình báo tích luỹ (Trace + 15 Submissions)

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

### Phân tích nguyên nhân gốc của 15 Submissions

#### ✅ 4 Submissions THÀNH CÔNG

| STT | Config chính                                              |   Điểm    | Bài học                                 |
| :-- | :-------------------------------------------------------- | :-------: | :-------------------------------------- |
| 4   | Baseline gốc BTC (`max-model-len=262144`, `gpu-mem=0.95`) | **15.26** | Mốc chuẩn. 84/120 passed SLO            |
| 7   | Custom image `bf16-v1`, tham số tương đương baseline      | **15.03** | Custom image khả thi                    |
| 12  | `max-model-len=32768` + `gpu-mem=0.98`                    | **15.00** | Gần baseline, có thể truncate input dài |
| 10  | Baseline + `max-num-seqs=32`                              | **2.64**  | ❌ Concurrency quá thấp                 |
| 11  | Baseline + `max-num-seqs=256`                             | **14.14** | ❌ Overhead scheduler tăng              |
| 14  | STT12 + `max-num-batched-tokens=1024`                     | **5.21**  | ❌ Batch quá nhỏ, nghẽn pipeline        |

#### ❌ 9 Submissions THẤT BẠI — Phân tích nguyên nhân gốc

> ⚠️ **PHÁT HIỆN QUAN TRỌNG:** Hầu hết các flag tối ưu (chunked prefill, FP8, scheduler steps) **CHƯA BAO GIỜ** được test trên image gốc BTC `vllm/vllm-openai:v0.22.1`. Chúng chỉ được thử trên image bị lỗi hoặc phiên bản vLLM cũ.

| STT       | Nguyên nhân thất bại THỰC SỰ                                     | Chi tiết                                                                                                                                                                                        |
| :-------- | :--------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 (1943)  | **Image chưa push lên Docker Hub** + flags chưa xác minh         | Image `viettel-qwen-local:v1` chưa được push → container không kéo được. Flags (`--enable-chunked-prefill`, `--num-scheduler-steps=8`) chưa được xác minh trên image hoạt động                  |
| 2 (1954)  | **Image chưa push lên Docker Hub**                               | Cùng image `viettel-qwen-local:v1` chưa push, transport errors do server không khởi động được                                                                                                   |
| 3 (2038)  | **Image chưa push** + `--max-model-len=8192` quá nhỏ             | Image `ptquanh/viettel-qwen35-2b:bf16-v1` chưa push tại thời điểm này. Ngoài ra `max-model-len=8192` cũng quá nhỏ cho trace (input 20k-42k tokens)                                              |
| 5 (2117)  | **Quá nhiều flag lạ cùng lúc** trên image gốc BTC                | `VLLM_USE_V1=1` + `--max-num-partial-prefills` + `--long-prefill-token-threshold` + `--kv-cache-dtype=fp8` + `--enforce-eager` + `--max-model-len=8192` → Không thể xác định flag nào gây crash |
| 6 (0631)  | **`--max-model-len=8192` + combo lỗi**                           | Có thể do conflict giữa `--max-model-len=8192` với `--max-num-batched-tokens=8192`, hoặc do `--disable-log-requests`                                                                            |
| 8 (0701)  | **Trùng lặp cấu hình STT6**                                      | Cùng lỗi                                                                                                                                                                                        |
| 9 (0747)  | **`--max-model-len=8192` quá nhỏ**                               | Server khởi động OK nhưng từ chối request dài → 120/120 transport errors                                                                                                                        |
| 13 (2217) | **`vllm/vllm-openai:v0.4.2` là phiên bản CŨ**, không tương thích | v0.4.2 là bản 2024, khác hoàn toàn v0.22.1 (bản 2026)                                                                                                                                           |
| 15 (2318) | **`v0.4.2` CŨ + không ổn định**                                  | 80/120 transport errors, bản cũ không kham nổi workload                                                                                                                                         |

> **Lưu ý:** STT1-3 fail vì image chưa được push lên Docker Hub. Kể từ STT7 (`04072026/0643`), custom image đã push thành công và hoạt động bình thường (15.03 điểm).

### Kết luận chiến lược RÚT RA

1. **`--max-model-len=8192` là CÁI BẪY** → Input trace dài 20k-42k tokens, giá trị <32768 chắc chắn gây lỗi.
2. **Không bao giờ đổi vLLM version** → `v0.22.1` là bản duy nhất hoạt động. `v0.4.2` (bản cũ) đã fail.
3. **Kỷ luật đơn biến BỊ VI PHẠM NẶNG** → Hầu hết các lần fail là do thay đổi quá nhiều biến cùng lúc, không thể xác định biến nào gây lỗi.
4. **Chunked prefill, FP8 KV cache, scheduler steps VẪN LÀ ẨN SỐ** → Chưa có bằng chứng chúng không hoạt động trên v0.22.1. Cần test lại đúng cách.

---

## 1. ⚙️ Triết lý Vận hành — Revised

### Không có Local GPU → Submit = Test

Mỗi submission trên portal BTC = 1 lượt test. Tối đa **5 submit/ngày**, cooldown 600s.

### Nguyên tắc TUYỆT ĐỐI (Rút kinh nghiệm từ 9 lần fail)

1. **Kỷ luật đơn biến NGHIÊM NGẶT:** Mỗi submit chỉ thay đổi **DUY NHẤT 1 tham số** so với config tốt nhất hiện tại. **KHÔNG BAO GIỜ** thay đổi 2+ biến cùng lúc.
2. **Luôn dùng image gốc BTC** `vllm/vllm-openai:v0.22.1` cho đến khi có lý do cực kỳ thuyết phục để đổi.
3. **`--max-model-len` ≥ 32768** (tuyệt đối không dùng 8192).
4. **1 slot/ngày dành cho Reference** (chạy lại config tốt nhất để đo variance).
5. **Ghi chép:** Mỗi submit → `HHMM-docker-compose.yml` + `HHMM-result.md` trong `submissions/DDMMYYYY/`.

---

## 2. 🎯 Chiến lược Tối ưu — Revised (ưu tiên theo ROI + khả thi)

### 🔴 Phase 0: Flag Discovery (ƯU TIÊN CAO NHẤT)

> **Mục tiêu:** Xác định chính xác flag nào được v0.22.1 hỗ trợ. Mỗi flag test RIÊNG LẺ trên baseline config.

| Flag cần xác minh             |      Đã test đúng cách?       | Kế hoạch                     |
| :---------------------------- | :---------------------------: | :--------------------------- |
| `--enable-chunked-prefill`    |  ❌ Chỉ test trên image lỗi   | **Test trên baseline image** |
| `--kv-cache-dtype fp8`        |    ❌ Chỉ test trên v0.4.2    | **Test trên baseline image** |
| `--quantization fp8`          |       ❌ Chưa từng test       | **Test trên baseline image** |
| `--num-scheduler-steps N`     |  ❌ Chỉ test trên image lỗi   | **Test trên baseline image** |
| `--disable-log-requests`      | ❌ Chỉ test kèm args lỗi khác | **Test trên baseline image** |
| `--enforce-eager`             |   ❌ Chỉ test kèm V1 engine   | **Test trên baseline image** |
| `OMP_NUM_THREADS=1` (env var) |  ❌ Chỉ test trên image lỗi   | **Test trên baseline image** |

### 🔴 Phase 1: Giảm TTFT (Impact cao nhất — nếu flag khả dụng)

| Hướng tối ưu                                     | Cơ chế                                                       | Kỳ vọng               | Ưu tiên |
| :----------------------------------------------- | :----------------------------------------------------------- | :-------------------- | :-----: |
| **Chunked Prefill** (`--enable-chunked-prefill`) | Chia nhỏ prefill, xen kẽ decode → giảm head-of-line blocking | Giảm TTFT P95 đáng kể |  🔴 P0  |
| **FP8 KV Cache** (`--kv-cache-dtype fp8`)        | Giảm 50% bộ nhớ KV → fit nhiều request                       | Tăng throughput       |  🔴 P0  |
| **FP8 Quantization** (`--quantization fp8`)      | Giảm 50% model weight → prefill nhanh hơn                    | Giảm TTFT 20-30%      |  🔴 P0  |

### 🟠 Phase 2: Tối ưu Scheduling & Tham số (nếu Phase 1 không đủ)

| Hướng tối ưu                                | Cơ chế                                 | Kỳ vọng              | Ưu tiên |
| :------------------------------------------ | :------------------------------------- | :------------------- | :-----: |
| **`--num-scheduler-steps N`**               | Batch decode steps → giảm CPU overhead | Giảm TPOT            |  🟠 P1  |
| **`--gpu-memory-utilization` tuning**       | Tìm sweet spot (0.95 vs 0.98)          | Minor                |  🟠 P1  |
| **`--max-model-len` tuning** (65536, 49152) | Giảm metadata overhead                 | Có thể cải thiện nhẹ |  🟠 P1  |
| **`--disable-log-requests`**                | Giảm CPU overhead                      | Minor                |  🟠 P1  |
| **CPU Thread Limits** (`OMP_NUM_THREADS=1`) | Tránh thrashing 3 cores                | Ổn định hoá          |  🟠 P1  |

### 🟢 Phase 3: Alternative Framework (nếu vLLM bão hòa)

| Hướng                   | Mô tả                           | Khi nào                                          |
| :---------------------- | :------------------------------ | :----------------------------------------------- |
| **SGLang**              | RadixAttention, scheduling khác | Chỉ nếu vLLM đã squeeze hết                      |
| **Custom Docker image** | vLLM mới hơn, nhẹ hơn           | Chỉ nếu có flag quan trọng không có trên v0.22.1 |

### ❌ DANH SÁCH CẤM (đã chứng minh thất bại)

| Cấu hình                          | Lý do cấm                                                 | Bằng chứng            |
| :-------------------------------- | :-------------------------------------------------------- | :-------------------- |
| `--max-model-len=8192`            | Input trace dài 20k-42k tokens, gây crash/transport error | STT2,3,6,8,9          |
| `--max-num-seqs=32` hoặc quá thấp | Giết throughput                                           | STT10: 2.64 điểm      |
| `--max-num-seqs=256` hoặc quá cao | Overhead scheduler                                        | STT11: 14.14 điểm     |
| `--max-num-batched-tokens=1024`   | Nghẽn pipeline                                            | STT14: 5.21 điểm      |
| `vllm/vllm-openai:v0.4.2`         | Phiên bản cũ, không tương thích                           | STT13,15: crash       |
| `VLLM_USE_V1=1`                   | V1 engine không ổn định trên v0.22.1                      | STT5: crash           |
| Thay đổi ≥2 biến cùng lúc         | Không xác định được nguyên nhân khi fail                  | 9/15 submissions fail |

---

## 3. 📝 Nguyên tắc sử dụng 5 Slot/Ngày

| Slot       | Vai trò                                                      | Ví dụ                                  |
| :--------- | :----------------------------------------------------------- | :------------------------------------- |
| **Slot 1** | **Reference**: Chạy lại config tốt nhất hiện tại             | Xác nhận variance                      |
| **Slot 2** | **Test Biến A**: Chỉ thêm/sửa 1 flag duy nhất                | Ví dụ: thêm `--enable-chunked-prefill` |
| **Slot 3** | **Test Biến B**: Chỉ thêm/sửa 1 flag khác                    | Ví dụ: thêm `--kv-cache-dtype fp8`     |
| **Slot 4** | **Test Biến C**: Chỉ thêm/sửa 1 flag khác                    | Ví dụ: thêm `--disable-log-requests`   |
| **Slot 5** | **Verify / Combo**: Kết hợp các biến ĐÃ CHỨNG MINH hoạt động | Chỉ combo từ các flag đã pass riêng lẻ |

---

## 4. 🗓️ Lộ trình 24 Ngày Còn lại (06/07 → 30/07)

### ✅ Tuần 1 (03/07 – 06/07): HOÀN THÀNH

_Đã hoàn thành: Setup pipeline, baseline 15.26 điểm, 15 submissions (6 success / 9 fail)._

**Bài học rút ra từ Tuần 1:**

- Baseline BTC = 15.26 điểm (84/120 passed SLO, TTFT P50=670ms, P95=10058ms)
- Custom image khả thi (15.03 điểm)
- `--max-model-len=8192` → CẤM (trace input quá dài)
- `--max-num-seqs` ngoài khoảng mặc định → điểm giảm
- Nhiều flag tối ưu chưa được test đúng cách (bị nhầm lẫn do test trên image lỗi)

---

### Tuần 2 (07/07 – 13/07): Flag Discovery + Đòn Quyết Định

_Mục tiêu: Xác minh flag nào khả dụng trên v0.22.1, sau đó tập trung vào chunked prefill + FP8._

#### Ngày 07/07 — Flag Discovery Day (QUAN TRỌNG NHẤT)

> Mỗi slot thêm DUY NHẤT 1 flag vào baseline config gốc (STT4).

| Slot | Config = Baseline + ...        | Mục đích                            |
| :--- | :----------------------------- | :---------------------------------- |
| 1    | (Baseline gốc, không thay đổi) | Reference: xác nhận 15.26 ổn định   |
| 2    | + `--enable-chunked-prefill`   | Xác minh flag có chạy trên v0.22.1? |
| 3    | + `--kv-cache-dtype fp8`       | Xác minh FP8 KV cache khả dụng?     |
| 4    | + `--disable-log-requests`     | Xác minh giảm CPU overhead?         |
| 5    | + `--num-scheduler-steps 8`    | Xác minh multi-step scheduling?     |

#### Ngày 08/07 — Discovery Day 2 + Đầu tiên Exploit

| Slot | Config                                | Mục đích                                         |
| :--- | :------------------------------------ | :----------------------------------------------- |
| 1    | + `--quantization fp8`                | Xác minh FP8 weights trên v0.22.1                |
| 2    | + `OMP_NUM_THREADS=1` (env var)       | Xác minh CPU thread limit                        |
| 3    | + `--max-model-len=65536`             | Test giảm context length (an toàn cho 42k input) |
| 4    | Flag thắng từ ngày 07 (combo 2 flags) | Kết hợp 2 flags đã pass riêng lẻ                 |
| 5    | Flag thắng từ ngày 07 (combo khác)    | Kết hợp khác                                     |

#### Ngày 09-10/07 — Exploit Phase

- Xây dựng combo từ các flags ĐÃ CHỨNG MINH hoạt động
- Mỗi ngày: 1 reference + 4 combo tests
- Tìm combo cho điểm cao nhất

#### Ngày 11-12/07 — max-model-len + gpu-memory-utilization Grid Search

- `--max-model-len`: 49152, 65536, 131072 (so với baseline 262144)
- `--gpu-memory-utilization`: 0.90, 0.92, 0.95, 0.98
- Kết hợp với các flags thắng từ ngày 09-10

#### Ngày 13/07 — Tổng kết & Đóng băng Tuần 2

- Chạy config tốt nhất 3 lần → đo variance
- Đóng băng "Reference Config v2"

---

### Tuần 3 (14/07 – 20/07): Fine-tuning & Alternatives

_Mục tiêu: Squeeze thêm 2-5 điểm. Thử SGLang nếu vLLM bão hòa._

#### Ngày 14-16/07 — Fine-tuning tham số

- Grid search `--max-num-seqs` (64, 96, 128) kết hợp config tốt nhất
- Grid search `--max-num-batched-tokens` (4096, 8192, 16384) kết hợp chunked prefill (nếu khả dụng)
- Test `--swap-space 0` vs default
- Test `--enforce-eager` vs CUDA graphs

#### Ngày 17-19/07 — Alternative Framework (nếu cần)

- Nếu vLLM đã bão hoà (~20 điểm), thử **SGLang** với custom Docker image
- SGLang có RadixAttention (prefix caching tiên tiến hơn)
- So sánh head-to-head với config vLLM tốt nhất

#### Ngày 20/07 — Tổng kết Tuần 3

- Chốt framework (vLLM vs SGLang)
- Đóng băng "Reference Config v3"

---

### Tuần 4 (21/07 – 27/07): Advanced Techniques + Variance

_Mục tiêu: Kỹ thuật nâng cao + kiểm chứng ổn định._

#### Ngày 21-23/07 — Kỹ thuật nâng cao

- **Custom entrypoint script** với warmup request trước benchmark
- **Speculative Decoding** (nếu TPOT vẫn cao)
- **Disaggregated Prefill/Decode** (nếu framework hỗ trợ)

#### Ngày 24-26/07 — Variance Testing

- Submit config tốt nhất 5 lần/ngày ở các khung giờ khác nhau
- Vẽ phân phối điểm → xác nhận ổn định
- Nếu variance > 2 điểm → điều tra

#### Ngày 27/07 — Đóng băng Final

- "Final Candidate Config" + backup config BF16 thuần

---

### Tuần 5 (28/07 – 30/07): Final Submission

#### Ngày 28/07

- Submit Final Candidate 2-3 lần → xác nhận lần cuối

#### Ngày 29/07

- **Buffer day**: Fix bug, clean up

#### Ngày 30/07

- **🏁 SUBMIT FINAL** trước deadline

---

## 5. 🧮 Ước tính Điểm số Mục tiêu

### Hiện tại: **15.26 điểm** (ERS = 0.1526)

- 84/120 request đóng góp điểm (trung bình S_request ≈ 0.218)
- 36/120 request bị **0 điểm** (TTFT > 1500ms ceiling)

### Kịch bản tăng điểm

| Kịch bản                                   | Cách đạt                                       | Ước tính điểm |
| :----------------------------------------- | :--------------------------------------------- | :-----------: |
| **Chunked prefill hoạt động**              | Giảm TTFT cho ~20 request thêm xuống <1500ms   |   **20-22**   |
| **FP8 + Chunked prefill**                  | Giảm TTFT cho ~30 request thêm                 |   **25-28**   |
| **FP8 + Chunked + tuning**                 | Gần toàn bộ 120 request đạt SLO                |    **30+**    |
| **Chỉ tuning tham số (không có flag mới)** | Tối ưu batch/scheduling trong giới hạn v0.22.1 |   **16-18**   |

### Mục tiêu

- **Thực tế:** **20-25 điểm** (nếu chunked prefill hoặc FP8 hoạt động)
- **Stretch:** **30+ điểm**
- **Worst case:** **16-18 điểm** (chỉ tuning tham số cơ bản)

---

## 6. ⚠️ Rủi ro & Giải pháp — Updated

| Rủi ro                                         |    Xác suất     | Impact  | Giải pháp                                                              |
| :--------------------------------------------- | :-------------: | :-----: | :--------------------------------------------------------------------- |
| **v0.22.1 không hỗ trợ chunked prefill / FP8** |       TB        | Rất Cao | Ngày 07/07 sẽ xác minh. Nếu fail → chuyển sang tuning tham số + SGLang |
| **FP8 gây accuracy drop > 10%**                |     Thấp-TB     |   Cao   | Kiểm tra `accuracy_drop` kết quả. Giữ BF16 fallback                    |
| **max-model-len nhỏ gây truncate input**       |    Đã xảy ra    |   Cao   | ≥ 32768, an toàn: 49152 hoặc 65536                                     |
| **Variance cao giữa các lần submit**           |       TB        |   TB    | Submit nhiều lần cùng config, chọn median                              |
| **CPU 3 cores quá tải**                        |       Cao       |   TB    | `OMP_NUM_THREADS=1`, `--disable-log-requests`, `--num-scheduler-steps` |
| **Vi phạm kỷ luật đơn biến**                   | Đã xảy ra 9 lần |   Cao   | Checklist bắt buộc. KHÔNG submit khi chưa review                       |

---

## 7. 📋 Checklist NGHIÊM NGẶT Trước Mỗi Submit

- [ ] **Image:** Có phải `vllm/vllm-openai:v0.22.1` không? (Nếu không → CẦN LÝ DO CỰC KỲ THUYẾT PHỤC)
- [ ] **Đơn biến:** Chỉ thay đổi **ĐÚNG 1 tham số** so với Reference Config?
- [ ] **max-model-len:** Giá trị ≥ 32768?
- [ ] **Không có flag cấm:** Không dùng `VLLM_USE_V1=1`, v0.4.2, max-model-len=8192?
- [ ] **Đã ghi file:** `submissions/DDMMYYYY/HHMM-docker-compose.yml` đã tạo?
- [ ] Sau khi có kết quả → ghi `HHMM-result.md` + cập nhật `submissions/logs.md`
- [ ] Nếu điểm tăng → cập nhật Reference Config
