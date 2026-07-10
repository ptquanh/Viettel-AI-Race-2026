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
**Chiến lược:** Submit-as-Test (max 15 submit/ngày, không có local GPU tương đương).

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

Mỗi submission trên portal BTC = 1 lượt test. Tối đa **15 submit/ngày**, cooldown 600s.

### Quy định của BTC về độ biến động (Variance)

> 💡 **Thông tin từ BTC:** Đối với các bài thi tính toán hiệu năng, BTC đã cấu hình hệ thống bench để duy trì mức sai số **< 2%**. Ở mỗi lượt submission, kết quả của các đội được **lấy trung bình từ tối thiểu 3 lần chấm** để đảm bảo tính ổn định. Do đó:
>
> - **KHÔNG cần tốn slot chạy đối chứng (Reference)** hàng ngày để đo độ biến động.
> - Tiết kiệm được tối đa số slot để thử nghiệm trực tiếp các tham số tối ưu mới.

### Nguyên tắc TUYỆT ĐỐI (Rút kinh nghiệm sau 32 lần submit)

1. **Kỷ luật đơn biến NGHIÊM NGẶT:** Mỗi submit chỉ thay đổi **DUY NHẤT 1 tham số** so với cấu hình chạy thành công gần nhất. **KHÔNG BAO GIỜ** thay đổi 2+ biến cùng lúc (ngoại trừ các combo exploit đã lập kế hoạch).
2. **Luôn dùng image gốc BTC** `vllm/vllm-openai:v0.22.1` làm mốc gốc cho đến khi chứng minh được flag hoạt động.
3. **`--max-model-len` ≥ 65536** (tuyệt đối không dùng 8192 hay 32768 để tránh crash hoặc giảm RadixAttention performance).
4. **Ghi chép:** Mỗi submit → `HHMM-docker-compose.yml` + `HHMM-result.md` trong `submissions/DDMMYYYY/`.

#### 🚫 Danh sách cờ / tham số BỊ CẤM TUYỆT ĐỐI

Dựa trên thực tế 32 lần chạy thử nghiệm, các flag/cấu hình sau đây bị cấm tuyệt đối do gây crash, timeout hoặc giảm điểm nghiêm trọng:

- ❌ `--max-model-len < 65536` (Gây crash do không đủ context chứa các prompts dài 20k-42k tokens).
- ❌ `--kv-cache-dtype=fp8` / `fp8_e4m3` (STT17: sụt -5.54 điểm, TTFT +43%, GPQA -9%).
- ❌ `--max-num-batched-tokens < 4096` (STT30/31: trị số thấp gây nghẽn prefill hoặc crash engine).
- ❌ `--max-num-seqs <= 64` (STT10: giới hạn concurrency quá thấp làm sụt điểm còn 2.64).
- ❌ `--enforce-eager` (STT22: Tắt CUDA graphs gây nghẽn CPU nặng dẫn tới timeout 2700s).
- ❌ `--num-scheduler-steps` (STT20: flag chưa được hỗ trợ, gây lỗi exited 2).
- ❌ `--swap-space` (STT32: flag đã bị loại bỏ hoàn toàn trong phiên bản vLLM mới của hệ thống chấm, gây lỗi exited 2).
- ❌ `--disable-log-requests` (Sai tên flag, tên đúng là `--no-enable-log-requests`).
- ❌ Các biến môi trường: `VLLM_USE_V1=1`, `VLLM_ENABLE_V1_MULTIPROCESSING=0`, `OMP_NUM_THREADS=1` (STT23: giới hạn luồng CPU làm giảm hiệu năng).
- ❌ Docker image: `vllm/vllm-openai:v0.4.2` (gây lỗi không khởi động được container).
- ❌ `--block-size=32` (STT33: tăng phân mảnh KV cache, TTFT P50 +11%, giảm điểm).
- ❌ `--performance-mode` (STT34: chế độ interactivity gây hàng đợi prefill nặng khi có concurrency cao, TTFT P50 +125ms, giảm điểm).
- ❌ `--max-num-batched-tokens` khác 512 (STT30: 1024 sụt còn 7.22đ; STT31: 256 gây crash; STT35: 32768 gây nghẽn prefill hàng đợi nghiêm trọng, TTFT P50 +4.1s; STT38: 24576 + seq 96 gây crash/OOM).
- ❌ `--no-enable-prefix-caching` (STT39: tắt prefix caching gây timeout >2700s do phải prefill lại toàn bộ ~3.6 triệu tokens).
- ❌ `--compilation-config` với các chế độ `FULL` hoặc `FULL_DECODE_ONLY` (STT36/37: không cải thiện TPOT 51ms, tăng nhẹ TTFT).
- ❌ `--max-num-seqs` khác mặc định (STT10/25/26/38: đều làm giảm điểm hoặc crash hệ thống).

