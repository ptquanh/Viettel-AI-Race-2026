# 🗺️ Review Plan Ngày 07/07 – Viettel AI Race 2026
## Revised v4 – sau 32 submissions, Best = 18.99đ (STT21)

tags: #ViettelAIRace2026 #LLM #Inference_Optimization #ActionPlan
date: 2026-07-07
status: 🚀 Active – Critical TPOT breakthrough needed

---

## 0. Tóm tắt tình báo sau 32 submissions

**Best Config hiện tại – STT21 (18.99đ):**
```
vllm/vllm-openai:v0.22.1
--model=/model
--max-model-len=262144
--gpu-memory-utilization=0.95
--tensor-parallel-size=1
--enable-prefix-caching
--enable-chunked-prefill          # +0.52đ (STT16)
--no-enable-log-requests          # +0.19đ (STT19)
--quantization=fp8                # +3.02đ (STT21)  ⭐ GOLDEN FLAG
```
Metrics STT21:
- TTFT P50=569ms (-16% vs baseline), P95=8520ms
- TPOT=51ms
- GPQA drop 1%
- passed_slo: ~ ? (ước ~95-100/120)

**Trace Round1 – phát hiện then chốt:**
- 120 req / 25.5s, bursty 25ms median arrival
- input **78k–167k chars ≈ 20k–42k tokens**
- output **max_tokens=200 fixed, temperature=0, seed đồng nhất**
- 2→12 messages/request, **1 system prompt chung → prefix caching ROI cực cao**
- → `max_model_len` **BẮT BUỘC ≥ 65536**, lý tưởng 262144. 8192 / 32768 / 131072 đều đã fail / tụt điểm.

---

## 1. Phân tích ERS – vì sao mới 18.99đ

`S_request = 0.5 × s_ttft + 0.5 × s_tpot`

- s_ttft = clamp((1500-TTFT)/1400,0,1)²
- s_tpot = clamp((45-TPOT)/25,0,1)²

Với STT21:
- TTFT P50=569ms → s_ttft = ((1500-569)/1400)² = **0.44**
- TPOT=51ms → (45-51) = -6 → **s_tpot = 0**
  → **MẤT TRẮNG 50% trọng số TPOT**

→ Đây là nút thắt #1. Chỉ cần TPOT <45ms:
- 44ms → s_tpot=0.0016
- 35ms → s_tpot=0.16
- 25ms → s_tpot=0.64
- 20ms → s_tpot=1.0

**Kết luận: TPOT 51ms → 35ms = +0.08 S_request trung bình ≈ +8-10 điểm ERS, lớn hơn toàn bộ lợi ích TTFT từ đầu cuộc thi.**

TTFT P95=8520ms vẫn giết 36 req tail >1500ms → s_ttft=0. Cần kéo P95 <1500ms.

---

## 2. Review 32 submissions – bài học cứng

| Flag | Kết quả thực | Bài học |
|---|---|---|
| `--quantization=fp8` | **+3.02đ, TTFT -16%, TPOT 59→51ms** | **GIỮ – baseline mới** |
| `--enable-chunked-prefill` | +0.52đ | GIỮ |
| `--no-enable-log-requests` | +0.19đ | GIỮ |
| `--kv-cache-dtype=fp8` | **-5.54đ, TTFT +43%, GPQA -9%** | CẤM vĩnh viễn |
| `--max-model-len=131072` | -6.25đ, TTFT P95 12682ms | **KHÔNG hạ context – RadixAttention prefix cache vỡ** |
| `--max-model-len=8192/32768` | crash / 15.00đ | CẤM <65536 |
| `--max-num-seqs=32` | **2.64đ** | CẤM thấp |
| `--max-num-seqs=128/256` | 17.71 / 17.82đ (-1.2đ) | default tốt hơn |
| `--max-num-batched-tokens=1024` | **7.22đ** | CẤM giảm |
| `--max-num-batched-tokens=256` | Engine crash | CẤM |
| `--gpu-memory-utilization` 0.90/0.92/0.98 | 17.58 / 18.07 / 18.24đ (đều <18.99) | **0.95 là sweet spot** |
| `--enforce-eager` | Timeout >2700s | CẤM |
| `OMP_NUM_THREADS=1` | 17.33đ (-1.66) | CẤM |
| `--num-scheduler-steps` | exit 2 | CẤM |
| `--swap-space=0` | unrecognized args | CẤM – flag đã bỏ ở v0.22.1 |

**Sai lầm hệ thống:** 9/15 fail đầu là do **đổi >2 biến + max_model_len sai + test flag trên image chưa push**. Từ STT16 đã kỷ luật đơn biến → tỉ lệ pass 10/17 (~59%).

---

## 3. Lỗ hổng chiến lược trong Plan v3 ngày 07/07

Plan hiện tại (Slot 4-15) có 3 vấn đề nghiêm trọng:

