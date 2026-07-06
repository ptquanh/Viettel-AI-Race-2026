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

#### 📊 6 Submissions CÓ ĐIỂM (Không bị crash)

| STT | Config chính                                              |   Điểm    | Phân loại | Bài học                                 |
| :-- | :-------------------------------------------------------- | :-------: | :-------: | :-------------------------------------- |
| 4   | Baseline gốc BTC (`max-model-len=262144`, `gpu-mem=0.95`) | **15.26** |    ✅     | Mốc chuẩn. 84/120 passed SLO            |
| 7   | Custom image `bf16-v1`, tham số tương đương baseline      | **15.03** |    ✅     | Custom image khả thi                    |
| 12  | `max-model-len=32768` + `gpu-mem=0.98`                    | **15.00** |    ✅     | Gần baseline, có thể truncate input dài |
| 11  | Baseline + `max-num-seqs=256`                             | **14.14** |    ⚠️     | Overhead scheduler tăng                 |
| 14  | STT12 + `max-num-batched-tokens=1024`                     | **5.21**  |    ❌     | Batch quá nhỏ, nghẽn pipeline           |
| 10  | Baseline + `max-num-seqs=32`                              | **2.64**  |    ❌     | Concurrency quá thấp                    |

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

### Phân tích cơ hội tối ưu theo công thức ERS

> ⚠️ **NHẮC NHỞ QUAN TRỌNG:** `S_request = 0.5 × s_ttft + 0.5 × s_tpot` — **TPOT chiếm 50% trọng số**, không chỉ TTFT!

**Công thức chi tiết:**

- `s_ttft = clamp((1500 - TTFT) / (1500 - 100), 0, 1)²` → Floor=100ms, Ceiling=1500ms
- `s_tpot = clamp((45 - TPOT) / (45 - 20), 0, 1)²` → Floor=20ms, Ceiling=45ms

**Baseline metrics cần phân tích sâu:**

- TTFT: P50=670ms, P95=10058ms → 84/120 có TTFT < 1500ms, 36/120 bị 0 điểm
- TPOT: Chưa có data chi tiết → **CẦN ĐO ĐẠC từ kết quả baseline**
- Ví dụ TPOT impact: Nếu TPOT giảm từ 30ms → 22ms, s_tpot tăng từ 0.36 → 0.85 (tăng 136%!)

**Phân bổ điểm ước tính (baseline 15.26 điểm = ERS 0.1526):**

- Nhóm A: ~30 request có TTFT < 200ms → s_ttft gần max → đã gần tối ưu
- Nhóm B: ~54 request có TTFT 200ms-1500ms → còn room tăng điểm bằng giảm TTFT
- Nhóm C: ~36 request có TTFT > 1500ms → đang 0 điểm hoàn toàn → ROI cao nhất
- **TPOT:** Nếu TPOT > 25ms cho cả 120 request, tối ưu TPOT cũng mang lại ROI lớn

### Kết luận chiến lược RÚT RA

1. **`--max-model-len=8192` là CÁI BẪY** → Input trace dài 20k-42k tokens, giá trị <32768 chắc chắn gây lỗi.
2. **Không bao giờ đổi vLLM version** → `v0.22.1` là bản duy nhất hoạt động. `v0.4.2` (bản cũ) đã fail.
3. **Kỷ luật đơn biến BỊ VI PHẠM NẶNG** → Hầu hết các lần fail là do thay đổi quá nhiều biến cùng lúc, không thể xác định biến nào gây lỗi.
4. **Chunked prefill, FP8 KV cache, scheduler steps VẪN LÀ ẨN SỐ** → Chưa có bằng chứng chúng không hoạt động trên v0.22.1. Cần test lại đúng cách.
5. **TPOT = 50% trọng số** → Cần đo TPOT baseline và tối ưu song song với TTFT. `--num-scheduler-steps` là hướng trực tiếp giảm TPOT.

---

## 1. ⚙️ Triết lý Vận hành — Revised

### Không có Local GPU → Submit = Test

Mỗi submission trên portal BTC = 1 lượt test. Tối đa **5 submit/ngày**, cooldown 600s.

### Quy định của BTC về độ biến động (Variance)

> 💡 **Thông tin từ BTC:** Đối với các bài thi tính toán hiệu năng, BTC đã cấu hình hệ thống bench để duy trì mức sai số **< 2%**. Ở mỗi lượt submission, kết quả của các đội được **lấy trung bình từ tối thiểu 3 lần chấm** để đảm bảo tính ổn định. Do đó:
>
> - **KHÔNG cần tốn slot chạy đối chứng (Reference)** hàng ngày để đo độ biến động.
> - Tiết kiệm được tối đa số slot để thử nghiệm trực tiếp các tham số tối ưu mới.

### Nguyên tắc TUYỆT ĐỐI (Rút kinh nghiệm từ 9 lần fail)