#### ✅ Danh sách cờ AN TOÀN / KHẢ DỤNG đã xác minh

- ✅ `--quantization=fp8` (Giảm dung lượng model weights, cải thiện lớn tốc độ).
- ✅ `--enable-chunked-prefill` (Chunk prefill tối ưu hóa lập lịch với mặc định `--max-num-batched-tokens=512`).
- ✅ `--no-enable-log-requests` (Giảm CPU logging overhead).
- ✅ `--enable-prefix-caching` (**BẮT BUỘC - SỐNG CÒN**, tắt đi gây timeout >2700s).
- ✅ `--block-size 16` (Kích thước KV Cache block mặc định và tối ưu nhất).
- ✅ `--max-seq-len-to-capture` (Tăng kích thước bắt CUDA Graphs).
- ✅ `--max-model-len=262144` (Giới hạn tối ưu nhất để chứa các prompt siêu dài).
- ✅ `--gpu-memory-utilization=0.95` (Tận dụng bộ nhớ VRAM tối đa an toàn).

---

## 2. 🎯 Chiến lược Tối ưu — Revised (ưu tiên theo ROI + khả thi)

### 🔴 Phase 0: Flag Discovery (ƯU TIÊN CAO NHẤT)

> **Mục tiêu:** Xác định chính xác flag nào được v0.22.1 hỗ trợ. Mỗi flag test RIÊNG LẺ trên baseline config.

| Flag cần xác minh             |      Đã test đúng cách?      | Kế hoạch / Kết quả                                                               |
| :---------------------------- | :--------------------------: | :------------------------------------------------------------------------------- |
| `--enable-chunked-prefill`    | ✅ Đã test đúng cách (STT16) | **Hoạt động tốt, cải thiện TTFT (+0.52 điểm)**                                   |
| `--kv-cache-dtype fp8`        | ✅ Đã test đúng cách (STT17) | **Hoạt động nhưng suy giảm nặng (-5.54 điểm), sụt GPQA 9%**                      |
| `--quantization fp8`          |      ❌ Chưa từng test       | **Test trên baseline image**                                                     |
| `--num-scheduler-steps N`     | ✅ Đã test đúng cách (STT20) | ❌ **Không được hỗ trợ (exited 2)**                                              |
| `--disable-log-requests`      | ✅ Đã test đúng cách (STT18) | ❌ **Sai tên flag. Flag đúng là `--no-enable-log-requests` (STT19: +0.19 điểm)** |
| `--enforce-eager`             |      ❌ Chưa từng test       | **Test trên baseline image**                                                     |
| `OMP_NUM_THREADS=1` (env var) |      ❌ Chưa từng test       | **Test trên baseline image**                                                     |

### 🔴 Phase 1: Giảm TTFT (Impact cao nhất — nếu flag khả dụng)

| Hướng tối ưu                                     | Cơ chế                                                       | Kỳ vọng               | Ưu tiên |
| :----------------------------------------------- | :----------------------------------------------------------- | :-------------------- | :-----: |
| **Chunked Prefill** (`--enable-chunked-prefill`) | Chia nhỏ prefill, xen kẽ decode → giảm head-of-line blocking | Giảm TTFT P95 đáng kể |  🔴 P0  |
| **FP8 Quantization** (`--quantization fp8`)      | Giảm 50% model weight → prefill nhanh hơn                    | Giảm TTFT 20-30%      |  🔴 P0  |

### 🟠 Phase 2: Tối ưu Scheduling & Tham số (nếu Phase 1 không đủ)

| Hướng tối ưu                                | Cơ chế                                                  | Kỳ vọng              | Ưu tiên |
| :------------------------------------------ | :------------------------------------------------------ | :------------------- | :-----: |
| **`--gpu-memory-utilization` tuning**       | Tìm sweet spot (0.95 vs 0.98)                           | Minor                |  🟠 P1  |
| **`--max-model-len` tuning** (65536, 49152) | Giảm metadata overhead, giải phóng VRAM cho KV cache    | Có thể cải thiện nhẹ |  🟠 P1  |
| **`--no-enable-log-requests`**              | Giảm CPU overhead (3 cores rất hạn chế)                 | Minor                |  🟠 P1  |
| **`--enforce-eager`**                       | Tắt CUDA graphs → giảm VRAM overhead, trade-off latency | Cần xác minh         |  🟠 P1  |
| **CPU Thread Limits** (`OMP_NUM_THREADS=1`) | Tránh thrashing 3 cores                                 | Ổn định hoá          |  🟠 P1  |