1. **Test giảm `max_num_batched_tokens` tiếp** – đã chứng minh thảm họa (1024→7.22đ, 256→crash). Hướng đúng phải là **TĂNG**, vì input 20k-42k tokens >> default batched_tokens (~8192-16384). Prefill bị chunk 3-5 lần → TTFT P95 nổ 8.5s.

2. **Bỏ qua TPOT <45ms breakthrough** – toàn bộ plan 07/07 tập trung TTFT, trong khi s_tpot đang =0. Cần ưu tiên các cờ giảm TPOT: `performance_mode`, CUDA graph capture size, block-size, TPOT-oriented scheduling.

3. **Chưa khai thác prefix caching triệt để** – trace có 1 system prompt chung, 2-12 messages multi-turn, seed đồng nhất. vLLM prefix caching đang bật, nhưng chưa tune: `--enable-prefix-caching` ok, thiếu `--prefix-caching-hash-algo=builtin`, chưa test SGLang RadixAttention (plan 08-09/07 mới test – nên đẩy sớm nếu vLLM TPOT không xuống <45ms).

---

## 4. Kế hoạch 07/07 Revised v4 – 15 slots

**Nền tảng:** STT21 = Best Config 18.99đ
```
--quantization=fp8
--enable-chunked-prefill
--no-enable-log-requests
--max-model-len=262144
--gpu-memory-utilization=0.95
--enable-prefix-caching
```
**Tuyệt đối KHÔNG đổi:** max_model_len, gpu_mem_util, image tag.

### Slot thực tế đã chạy sáng 07/07

| Slot | Đã chạy | Kết quả |
|---|---|---|
| 1 | `--max-num-batched-tokens=1024` | **7.22đ – FAIL** |
| 2 | `--max-num-batched-tokens=256` | **Engine crash** |
| 3 | `--swap-space=0` | **exit 2 – flag removed** |

→ 3 slot mất, còn 12 slot.

### Revised Slot 4–15 (chiều 07/07)

| Slot | Config = STT21 + … | Lý do / Giả thuyết | Kỳ vọng TPOT | Risk |
|---|---|---|---|---|
| **4** | `--block-size=32` | Input 20-42k tokens → block 16 = 1250-2625 blocks/req, overhead paged_attention lớn. 32 giảm 50% metadata, hợp H200. | 51→48ms | Thấp |
| **5** | `--max-seq-len-to-capture=32768` | Default cudagraph capture ~8192. Prompt 20-42k → decode never hit graph → kernel launch overhead cao trên 3 CPU core. Nâng capture lên 32k. | 51→46ms | TB |
| **6** | `--performance-mode=interactivity` | V1: fine-grained CUDA graphs 1…32, latency-oriented kernels. Đúng bài TPOT. | **51→42-44ms** ⭐ | Thấp |
| **7** | `--performance-mode=throughput` | Đối chứng: nếu interactivity thắng → xác nhận TPOT-bound. | 51→49ms | Thấp |
| **8** | `--max-num-batched-tokens=32768` | **ĐẢO CHIỀU**: tăng gấp ~4x default. Cho phép prefill 20-42k tokens trong 1-2 chunk thay vì 5-6. TTFT P95 mục tiêu <3000ms. | TTFT P95 8520→~3500ms | TB |
| **9** | `--max-num-batched-tokens=65536` | Full prefill 1 shot cho 90% requests. | TTFT P95 →~2200ms | TB-Cao VRAM |
| **10** | `--max-num-batched-tokens=32768` **+** `--performance-mode=interactivity` | **Combo #1 – TTFT + TPOT song song**. Ứng viên Final nếu cả 6 & 8 pass riêng lẻ. | TTFT <3500ms, TPOT <45ms | TB |
| **11** | `--block-size=32` **+** `--performance-mode=interactivity` | Combo #2 – low overhead KV + low latency graph | TPOT 40-44ms | Thấp |
| **12** | `--max-seq-len-to-capture=32768` **+** `--performance-mode=interactivity` | Combo #3 – CUDA graph sâu + interactivity | TPOT <43ms | Thấp |
| **13** | `--compilation-config='{"cudagraph_mode":"FULL","max_cudagraph_capture_size":256}'` | Ép FULL graph decode-only, capture_size=256 > output 200 tokens → giảm kernel launch tối đa. Thay thế enforce_eager đã timeout. | TPOT 38-44ms | TB |
| **14** | **Best single + best single** (chọn từ Slot 4-9 winner x2) | Exploit chính thức | Target >22đ | - |
| **15** | **Verify Final Config v2** – repeat Slot 14 | Chốt Reference Config v2, 3 lần submit nếu còn slot dư (BTC avg 3 runs) | Lock 22-26đ | - |