1. **Kỷ luật đơn biến NGHIÊM NGẶT:** Mỗi submit chỉ thay đổi **DUY NHẤT 1 tham số** so với cấu hình chạy thành công gần nhất. **KHÔNG BAO GIỜ** thay đổi 2+ biến cùng lúc.
2. **Luôn dùng image gốc BTC** `vllm/vllm-openai:v0.22.1` làm mốc gốc cho đến khi chứng minh được flag hoạt động.
3. **`--max-model-len` ≥ 32768** (tuyệt đối không dùng 8192).
4. **Ghi chép:** Mỗi submit → `HHMM-docker-compose.yml` + `HHMM-result.md` trong `submissions/DDMMYYYY/`.

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
| **`--num-scheduler-steps N`**                    | Batch decode steps → giảm CPU overhead → **giảm TPOT**       | Giảm TPOT (50% ERS!)  |  🔴 P0  |

### 🟠 Phase 2: Tối ưu Scheduling & Tham số (nếu Phase 1 không đủ)

| Hướng tối ưu                                | Cơ chế                                                  | Kỳ vọng              | Ưu tiên |
| :------------------------------------------ | :------------------------------------------------------ | :------------------- | :-----: |
| **`--gpu-memory-utilization` tuning**       | Tìm sweet spot (0.95 vs 0.98)                           | Minor                |  🟠 P1  |
| **`--max-model-len` tuning** (65536, 49152) | Giảm metadata overhead, giải phóng VRAM cho KV cache    | Có thể cải thiện nhẹ |  🟠 P1  |
| **`--disable-log-requests`**                | Giảm CPU overhead (3 cores rất hạn chế)                 | Minor                |  🟠 P1  |
| **`--enforce-eager`**                       | Tắt CUDA graphs → giảm VRAM overhead, trade-off latency | Cần xác minh         |  🟠 P1  |
| **CPU Thread Limits** (`OMP_NUM_THREADS=1`) | Tránh thrashing 3 cores                                 | Ổn định hoá          |  🟠 P1  |

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
| **Slot 1** | **Test Biến A**: Thử nghiệm 1 flag tối ưu tiềm năng          | Ví dụ: thêm `--enable-chunked-prefill` |
| **Slot 2** | **Test Biến B**: Thử nghiệm 1 flag tối ưu khác               | Ví dụ: thêm `--kv-cache-dtype fp8`     |
| **Slot 3** | **Test Biến C**: Thử nghiệm 1 flag tối ưu khác               | Ví dụ: thêm `--disable-log-requests`   |
| **Slot 4** | **Test Biến D**: Thử nghiệm 1 flag tối ưu khác               | Ví dụ: thêm `--num-scheduler-steps 8`  |
| **Slot 5** | **Verify / Combo**: Kết hợp các biến ĐÃ CHỨNG MINH hoạt động | Chỉ combo từ các flag đã pass riêng lẻ |

---

## 4. 🗓️ Lộ trình 24 Ngày Còn lại (06/07 → 30/07)

### ✅ Tuần 1 (03/07 – 05/07): HOÀN THÀNH

_Đã hoàn thành: Setup pipeline, baseline 15.26 điểm, 15 submissions (6 success / 9 fail)._

**Bài học rút ra từ Tuần 1:**

- Baseline BTC = 15.26 điểm (84/120 passed SLO, TTFT P50=670ms, P95=10058ms)
- Custom image khả thi (15.03 điểm)
- `--max-model-len=8192` → CẤM (trace input quá dài)
- `--max-num-seqs` ngoài khoảng mặc định → điểm giảm
- Nhiều flag tối ưu chưa được test đúng cách (bị nhầm lẫn do test trên image lỗi)

---

### Tuần 2 (06/07 – 12/07): Flag Discovery + Đòn Quyết Định

_Mục tiêu: Xác minh flag nào khả dụng trên v0.22.1, sau đó tập trung vào chunked prefill + FP8._

#### Ngày 06/07 — Flag Discovery Day 1 (QUAN TRỌNG NHẤT)

> Mỗi slot thêm DUY NHẤT 1 flag tối ưu vào baseline config gốc (STT4) trên image `vllm/vllm-openai:v0.22.1`.

| Slot | Config = Baseline + ...      | Mục đích                            |
| :--- | :--------------------------- | :---------------------------------- |
| 1    | + `--enable-chunked-prefill` | Xác minh flag có chạy trên v0.22.1? |
| 2    | + `--kv-cache-dtype fp8`     | Xác minh FP8 KV cache khả dụng?     |
| 3    | + `--disable-log-requests`   | Xác minh giảm CPU overhead?         |
| 4    | + `--num-scheduler-steps 8`  | Xác minh multi-step scheduling?     |
| 5    | + `OMP_NUM_THREADS=1` (env)  | Xác minh CPU thread limit           |

#### Ngày 07/07 — Flag Discovery Day 2 + Đầu tiên Exploit