### 🟢 Phase 3: Alternative Framework (Bị cấm / Không hỗ trợ)

Hệ thống grader chấm bài tự động ép buộc cấu hình chạy của vLLM và không tương thích các serving engine khác như SGLang, LMDeploy, Aphrodite, v.v. Tất cả các nỗ lực chuyển đổi framework đều dẫn đến lỗi khởi chạy hoặc chấm điểm thất bại. Do đó, Phase 3 được điều chuyển hoàn toàn sang tối ưu hóa sâu backend attention (như FlashInfer) và scheduler của vLLM.

### ❌ DANH SÁCH CẤM (đã chứng minh thất bại hoặc crash)

| Cấu hình                          | Lý do cấm                                                                       | Bằng chứng            |
| :-------------------------------- | :------------------------------------------------------------------------------ | :-------------------- |
| `--max-model-len=8192`            | Input trace dài 20k-42k tokens, gây crash/transport error                       | STT2,3,6,8,9          |
| `--num-scheduler-steps=N`         | Gây lỗi khởi động `unrecognized arguments`                                      | STT20                 |
| `--disable-log-requests`          | Gây lỗi khởi động (dùng sai tên flag, dùng `--no-enable-log-requests` thay thế) | STT18                 |
| `--kv-cache-dtype=fp8`            | Gây sụt giảm nặng hiệu năng (-5.54 điểm) và giảm GPQA 9%                        | STT17                 |
| `--max-num-seqs=32` hoặc quá thấp | Giết throughput                                                                 | STT10: 2.64 điểm      |
| `--max-num-seqs=256` hoặc quá cao | Overhead scheduler                                                              | STT11: 14.14 điểm     |
| `--max-num-batched-tokens=1024`   | Nghẽn pipeline                                                                  | STT14: 5.21 điểm      |
| `vllm/vllm-openai:v0.4.2`         | Phiên bản cũ, không tương thích                                                 | STT13,15: crash       |
| `VLLM_USE_V1=1`                   | V1 engine không ổn định trên v0.22.1                                            | STT5: crash           |
| Thay đổi ≥2 biến cùng lúc         | Không xác định được nguyên nhân khi fail                                        | 9/15 submissions fail |

---

## 3. 📝 Nguyên tắc sử dụng 15 Slot/Ngày

Với việc BTC nâng hạn mức lên **15 submit/ngày**, chúng ta có thể đẩy nhanh tốc độ thử nghiệm gấp 3 lần bằng cách phân bổ tài nguyên theo cơ cấu:

| Nhóm Slots          | Số lượng | Nội dung thử nghiệm                       | Cách áp dụng                                                  |
| :------------------ | :------: | :---------------------------------------- | :------------------------------------------------------------ |
| **Flag Discovery**  | 3 slots  | Thử nghiệm các flag tối ưu mới (đơn biến) | Add 1 flag lạ vào Baseline để xem hệ thống có chạy được không |
| **Grid Search A**   | 3 slots  | Khảo sát tham số `max-model-len`          | Test các mốc (49152, 65536, 131072) để tìm điểm tối ưu        |
| **Grid Search B**   | 3 slots  | Khảo sát tham số `gpu-memory-utilization` | Test các mốc (0.90, 0.92, 0.98) để tìm điểm tối ưu            |
| **Combo / Exploit** | 6 slots  | Kết hợp các biến thắng từ 3 nhóm trên     | Ghép các flag và tham số tối ưu đã được xác minh hoạt động    |

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

#### Ngày 06/07 — Flag Discovery & Parameter Grid Search (15 Slots)

> Kết quả thực tế của 5 slots thử nghiệm đầu tiên (Image `vllm/vllm-openai:v0.22.1`):