**Thứ tự ưu tiên nếu thiếu slot:**
6 > 8 > 5 > 4 > 10 > 11 > 13 > 9 > 7 > 12

Lý do: Slot 6 (`performance-mode=interactivity`) là **cửa duy nhất để TPOT <45ms trong 1 flag**, ROI = 50% ERS weight. Slot 8 (`max_num_batched_tokens=32768`) là cửa duy nhất cứu TTFT P95 tail.

---

## 5. Các flag CẤM TUYỆT ĐỐI ngày 07/07 (update)

- ❌ `--max-model-len < 65536` (đã 5 lần crash)
- ❌ `--kv-cache-dtype=fp8` / `fp8_e4m3` (STT17 -5.54đ)
- ❌ `--max-num-batched-tokens < 4096` (STT30/31)
- ❌ `--max-num-seqs <=64` (STT10 2.64đ)
- ❌ `--enforce-eager` (STT22 timeout 2700s)
- ❌ `--num-scheduler-steps` (STT20 exit 2)
- ❌ `--swap-space` (STT32 removed flag)
- ❌ `--disable-log-requests` (sai tên, dùng `--no-enable-log-requests`)
- ❌ `VLLM_USE_V1=1`, `VLLM_ENABLE_V1_MULTIPROCESSING=0`, `OMP_NUM_THREADS=1`
- ❌ `vllm/vllm-openai:v0.4.2`
- ❌ Thay >1 biến / submit

**Flag AN TOÀN đã verify trên v0.22.1:**
- ✅ `--quantization=fp8`
- ✅ `--enable-chunked-prefill`
- ✅ `--no-enable-log-requests`
- ✅ `--max-num-batched-tokens` (chỉ TĂNG, không giảm <8192)
- ✅ `--block-size {8,16,32,64,128}`
- ✅ `--performance-mode {balanced,interactivity,throughput}`
- ✅ `--max-seq-len-to-capture`
- ✅ `--compilation-config`

---

## 6. Dự báo điểm

| Kịch bản 07/07 | Điều kiện | ERS ước tính |
|---|---|---|
| **Conservative** | Chỉ block-size + interactivity pass, TPOT 44ms | **21-23đ** |
| **Base case** | interactivity + max_num_batched_tokens=32768 pass | **24-27đ** |
| **Breakthrough** | TPOT <35ms + TTFT P95 <3000ms | **30-34đ** |
| **Worst** | Tất cả slot 4-9 fail / giảm điểm | giữ **18.99đ** (STT21) |

**Floor bảo hiểm:** luôn giữ STT21 compose sẵn sàng re-submit nếu combo crash.

---

## 7. Checklist Submit 07/07 – siết chặt

- [ ] Image = `vllm/vllm-openai:v0.22.1` ?
- [ ] `max_model_len = 262144` ?
- [ ] `gpu_memory_utilization = 0.95` ?
- [ ] Base = STT21 (`--quantization=fp8 --enable-chunked-prefill --no-enable-log-requests`) ?
- [ ] **Chỉ +1 flag mới** ?
- [ ] Flag KHÔNG nằm trong CẤM list ?
- [ ] Đã lưu `submissions/07072026/HHMM-docker-compose.yml` ?
- [ ] Sau result → `HHMM-result.md` + update logs.md + tính s_ttft / s_tpot tay ?
- [ ] Nếu điểm >18.99 → update Reference Config ngay

---

## 8. Đề xuất đẩy nhanh SGLang

Nếu sau Slot 6-8 (interactivity + batched_tokens) mà **TPOT vẫn ≥46ms**, nghĩa là vLLM V1 trên H200 MiG 3 CPU đã chạm trần.

→ **Dời SGLang từ 08-09/07 lên tối 07/07 Slot 14-15**, dùng 2 slot cuối test:
```
# SGLang test nhanh
docker run --gpus all -p 8000:8000 \
  lmsysorg/sglang:latest \
  --model-path /model \
  --quantization fp8 \
  --context-length 65536 \
  --mem-fraction-static 0.90
```
SGLang RadixAttention = prefix caching native mạnh hơn vLLM, rất hợp trace multi-turn shared system prompt. Đây là plan B để phá TPOT <40ms.

---

**Kết luận cho 07/07:**
- STOP test giảm `max_num_batched_tokens`. Đảo chiều TĂNG lên 32768 / 65536.
- Ưu tiên #1: `--performance-mode=interactivity` → cứu TPOT 50% ERS weight.
- Ưu tiên #2: `--max-num-batched-tokens=32768` → cứu TTFT P95 tail.
- Giữ nguyên: max_model_len=262144, gpu_mem=0.95, quantization=fp8, chunked_prefill.
- Mục tiêu cuối ngày: **TPOT <45ms, TTFT P95 <4000ms, điểm ≥24**.

Good luck – 12 slot chiều nay quyết định có vượt mốc 20đ bền vững hay không.