| Slot | Config                                | Mục đích                                                |
| :--- | :------------------------------------ | :------------------------------------------------------ |
| 1    | + `--quantization fp8`                | Xác minh FP8 weights trên v0.22.1                       |
| 2    | + `--enforce-eager`                   | Xác minh tắt CUDA graphs (giải phóng VRAM)              |
| 3    | + `--max-model-len=65536`             | Test giảm context length (an toàn, 65k > 42k input max) |
| 4    | Flag thắng từ ngày 06 (combo 2 flags) | Kết hợp 2 flags đã pass riêng lẻ                        |
| 5    | Flag thắng từ ngày 06 (combo khác)    | Kết hợp khác                                            |

#### Ngày 08-09/07 — Exploit Phase

- Xây dựng combo từ các flags ĐÃ CHỨNG MINH hoạt động
- Mỗi ngày: 5 combo tests
- Tìm combo cho điểm cao nhất

#### Ngày 10-11/07 — max-model-len + gpu-memory-utilization Grid Search

- `--max-model-len`: 49152, 65536, 131072 (so với baseline 262144)
- `--gpu-memory-utilization`: 0.90, 0.92, 0.95, 0.98
- Kết hợp với các flags thắng từ ngày 08-09

#### Ngày 12/07 — Tổng kết & Đóng băng Tuần 2

- Chạy config tốt nhất để đo đạc độ ổn định
- Đóng băng "Reference Config v2"

---

### Tuần 3 (13/07 – 20/07): Fine-tuning & Alternatives

_Mục tiêu: Squeeze thêm 2-5 điểm. Thử SGLang nếu vLLM bão hòa._

#### Ngày 13-15/07 — Fine-tuning tham số

- Grid search `--max-num-seqs` (64, 96, 128) kết hợp config tốt nhất
- Grid search `--max-num-batched-tokens` (4096, 8192, 16384) kết hợp chunked prefill (nếu khả dụng)
- Test `--max-model-len` fine-tuning: 49152 vs 65536 vs 131072 (nếu chưa test ở Tuần 2)
- Test `--swap-space 0` vs default

#### Ngày 16-18/07 — Alternative Framework (nếu cần)

- Nếu vLLM đã bão hoà (~20 điểm), thử **SGLang** với custom Docker image
- SGLang có RadixAttention (prefix caching tiên tiến hơn)
- So sánh head-to-head với config vLLM tốt nhất

#### Ngày 19-20/07 — Tổng kết Tuần 3

- Chốt framework (vLLM vs SGLang)
- Đóng băng "Reference Config v3"
- Variance check: chạy config tốt nhất 2-3 lần để xác nhận ổn định

---

### Tuần 4 (21/07 – 27/07): Advanced Techniques + Final Polish

_Mục tiêu: Kỹ thuật nâng cao + đóng băng config cuối._

#### Ngày 21-24/07 — Kỹ thuật nâng cao

- **Custom entrypoint script** với warmup request trước benchmark
- **Speculative Decoding** (nếu TPOT vẫn cao)
- **Disaggregated Prefill/Decode** (nếu framework hỗ trợ)
- Tiếp tục fine-tune combo tham số từ best config Tuần 3

#### Ngày 25/07 — Variance Check (1 ngày, không 3 ngày)

> BTC đã lấy trung bình ≥3 lần chấm với sai số < 2%, không cần test variance nhiều.

- Submit config tốt nhất 3-5 lần trong ngày → xác nhận ổn định
- Nếu variance > 2 điểm → điều tra (hiếm khi xảy ra theo BTC)

#### Ngày 26-27/07 — Đóng băng Final

- "Final Candidate Config" + backup config BF16 thuần
- Rà soát docker-compose, image tags, clean up

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
- TPOT data: chưa có → **Cần đo từ kết quả submit tiếp theo**

### Kịch bản tăng điểm

| Kịch bản                                   | Cách đạt                                       | Ước tính điểm |
| :----------------------------------------- | :--------------------------------------------- | :-----------: |
| **Chunked prefill hoạt động**              | Giảm TTFT cho ~20 request thêm xuống <1500ms   |   **20-22**   |
| **FP8 + Chunked prefill**                  | Giảm TTFT cho ~30 request thêm                 |   **25-28**   |
| **FP8 + Chunked + TPOT tuning**            | Tối ưu cả TTFT lẫn TPOT cho toàn bộ 120 req    |    **30+**    |
| **Chỉ tuning tham số (không có flag mới)** | Tối ưu batch/scheduling trong giới hạn v0.22.1 |   **16-18**   |
| **⚠️ FP8 + accuracy drop 12%**             | f(Δ) = 0.67 → điểm bị nhân 0.67                | **Giảm 33%**  |
| **⚠️ FP8 + accuracy drop ≥ 16%**           | f(Δ) = 0.0 → điểm = 0 bất kể ERS               |    **0!**     |

### Mục tiêu

- **Thực tế:** **20-25 điểm** (nếu chunked prefill hoặc FP8 hoạt động)
- **Stretch:** **30+ điểm** (tối ưu cả TTFT + TPOT)
- **Worst case:** **16-18 điểm** (chỉ tuning tham số cơ bản)
- **Cảnh báo FP8:** Luôn giữ **BF16 backup** sẵn sàng. Kiểm tra `accuracy_drop` sau mỗi lần submit FP8.

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