| Slot | Config = Baseline + ...           | Kết quả thực tế & Chỉ số                                                                               | Đánh giá                            |
| :--- | :-------------------------------- | :----------------------------------------------------------------------------------------------------- | :---------------------------------- |
| 1    | + `--enable-chunked-prefill`      | **Thành công (15.78 điểm)**. TTFT P50=667ms, P95=10162ms, TPOT=59ms.                                   | ✅ **Bật mặc định**                 |
| 2    | + `--kv-cache-dtype fp8`          | **Thành công nhưng sụt điểm sâu (10.24 điểm)**. TTFT P50=958ms (+43%), TPOT=71ms (+20%), GPQA drop 9%. | ❌ **CẤM DÙNG** (overhead lớn)      |
| 3    | + `--disable-log-requests`        | **Thất bại (exited 2)**. Lỗi `unrecognized arguments`.                                                 | ❌ **Sai tên flag**                 |
| 4    | + `--no-enable-log-requests`      | **Thành công (15.97 điểm)**. TTFT P50=677ms, P95=10090ms, TPOT=59ms.                                   | ✅ **Bật mặc định**                 |
| 5    | + `--num-scheduler-steps=8`       | **Thất bại (exited 2)**. Lỗi `unrecognized arguments`.                                                 | ❌ **Không được hỗ trợ**            |
| 6    | + `--quantization=fp8`            | **Thành công vọt điểm (18.99 điểm)**. TTFT P50=569ms (-16%), P95=8520ms, TPOT=51ms, GPQA drop 1%.      | ✅ **Bật mặc định** (baseline mới)  |
| 7    | + `--enforce-eager`               | **Thất bại (Timeout)**. Vượt quá giới hạn thời gian 2700s.                                             | ❌ **CẤM DÙNG** (nghẽn CPU nặng)    |
| 8    | + `OMP_NUM_THREADS=1` (env)       | **Thành công nhưng giảm điểm (17.33 điểm)**. TTFT P50=624ms, P95=8995ms, TPOT=50ms, GPQA drop 0%.      | ❌ **KHÔNG DÙNG** (tăng TTFT)       |
| 9    | + `--max-model-len=131072`        | **Thành công nhưng giảm điểm sâu (12.74 điểm)**. TTFT P50=739ms, P95=12682ms, TPOT=68ms, GPQA drop 0%. | ❌ **CẤM HẠ CONTEXT** (tụt cache)   |
| 10   | + `--max-num-seqs=256`            | **Thành công nhưng giảm điểm (17.82 điểm)**. TTFT P50=618ms, P95=8390ms, TPOT=51ms, GPQA drop 4%.      | ❌ **KHÔNG DÙNG** (tăng TTFT)       |
| 11   | + `--max-num-seqs=128`            | **Thành công nhưng giảm điểm (17.71 điểm)**. TTFT P50=618ms, P95=8497ms, TPOT=51ms, GPQA drop 0%.      | ❌ **KHÔNG DÙNG** (tăng TTFT)       |
| 12   | + `--gpu-memory-utilization=0.90` | **Thành công nhưng giảm điểm (17.58 điểm)**. TTFT P50=627ms, P95=8739ms, TPOT=51ms, GPQA drop 0%.      | ❌ **KHÔNG DÙNG** (giảm cache pool) |
| 13   | + `--gpu-memory-utilization=0.92` | **Thành công nhưng giảm điểm (18.07 điểm)**. TTFT P50=609ms, P95=8488ms, TPOT=51ms, GPQA drop 0%.      | ❌ **KHÔNG DÙNG** (giảm nhẹ cache)  |
| 14   | + `--gpu-memory-utilization=0.98` | **Thành công nhưng giảm điểm (18.24 điểm)**. TTFT P50=614ms, P95=8603ms, TPOT=51ms, GPQA drop 0%.      | ❌ **KHÔNG DÙNG** (VRAM overhead)   |

> **Kết luận thử nghiệm ngày 06/07:** Cấu hình tốt nhất vẫn giữ nguyên là **STT21 (18.99 điểm)** với các cờ: Baseline + `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8` + `--gpu-memory-utilization=0.95`. Tất cả các điều chỉnh đơn biến xung quanh (max-model-len, max-num-seqs, gpu-memory-utilization khác) đều làm giảm hiệu năng.

#### Ngày 07/07 — Deep Parameters Tuning & Combo Exploit (15 Slots)

> Thử nghiệm chuyên sâu các tham số điều phối luồng để ép trễ giải mã (TPOT) và tăng số request pass SLO, kết hợp với cấu hình Best Config mới làm nền tảng (STT21 = Baseline 18.99).

| Slot | Cấu hình = Best Config + ...                                                                      | Kết quả thực tế & Chỉ số                                                     | Đánh giá                                   |
| :--- | :------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------- | :----------------------------------------- |
| 1    | + `--max-num-batched-tokens=1024`                                                                 | **Sụt điểm thảm hại (7.22 điểm)**. TTFT P50=2145ms, P95=11893ms, TPOT=56ms.  | ❌ **CẤM TĂNG NHẸ** (prefill chặn decode)  |
| 2    | + `--max-num-batched-tokens=256` (Mới)                                                            | **Thất bại (Engine crash)**. Lỗi `Engine core initialization failed`.        | ❌ **CẤM DÙNG** (lỗi khởi động engine)     |
| 3    | + `--swap-space=0`                                                                                | **Thất bại (Unrecognized flag)**. Lỗi `unrecognized arguments: --swap-space` | ❌ **CẤM DÙNG** (flag đã bị loại bỏ)       |
| 4    | + `--block-size=32`                                                                               | **Giảm điểm (17.23đ)**. TTFT P50=632ms, P95=8430ms, TPOT=51ms.               | ❌ **CẤM DÙNG** (KV fragmentation)         |
| 5    | + `--performance-mode=interactivity`                                                              | **Giảm điểm (16.33đ)**. TTFT P50=694ms, P95=8301ms, TPOT=51ms.               | ❌ **CẤM DÙNG** (tăng scheduling overhead) |
| 6    | + `--max-num-batched-tokens=32768`                                                                | **Giảm điểm (16.73đ)**. TTFT P50=4674ms, P95=9988ms, TPOT=32ms.              | ❌ **CẤM DÙNG** (nghẽn prefill hàng đợi)   |
| 7    | + `--compilation-config='{"cudagraph_mode":"FULL","max_cudagraph_capture_size":256}'`             | **Giảm điểm (17.78đ)**. TTFT P50=605ms, P95=8929ms, TPOT=51ms.               | ❌ **CẤM DÙNG** (compile overhead)         |
| 8    | + `--compilation-config='{"cudagraph_mode":"FULL_DECODE_ONLY","max_cudagraph_capture_size":256}'` | **Giảm điểm (18.24đ)**. TTFT P50=601ms, P95=8426ms, TPOT=51ms.               | ❌ **CẤM DÙNG** (không cải thiện TPOT)     |
| 9    | + `--max-num-batched-tokens=24576` + `--max-num-seqs=96` (Slot 9b)                                | **Thất bại (Chấm điểm thất bại)**. Gặp lỗi 119/120 transport errors.         | ❌ **CẤM DÙNG** (lỗi crash/OOM)            |
| 10   | Baseline + `--no-enable-prefix-caching` (Test ngược)                                              | **Thất bại (Timeout)**. Vượt quá giới hạn thời gian 2700s của hệ thống.      | ❌ **CẤM TẮT** (công nghệ sống còn)        |
| 11   | Khảo sát SGLang FP8 (`lmsysorg/sglang:v0.4.6.post1` + FP8)                                        | **Thất bại (Startup Timeout)**. Image SGLang quá nặng gây lỗi pull timeout.  | ❌ **CẤM DÙNG** (lỗi pull image)           |
| 12   | STT21 Verification Run #1 (Baseline 18.99đ)                                                       | **Giảm điểm nhẹ (17.89đ)**. TTFT P50=621ms, P95=8416ms, TPOT=51ms.           | Đạt độ ổn định, passed SLO 85/120          |
| 13   | STT21 Verification Run #2 (Baseline 18.99đ)                                                       | **Giảm điểm nhẹ (18.09đ)**. TTFT P50=608ms, P95=8247ms, TPOT=51ms.           | Đạt độ ổn định, passed SLO 86/120          |
| 14   | STT21 Verification Run #3 (Baseline 18.99đ)                                                       | **Giảm điểm nhẹ (17.05đ)**. TTFT P50=642ms, P95=9260ms, TPOT=51ms.           | Đạt độ ổn định, passed SLO 80/120          |
| 15   | STT21 Verification Run #4 (Dự phòng)                                                              | Chạy lặp lại cấu hình tốt nhất để tính trung bình và lấy median an toàn      | TBD                                        |

#### Ngày 08-09/07 — SGLang & LMDeploy Exploration (30 Slots)

**Phát hiện cực kỳ quan trọng về Grader của BTC:**

- Grader **bỏ qua hoàn toàn cấu hình `entrypoint`** trong `docker-compose.yml` của thí sinh và áp đặt lệnh khởi động vLLM.
- Các thử nghiệm hijack để chạy Aphrodite, SGLang, LMDeploy đều **Thất bại hoàn toàn** (lỗi timeout, exit code 126, crash Turbomind RPC).
- **Kết luận:** Hệ thống chấm điểm chỉ tương thích với vLLM. Dừng toàn bộ các thử nghiệm liên quan đến framework khác.

| Slot | Tên thử nghiệm        | Cấu hình & Mô tả                                                          | Kết quả thực tế        | Bài học & Hành động tiếp theo                                                                 |
| ---- | --------------------- | ------------------------------------------------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------- |
| 1-6  | Framework Exploration | Thử nghiệm Aphrodite, SGLang, LMDeploy qua các phiên bản hijack khác nhau | **Thất bại hoàn toàn** | Các framework khác không tương thích với grader của BTC. Quay lại tập trung tối ưu vLLM 100%. |

#### Ngày 10-12/07 — Chiến dịch đột phá TPOT & Chuẩn hóa vLLM (45 Slots)

**Phân tích cổ chai:** Chỉ số TPOT (Time-Per-Output-Token) hiện tại của model Qwen3.5-2B là ~51ms, vượt ngưỡng trần (ceiling) 45ms nên phần điểm TPOT (chiếm 50% tổng trọng số) đang bị **0 điểm**. Mục tiêu ngày 10/07 là giảm TPOT xuống dưới 45ms (tốt nhất là tiệm cận 20ms) để mở khóa điểm số.

##### Kế hoạch 15 Slots ngày 10/07/2026:

- **Slot 1 (0818-docker-compose.yml):** Combo FP8 Weights + FP8 KV Cache (image gốc). **Thất bại (10.88 điểm, tbt_median=63ms)** do overhead lượng tử KV Cache quá lớn trên vLLM v0.22.1.
- **Slot 2 (0925-docker-compose.yml):** MTP Speculative Decoding (image gốc). **Thất bại (10.53 điểm, TTFT P50 vọt lên 2.8s)** do overhead verify draft model nghẽn CPU nghiêm trọng trên 3 cores.
- **Slot 3 (0845-docker-compose.yml):** FlashInfer backend via hijack (custom image `vllm-v0.22.1-flashinfer`). Thử nghiệm attention backend tối ưu cho long context.
- **Slot 4 (0900-docker-compose.yml):** CUDA Graph capture size 65k (`--max-seq-len-to-capture=65536` + FP8 weights) để giữ CUDA Graph decode không fallback về eager mode khi context > 8192 (chuỗi thực tế 20k-42k), triệt tiêu CPU overhead.
- **Slot 5:** CUDA Graph capture size 131k (`--max-seq-len-to-capture=131072`).
- **Slot 6:** Combo FlashInfer + CUDA Graph capture 65k.
- **Slot 7:** Combo MTP Speculative + CUDA Graph capture 65k.
- **Slot 8:** Best combo refinement #1
- **Slot 9-15:** Tinh chỉnh các tham số tốt nhất thu được từ Phase 1 & 2 để chốt cấu hình tối ưu.

---

### Tuần 3 (13/07 – 20/07): Fine-tuning nâng cao & Ổn định hóa (15 slots/ngày)

_Mục tiêu: Đưa điểm số tiệm cận mốc mục tiêu 25-30 điểm, kiểm thử diện rộng._

#### Ngày 13-16/07 — Tối ưu hóa cực hạn

- Tiếp tục tinh chỉnh các tham số sâu của framework đã chọn (vLLM).
- Khảo sát độ ổn định của điểm số khi lượng VRAM thay đổi nhẹ.

#### Ngày 17-19/07 — Đánh giá phân phối độ trễ

- Chạy benchmark liên tục để vẽ biểu đồ phân bổ TTFT và TPOT.
- Phân tích nhóm request nào vẫn bị timeout (>1500ms TTFT) để tìm cách khắc phục cá biệt.

#### Ngày 20/07 — Đóng băng Reference Config v4

- Chốt cấu hình ứng cử viên sáng giá nhất cho vòng chung cuộc.

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
| **v0.22.1 không hỗ trợ chunked prefill / FP8** |       TB        | Rất Cao | Ngày 07/07 sẽ xác minh. Nếu fail → chuyển sang tuning tham số vLLM     |
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
