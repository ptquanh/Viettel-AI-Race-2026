---
tags:
  -  #ViettelAIRace2026
  -  #LLM
  -  #Inference_Optimization
  -  #ActionPlan
status: 🚀 Active (Revised v4.1 — Target 90+)
date: 2026-07-03
updated: 2026-07-10
---

# 🗺️ Kế hoạch Hành động Bài 3 (Vòng 1) — Revised v4.1: Mục tiêu 90+ điểm

**Mục tiêu:** Tối ưu hóa inference Qwen/Qwen3.5-2B trên vLLM, đạt ERS ≥ 0.90 (**90+ điểm**, top 3 leaderboard).
**Hạ tầng BTC:** MiG H200 (18GB VRAM / 3 CPU cores / 8GB RAM), CUDA 12.x.
**Deadline:** 30/07/2026 (Còn **20 ngày**).
**Chiến lược:** Submit-as-Test (15 submit/ngày) + Can thiệp sâu vào vLLM engine.
**Leaderboard:** Top 1 = **100đ** | Top 2 = **98.7đ** | Top 3 = **97.8đ** | **Chúng ta = 18.99đ** (cách top ~80 điểm).

---

## 0. 📊 Tình trạng Hiện tại & Chẩn đoán Cổ chai (Ngày 10/07)

### Kết quả tích luỹ: 69 Submissions (03/07 → 10/07)

| Chỉ số                  | Giá trị                                                                           |
| :---------------------- | :-------------------------------------------------------------------------------- |
| **Điểm cao nhất**       | **18.99** (STT 21: FP8 weights + chunked prefill)                                 |
| **Best Config**         | vLLM v0.22.1 + `--quantization=fp8` + prefix caching + `--no-enable-log-requests` |
| **TPOT hiện tại**       | **51ms** (> ceiling 45ms → $s_{tpot} = 0$)                                        |
| **TTFT P50 / P95**      | 611ms / 8.3s                                                                      |
| **Passed SLO**          | 85/120 (35 request bị 0 điểm TTFT)                                                |
| **Accuracy drop**       | 1% (f(Δ) = 1.0, an toàn)                                                          |
| **Submissions đã dùng** | 69/300 (15/ngày × 20 ngày còn)                                                    |

### ⚠️ Chẩn đoán Cổ chai Cốt lõi

> [!CAUTION]
> **50% tổng điểm đang bị 0 tuyệt đối.** TPOT = 51ms > ceiling 45ms → $s_{tpot} = 0$ cho **mọi** 120 request. Điểm 18.99 hiện tại chỉ đến từ thành phần TTFT.

**Nguyên nhân gốc: KV Cache Memory Bandwidth Bottleneck**

Qwen3.5-2B có kiến trúc lai: **18 linear attention** + **6 full attention** layers. Mỗi bước decode phải đọc toàn bộ KV cache của 6 full-attention layers từ HBM:

| Thông số                 | Giá trị                                                 |
| :----------------------- | :------------------------------------------------------ |
| KV bytes/token/layer     | 2 × 256 (head_dim) × 2 (kv_heads) × 2 bytes = **2,048** |
| Số full-attention layers | **6**                                                   |
| KV bytes/token tổng      | 6 × 2,048 = **12,288 bytes (12 KB)**                    |
| Context trung bình       | ~**30,000** tokens                                      |
| Concurrent sequences     | ~**86** (= passed_slo hiện tại)                         |
| **Tổng KV reads/step**   | 86 × 30k × 12KB = **~31 GB**                            |
| Bandwidth MiG H200       | ~**685 GB/s** (1/7 of full H200)                        |
| **Thời gian đọc KV**     | 31GB / 685 GB/s = **~46ms**                             |
| + Model weights (FP8)    | 2GB / 685 GB/s = **~3ms**                               |
| **Tổng lý thuyết**       | **~49ms** (thực tế đo: 51ms ✅)                         |

> [!IMPORTANT]
> TPOT bị giới hạn bởi **vật lý băng thông HBM**. Không có flag/scheduler/attention backend nào phá vỡ được. Đòn bẩy DUY NHẤT: **giảm tổng lượng KV reads mỗi bước decode**.

---

## 1. 🧮 Phân tích Toán học — Con đường đến 70+ điểm

### Công thức tính điểm chi tiết

$$Score = 100 \times \frac{1}{120} \sum_{i=1}^{120} \left[ 0.5 \cdot s_{ttft,i} + 0.5 \cdot s_{tpot,i} \right] \times f(\Delta)$$

Với: $s_{ttft} = \text{clamp}\left(\frac{1500 - TTFT}{1400}, 0, 1\right)^2$ và $s_{tpot} = \text{clamp}\left(\frac{45 - TPOT}{25}, 0, 1\right)^2$

### Bảng tra cứu nhanh $s_{tpot}$

| TPOT (ms)  | 20   | 22   | 25   | 28   | 30   | 35   | 40   | ≥45  |
| :--------- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $s_{tpot}$ | 1.00 | 0.85 | 0.64 | 0.46 | 0.36 | 0.16 | 0.04 | 0.00 |

### Bảng tra cứu nhanh $s_{ttft}$

| TTFT (ms)  | 100  | 200  | 300  | 400  | 500  | 700  | 1000 | 1200 | ≥1500 |
| :--------- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---- |
| $s_{ttft}$ | 1.00 | 0.86 | 0.73 | 0.62 | 0.51 | 0.33 | 0.13 | 0.05 | 0.00  |

### 🕵️ Tình báo Cạnh tranh — Reverse-Engineering Top Teams

> [!CAUTION]
> **Top 1 đạt 100 điểm = ERS = 1.0 = TTFT ≤ 100ms VÀ TPOT ≤ 20ms cho TẤT CẢ 120 requests.**
> Đây là thông tin tình báo thay đổi hoàn toàn chiến lược. Mức 70 điểm là KHÔNG ĐỦ cạnh tranh.

**Phân tích ngược từ điểm số 100:**

| Yêu cầu cho 100 điểm               | Ý nghĩa kỹ thuật                                                  | Khả thi trên MiG H200?                        |
| :--------------------------------- | :---------------------------------------------------------------- | :-------------------------------------------- |
| TTFT ≤ 100ms cho 42k-token request | Prefix cache phải cover gần hết input, chỉ prefill < 2k token mới | ✅ Nếu multi-turn cùng conversation chain     |
| TPOT ≤ 20ms với 120 concurrent     | KV reads ≤ 13.7 GB/step (120 × 30k × 12KB = 43GB → phải giảm 3x)  | ❌ Với BF16 KV. ✅ Với INT4 KV (43GB → ~11GB) |
| Accuracy drop ≤ 10%                | Quantization không ảnh hưởng nhiều                                | ✅ Với FP8 weights (drop ~1%)                 |

**Kết luận: Top teams CHẮC CHẮN đang dùng ít nhất:**

1. **INT4/INT8 Quantized KV Cache** (custom kernel, không phải `--kv-cache-dtype` của vLLM)
   - Lý do: BF16 KV = 12KB/token → INT4 KV = ~3KB/token → giảm 4x bandwidth
   - Khi đó: 120 × 30k × 3KB = ~10.8 GB → TPOT = 10.8/685 + 3ms = **~19ms** ✅
2. **Prefix caching tối đa** — Warmup + trace structure exploitation
   - Trace có multi-turn conversations. Turn N+1 chứa turn N → prefix cache hit gần hoàn hảo
   - Chỉ cần prefill phần mới (~1-2k tokens) → TTFT ≈ 50-100ms
3. **Custom CUDA/Triton kernels** cho dequantize-on-the-fly KV cache
4. **FP8 weights** (giảm model weight, tăng tốc compute-bound prefill)

### Mô hình dự đoán điểm — CẬP NHẬT

#### Kịch bản A: Batch Size Tuning (Ghost Strategy v3) — _Đang test_

`--max-num-seqs 48` + chunked prefill, BF16 KV:

- TPOT ≈ 28ms → $s_{tpot}$ = 0.46 | TTFT vẫn cao
- **Dự kiến: ~30-34 điểm** ← Bước đệm, KHÔNG PHẢI đích đến

#### Kịch bản B: INT4 KV Cache + Custom Dequant Kernel

Custom Triton kernel dequantize INT4 KV on-the-fly:

- TPOT ≈ 19ms → $s_{tpot}$ = 1.00 với **TẤT CẢ 120 concurrent**
- Không cần giảm `--max-num-seqs` → TTFT không bị hy sinh
- **Dự kiến: ~75-85 điểm** ← Game changer

#### Kịch bản C: INT4 KV + Prefix Cache Warmup + FP8 Weights

Kịch bản B + warmup + prefix caching tối ưu:

- TPOT ≈ 19ms → $s_{tpot}$ = 1.00
- TTFT ≈ 100-300ms (nhờ prefix cache hit) → avg $s_{ttft}$ ≈ 0.73-0.86
- **Dự kiến: ~87-93 điểm** 🎯

#### 🏆 Kịch bản D: Full Stack (Mục tiêu tối đa)

INT4 KV + Custom kernels + Patched scheduler + Warmup + Trace exploitation:

- TPOT ≈ 19-20ms → $s_{tpot}$ ≈ 1.00
- TTFT ≈ 50-150ms (prefix cache gần hoàn hảo) → avg $s_{ttft}$ ≈ 0.86-0.98
- **Dự kiến: ~93-99 điểm** ← 🏆 Top 3 leaderboard

### Tại sao 90+ điểm khả thi?

**Phép tính với INT4 KV Cache:**

- KV reads/step = 120 × 30k × 3KB (INT4) = 10.8 GB → TPOT = 10.8/685 + 3 = **~19ms** → $s_{tpot}$ = 1.0
- Với prefix cache: avg TTFT ≈ 200ms → $s_{ttft}$ = ((1300)/1400)² = **0.86**
- Mỗi request: $S = 0.5 \times 0.86 + 0.5 \times 1.0 = 0.93$
- **Score = 100 × 0.93 × 1.0 = 93 điểm** 🎯

---

## 2. ⚙️ Triết lý Vận hành — Revised v4

### Submit = Test (không có local GPU tương đương)

- BTC đã xác nhận: mỗi lượt submit được lấy trung bình ≥3 lần chấm, sai số < 2%.
- Không cần tốn slot chạy verification. Dành 100% slot cho thử nghiệm.

### Nguyên tắc TUYỆT ĐỐI (Rút kinh nghiệm từ 69 submissions)

1. **Kỷ luật đơn biến** cho flag discovery. Combo chỉ khi các biến đã được xác minh riêng lẻ.
2. **Image gốc `vllm/vllm-openai:v0.22.1`** hoặc custom image dựa trên nó (Ghost Strategy).
3. **`--max-model-len=262144`** — KHÔNG BAO GIỜ giảm (gây hỏng RadixAttention/prefix caching).
4. **`--enable-prefix-caching`** — BẮT BUỘC (tắt → timeout > 2700s, đã chứng minh STT 39).
5. **Framework: Chỉ vLLM** — Grader ép entrypoint vLLM, các framework khác đều fail.
6. **Quantization: Chỉ Online** — Không dùng pre-quantized weights (AWQ/GPTQ checkpoint).

### ✅ Cờ AN TOÀN đã xác minh (Best Config hiện tại)

| Cờ / Tham số                    | Tác dụng                         | Bằng chứng |
| :------------------------------ | :------------------------------- | :--------- |
| `--quantization=fp8`            | Giảm 50% model weights → +3 điểm | STT 21     |
| `--enable-chunked-prefill`      | Xen kẽ prefill/decode            | STT 16     |
| `--no-enable-log-requests`      | Giảm CPU logging overhead        | STT 19     |
| `--enable-prefix-caching`       | Cache system prompt chung        | STT 39     |
| `--gpu-memory-utilization=0.95` | VRAM tối ưu nhất                 | STT 21     |

### 🚫 Cờ BỊ CẤM (đã chứng minh thất bại)

| Cờ                                             | Lý do cấm                                         | Bằng chứng       |
| :--------------------------------------------- | :------------------------------------------------ | :--------------- |
| `--max-model-len < 65536`                      | Crash/truncate input dài 20k-42k tokens           | STT 2,3,6,8,9,24 |
| `--kv-cache-dtype=fp8`                         | Sụt -5.54 điểm, GPQA -9%, overhead chuyển đổi cao | STT 17, 61       |
| `--enforce-eager`                              | Timeout 2700s (nghẽn CPU)                         | STT 22           |
| `--num-scheduler-steps`                        | Unrecognized flag                                 | STT 20           |
| `--swap-space`                                 | Flag đã bị loại bỏ                                | STT 32           |
| `--no-enable-prefix-caching`                   | Timeout > 2700s                                   | STT 39           |
| `--max-num-batched-tokens < 4096`              | Crash engine hoặc nghẽn pipeline                  | STT 30,31        |
| `--performance-mode`                           | Scheduling overhead dưới tải                      | STT 34           |
| `--block-size=32`                              | KV fragmentation                                  | STT 33           |
| `--compilation-config` (FULL/FULL_DECODE_ONLY) | Không cải thiện TPOT 51ms                         | STT 36,37        |
| Docker image `v0.4.2`, `v0.5.2`                | Phiên bản cũ, không tương thích                   | STT 13,15,65     |
| Framework SGLang/LMDeploy/Aphrodite            | Grader ép vLLM entrypoint                         | STT 40,44-54     |
| MTP Speculative Decoding                       | CPU 3 cores quá tải, TTFT +350%                   | STT 50,62        |

---

## 3. 🎯 Chiến lược Tối ưu 6 Tầng (Song song, ưu tiên theo impact)

> [!IMPORTANT]
> **Thay đổi triết lý v4.1:** INT4 KV Cache + Custom Kernel là **CON ĐƯỜNG DUY NHẤT** đến 90+ điểm. Batch size tuning (Tầng 1) chỉ là bước đệm. Mọi effort phải hướng đến Tầng 0 ngay lập tức.

### 🔥 Tầng 0: INT4 Quantized KV Cache + Custom Dequant Kernel (ƯU TIÊN SỐ 1 — BẮT ĐẦU NGAY)

**Mục tiêu:** Giảm KV cache bandwidth 4x → TPOT từ 51ms xuống ~19ms mà KHÔNG cần giảm `--max-num-seqs`.
**Dự kiến đóng góp:** **+50 đến +70 điểm** (game changer lớn nhất).
**Khả thi trên BTC:** ✅ Mục 3 cho phép "Custom CUDA/Triton kernels", "KV cache quantization (FP8, INT8)".

**Cơ chế:**

- Thay vì dùng `--kv-cache-dtype=fp8` của vLLM (chậm do overhead conversion tầng Python), viết **custom Triton kernel** đọc KV cache INT4 và dequantize trực tiếp trong registers GPU.
- BF16 KV = 12KB/token → INT4 KV = ~3KB/token (giảm 4x)
- Tổng KV reads: 120 × 30k × 3KB = 10.8 GB → 10.8/685 = **16ms** + 3ms weights = **19ms TPOT**

**Triển khai:**

1. **Monkey-patch vLLM's PagedAttention kernel** để lưu KV ở INT4 thay vì BF16.
2. Viết **Triton fused attention kernel** với dequantize-on-the-fly: load INT4 → dequant to BF16 in registers → compute attention.
3. Sử dụng per-channel/per-head quantization scales (FP16) để duy trì accuracy.
4. Bake vào custom Docker image, inject qua hijack script.

**Rủi ro:** Accuracy drop do INT4 KV. Giải pháp: test ngay, nếu drop > 10% → dùng INT8 KV (vẫn giảm 2x bandwidth, TPOT ~30ms).

---

### 🔴 Tầng 1: Batch Size Optimization (Tuần 2 — ĐANG CHẠY, bước đệm)

**Mục tiêu:** Mở khóa $s_{tpot}$ ngay lập tức trong khi chờ Tầng 0 sẵn sàng. Bằng cách giảm `--max-num-seqs`.
**Dự kiến đóng góp:** +12 đến +25 điểm.

| Cấu hình                  | TPOT dự kiến | $s_{tpot}$ | Trade-off TTFT             |
| :------------------------ | :----------- | :--------- | :------------------------- |
| `--max-num-seqs 64`       | ~37ms        | 0.10       | Nhẹ (nhiều request vẫn OK) |
| **`--max-num-seqs 48`** ★ | ~28ms        | 0.46       | Vừa phải (SLO giảm ~12%)   |
| `--max-num-seqs 32`       | ~20ms        | 1.00       | Nặng (SLO giảm ~35-40%)    |

Kết hợp bắt buộc: `--enable-chunked-prefill` + `--max-num-batched-tokens 2048` để cứu TTFT.

**Trạng thái:** Grid search 4 điểm đang chạy (Slot 6-9 ngày 10/07).

---

### 🔴 Tầng 2: Custom Entrypoint & Warmup (Tuần 2 — BẮT ĐẦU NGAY)

**Mục tiêu:** Giảm TTFT cho wave đầu tiên bằng cách pre-warm prefix cache.
**Dự kiến đóng góp:** +3 đến +5 điểm.

**Cơ chế:**

- Trace có **1 system prompt chung** cho tất cả 120 requests.
- Nếu prefix cache đã warm trước khi benchmark bắt đầu, request đầu tiên (và tất cả sau đó) sẽ skip prefill cho phần system prompt (~10k tokens), giảm TTFT ~30-40% cho mỗi request.

**Triển khai:**

1. Trong script hijack (`python3_hijack`), **sau khi vLLM server khởi động xong** (healthcheck pass), gửi 1 dummy request chứa system prompt để trigger prefix caching.
2. Dummy request phải đủ nhỏ để không tốn nhiều thời gian (<5 giây).
3. Grader sẽ gọi API sau khi healthcheck pass → prefix cache đã sẵn sàng.

**Rủi ro & Giải pháp:**

- Nếu grader gọi ngay khi healthcheck pass mà không chờ warmup xong → Tạo healthcheck endpoint riêng, chỉ trả `200 OK` sau khi warmup hoàn tất.
- Nếu warmup tốn quá nhiều thời gian → Timeout startup. Giới hạn warmup ≤ 30 giây.

**Khả thi trên BTC:** ✅ Cho phép. BTC cho phép custom Docker image và entrypoint script. Warmup là kỹ thuật tiêu chuẩn trong production.

---

### 🟠 Tầng 3: Custom Triton/CUDA Kernels (Tuần 2-3 — BẮT ĐẦU SONG SONG)

**Mục tiêu:** Tăng tốc prefill 20-30% để giảm TTFT, đồng thời tối ưu decode.
**Dự kiến đóng góp:** +10 đến +20 điểm.

**Phạm vi BTC cho phép:** ✅ Mục 3 (Optimization Scope) ghi rõ: _"Viết custom CUDA/Triton kernels; Tích hợp Fused attention kernels (FlashAttention, FlashInfer)"_.

#### 3a. Fused GQA Attention Kernel cho Qwen3.5-2B

Qwen3.5-2B có cấu hình GQA đặc biệt: `num_attention_heads=16`, `num_key_value_heads=2`, `head_dim=256`. Đây là ratio 8:1, rất phù hợp để viết kernel chuyên biệt:

- **Triton kernel fused** cho GQA 8:1 decode attention:
  - Load 1 KV head, broadcast cho 8 query heads trong shared memory
  - Giảm số lần đọc HBM gấp 8 lần so với naive implementation
  - Tối ưu tile size cho head_dim=256 trên H200 (Hopper architecture)

- **Fused RoPE + Attention kernel:**
  - Gộp rotary position embedding vào attention kernel
  - Tiết kiệm 1 round-trip HBM read/write

#### 3b. Prefill Kernel tối ưu cho Long Context

- Chunked prefill hiện tại trong vLLM chia nhỏ prefill thành chunks nhưng mỗi chunk vẫn dùng generic kernel.
- Custom kernel: **Fused chunked prefill** với paged KV cache write — giảm overhead memory allocation.
- **Flash Decoding v2** pattern: chia context dài thành sub-tiles, tính attention song song trên nhiều SMs, merge kết quả. Đặc biệt hiệu quả cho context 30k-42k tokens.

#### 3c. Linear Attention Optimization

- 18 linear attention layers chiếm 75% model nhưng không cần KV cache.
- Kiểm tra xem vLLM v0.22.1 có tối ưu riêng cho linear attention không.
- Nếu chưa: viết kernel chuyên biệt cho linear attention forward pass (state-space compression).

**Triển khai:**

1. Viết Triton kernels trong custom Docker image.
2. Monkey-patch vào vLLM's attention backend tại runtime (trong hijack script).
3. Test từng kernel riêng lẻ trước khi kết hợp.

---

### 🟠 Tầng 4: Scheduler Patching (Tuần 3 — SAU KHI CÓ BASELINE MỚI)

**Mục tiêu:** Tối ưu phân phối thời gian GPU giữa prefill và decode để cân bằng TTFT/TPOT.
**Dự kiến đóng góp:** +5 đến +10 điểm.

**Phạm vi BTC cho phép:** ✅ Mục 3 ghi: _"Memory-aware scheduling"_, _"Dynamic/Continuous batching"_.

#### 4a. Decode-Priority Scheduling

- Hiện tại vLLM interleave prefill và decode dựa trên `--max-num-batched-tokens`.
- Patch: Ưu tiên **TUYỆT ĐỐI** decode step trước prefill.
- Mỗi iteration: chạy decode cho tất cả active sequences TRƯỚC, rồi mới chạy prefill chunk.
- Lý do: $s_{tpot}$ nhạy cảm hơn $s_{ttft}$ (dải TPOT chỉ có 25ms, dải TTFT có 1400ms).

#### 4b. TTFT-Aware Request Admission

- Patch scheduler để theo dõi thời gian đã chờ (queuing time) của mỗi request.
- Nếu request sắp vượt TTFT ceiling (1500ms) → ưu tiên prefill cho nó ngay.
- Nếu request đã vượt ceiling → giảm ưu tiên (đã 0 điểm, không cần cứu).

#### 4c. Adaptive Batch Size

- Thay vì cố định `--max-num-seqs`, dùng dynamic batch size:
  - Khi queue ngắn (ít request chờ): tăng batch size → cải thiện throughput
  - Khi queue dài (nhiều request chờ): giảm batch size → cải thiện TPOT per request
  - Mục tiêu: luôn giữ TPOT < 30ms mà không hy sinh quá nhiều TTFT

**Triển khai:**

1. Fork/patch file scheduler trong vLLM v0.22.1 (V1 Engine sử dụng C++ core).
2. Nếu C++ core khó patch → inject Python wrapper xung quanh scheduling decisions.
3. Bake vào custom Docker image.

---

### 🟢 Tầng 5: Trace Exploitation & Prefix Caching Maximization (Tuần 2-3)

**Mục tiêu:** Khai thác triệt để cấu trúc trace để TTFT tiệm cận 100ms.
**Dự kiến đóng góp:** +10 đến +20 điểm.

#### 5a. Phân tích cấu trúc Multi-turn trong trace

- Trace có 120 requests với 2-12 messages mỗi request.
- **Giả thuyết quan trọng:** Nhiều request là các turn khác nhau của CÙNG 1 conversation.
- Turn N+1 chứa toàn bộ turn N + thêm 1-2 messages mới.
- Nếu đúng: prefix caching sẽ cover gần 100% input → chỉ prefill phần mới (~1-2k tokens) → TTFT ≈ 50-100ms.

#### 5b. Prefix Cache Warmup Strategy

- Warmup bằng 1 dummy request chứa system prompt → cache sẵn phần chung.
- Nếu trace thực sự có conversation chains → các request sau tự động được cache.

#### 5c. Linear Attention Layer KV Bypass

- 18/24 layers là linear attention → KHÔNG dùng KV cache truyền thống.
- Kiểm tra vLLM v0.22.1 có tối ưu cho trường hợp này chưa.
- Nếu chưa: patch để skip KV cache allocation cho 18 linear layers → tiết kiệm VRAM → chứa thêm KV cache cho 6 full-attention layers.

---

### 🟢 Tầng 6: INT4/INT8 Weight Quantization Online (Tuần 3)

**Mục tiêu:** Giảm model weight size thêm 2-4x so với FP8 → prefill nhanh hơn.
**Dự kiến đóng góp:** +3 đến +8 điểm.

- Khảo sát `--quantization compressed-tensors` hoặc `--quantization bitsandbytes` trên v0.22.1.
- A/B test accuracy drop vs FP8. Chỉ dùng nếu $\Delta \le 10$.

---

## 4. 🗓️ Lộ trình 20 Ngày (10/07 → 30/07) — ALL-IN Sprint

> [!CAUTION]
> **KHẨN CẤP:** Top 1 đã đạt 100 điểm. Chúng ta ở 18.99 điểm — cách top **81 điểm**. Mọi kỹ thuật can thiệp sâu phải bắt đầu **TRONG TUẦN NÀY**. Không có thời gian cho tiến trình tuần tự.

### ✅ Tuần 1 (03/07 – 09/07): HOÀN THÀNH

**Thành quả:**

- Baseline BTC: 15.26 điểm → Best config FP8: 18.99 điểm (+24%).
- Xác minh 15+ flags trên v0.22.1, xây dựng bản đồ tham số đầy đủ.
- Phát hiện Grader ép vLLM entrypoint → chấm dứt thử nghiệm framework khác.
- Phát hiện kỹ thuật Ghost Strategy (hijack script) hoạt động.
- Chẩn đoán cổ chai thực sự: KV cache memory bandwidth, không phải CPU/scheduler.

---

### 🔥 Tuần 2 (10/07 – 16/07): ALL-IN SPRINT — 4 Track Song Song

> **Mục tiêu tuần:** Đạt ≥ **50 điểm** + prototype INT4 KV cache kernel.

#### Track A: Grid Search Batch Size (Ngày 10-11/07) — 20 Slots (Bước đệm)

**Mục tiêu:** Baseline tạm thời ≥ 30 điểm trong khi chờ Tầng 0.

| Ngày  | Slots | Nội dung                                                        |
| :---- | :---: | :-------------------------------------------------------------- |
| 10/07 |  15   | Grid search 4 điểm (seqs 32/48/64 + chunked). **Đang chạy.**    |
| 11/07 |   5   | Tinh chỉnh nhanh quanh winner. Chuyển effort sang Track D ngay. |

**Deliverable:** New Baseline ≥ 30 điểm (bước đệm).

#### Track B: Warmup + Trace Analysis (Ngày 10-11/07) — Không tốn Slot

| Ngày  | Nội dung                                                             |
| :---- | :------------------------------------------------------------------- |
| 10/07 | Phân tích trace: xác định conversation chains, prefix overlap ratio. |
| 11/07 | Build warmup image. Extract system prompt → dummy request.           |

#### Track C: Custom Triton Kernel R&D (Ngày 10-13/07) — Không tốn Slot

| Ngày     | Nội dung                                                                 |
| :------- | :----------------------------------------------------------------------- |
| 10-11/07 | Nghiên cứu vLLM v0.22.1 PagedAttention source code + KV cache layout.    |
| 12/07    | Viết Triton fused GQA decode attention kernel (8:1 ratio, head_dim=256). |
| 13/07    | Tích hợp kernel vào custom image. Test trên 2 slots.                     |

#### 🔥 Track D: INT4 KV Cache Kernel (Ngày 11-16/07) — ƯU TIÊN SỐ 1

> [!IMPORTANT]
> **Đây là con đường duy nhất đến 90+ điểm.** Ưu tiên tuyệt đối.

| Ngày     | Nội dung                                                                        |
| :------- | :------------------------------------------------------------------------------ |
| 11-12/07 | Phân tích KV cache memory layout trong vLLM. Xác định injection point.          |
| 13-14/07 | Viết Triton kernel: INT4 quantize KV khi write, dequantize khi read attention.  |
| 15/07    | Tích hợp vào custom image. Test trên 3-5 slots. Đo TPOT và accuracy.            |
| 16/07    | Nếu INT4 accuracy OK → chốt. Nếu không → fallback INT8 (vẫn 2x bandwidth gain). |

**Deliverable:** INT4/INT8 KV cache kernel → TPOT ≤ 25ms + TTFT không bị hy sinh.

#### Ngày 14-16/07 — Integration Sprint (30 slots)

| Ngày  | Slots | Nội dung                                                       |
| :---- | :---: | :------------------------------------------------------------- |
| 14/07 |  10   | Kết hợp Track A winner + Track B warmup. Đo điểm tổng hợp.     |
| 15/07 |  10   | Test Track D (INT4 KV) lần đầu. Grid search kết hợp.           |
| 16/07 |  10   | Kết hợp tất cả: INT4 KV + Warmup + FP8 weights. Đo điểm combo. |

**Mục tiêu cuối Tuần 2:** ≥ **50 điểm** (Tầng 0 prototype + Tầng 1-2 hoàn thành).

---

### ⚡ Tuần 3 (17/07 – 23/07): TĂNG TỐC ĐỘT PHÁ — Tối ưu INT4 KV + Scheduler

> **Mục tiêu tuần:** Đạt ≥ **80 điểm** (INT4 KV kernel đã ổn định + scheduler patch).

#### Track E: INT4 KV Kernel Polish + Accuracy Tuning (Ngày 17-19/07)

| Ngày  | Slots | Nội dung                                                                         |
| :---- | :---: | :------------------------------------------------------------------------------- |
| 17/07 |  10   | Tinh chỉnh INT4 quantization scales (per-head vs per-channel). A/B accuracy.     |
| 18/07 |  10   | Tối ưu Triton kernel perf: tile sizes, memory coalescing, warp-level primitives. |
| 19/07 |   5   | Mixed INT4/INT8 KV: INT4 cho 4 layers, INT8 cho 2 layers nhạy cảm nhất.          |

#### Track F: Scheduler Patching (Ngày 17-20/07)

| Ngày     | Nội dung                                                          |
| :------- | :---------------------------------------------------------------- |
| 17-18/07 | Decode-priority scheduling + TTFT-aware admission control.        |
| 19-20/07 | Adaptive batch size: dynamic `max-num-seqs` based on queue depth. |

#### Ngày 20-23/07 — Full Stack Integration (60 Slots)

| Ngày  | Slots | Nội dung                                                                  |
| :---- | :---: | :------------------------------------------------------------------------ |
| 20/07 |  15   | Merge ALL: INT4 KV + Custom attention + Scheduler + Warmup + FP8 weights. |
| 21/07 |  15   | Grid search: optimal (num_seqs, batch_tokens, KV quant bits) combo.       |
| 22/07 |  15   | Stability: 5 lần cùng config → variance < 2 điểm.                         |
| 23/07 |  15   | Freeze **Candidate Config v1**. Target: ≥ 80 điểm.                        |

**Mục tiêu cuối Tuần 3:** ≥ **80 điểm** (Tầng 0-4 hoàn thành, tiệm cận top 10).

---

### 🏁 Tuần 4 (24/07 – 30/07): FINAL PUSH — Target Top 3

> **Mục tiêu tuần:** Đạt ≥ **90 điểm** (tinh chỉnh cực hạn + final submission).

#### Ngày 24-26/07 — Micro-optimization & Edge Cases (45 Slots)

| Ngày  | Slots | Nội dung                                                                  |
| :---- | :---: | :------------------------------------------------------------------------ |
| 24/07 |  15   | Micro-tune INT4 KV quantization: per-token scaling, group quantization.   |
| 25/07 |  15   | Trace-specific tuning: optimize for actual request arrival pattern.       |
| 26/07 |  15   | Fused end-to-end pipeline: minimize Python overhead between kernel calls. |

#### Ngày 27-28/07 — Stabilization & Accuracy Audit (20 Slots)

| Ngày  | Slots | Nội dung                                             |
| :---- | :---: | :--------------------------------------------------- |
| 27/07 |  10   | Chạy best config 5 lần. Variance < 2 điểm.           |
| 27/07 |   5   | Accuracy audit: GPQA check, đảm bảo $\Delta \le 10$. |
| 28/07 |   5   | Freeze **Final Config**. Build final Docker image.   |

#### Ngày 29-30/07 — Final Submission

| Ngày  | Slots | Nội dung                                       |
| :---- | :---: | :--------------------------------------------- |
| 29/07 |   3   | Submit Final Config 3 lần → xác nhận lần cuối. |
| 30/07 |   2   | 🏁 **SUBMIT FINAL** trước deadline.            |

---

## 5. 📐 Ước tính Tổng Quỹ Slot & Phân bổ

| Giai đoạn           | Ngày        |  Slots  | Mục đích                                |
| :------------------ | :---------- | :-----: | :-------------------------------------- |
| ✅ Tuần 1 (đã dùng) | 03-09/07    |   69    | Flag discovery + baseline               |
| Tuần 2 ALL-IN       | 10-16/07    |   80    | Batch size + INT4 KV prototype + warmup |
| Tuần 3 BREAKTHROUGH | 17-23/07    |   85    | INT4 KV polish + scheduler + full stack |
| Tuần 4 FINAL PUSH   | 24-30/07    |   70    | Micro-optimization + final submission   |
| **Tổng khả dụng**   | 28 ngày     |   420   |                                         |
| **Đã dùng**         | 8 ngày      |   69    |                                         |
| **Còn lại**         | **20 ngày** | **231** |                                         |

---

## 6. ⚠️ Rủi ro & Giải pháp — Updated v4

| Rủi ro                                                    | Xác suất | Impact  | Giải pháp                                                                  |
| :-------------------------------------------------------- | :------: | :-----: | :------------------------------------------------------------------------- |
| **Custom kernel gây crash/sai kết quả**                   |    TB    | Rất Cao | Test từng kernel riêng lẻ. Giữ backup config không có custom kernel.       |
| **Scheduler patch gây deadlock/timeout**                  |   Thấp   |   Cao   | Test trên slots nhỏ. Rollback về cấu hình Tầng 1-2 nếu fail.               |
| **Warmup tốn quá nhiều thời gian startup**                |   Thấp   |   TB    | Giới hạn warmup ≤ 30 giây. Healthcheck endpoint tùy chỉnh.                 |
| **INT8 online quantization gây accuracy drop > 10%**      |    TB    |   Cao   | Kiểm tra GPQA ngay sau submit. Giữ FP8 làm fallback.                       |
| **`--max-num-seqs` quá thấp → quá nhiều request timeout** |    TB    |   TB    | Kết hợp chunked prefill + warmup để bù đắp. Grid search tìm sweet spot.    |
| **KV bandwidth bottleneck KHÔNG THỂ vượt qua**            |   Cao    |   Cao   | Chấp nhận giới hạn vật lý. Tập trung cải thiện TTFT bằng custom kernel.    |
| **Variance cao do CPU host jitter**                       |   Thấp   |   TB    | BTC đã xác nhận < 2%. Submit 3-5 lần, lấy median.                          |
| **Grader thay đổi healthcheck/entrypoint**                | Rất thấp |   Cao   | Giữ config tương thích ngược (không chỉnh sửa entrypoint gốc, chỉ hijack). |

---

## 7. 📋 Checklist NGHIÊM NGẶT Trước Mỗi Submit

- [ ] **Image:** Dựa trên `vllm/vllm-openai:v0.22.1`? (Custom image OK nếu base là v0.22.1)
- [ ] **Đơn biến:** Chỉ thay đổi **ĐÚNG 1 tham số** so với Reference Config? (Trừ combo đã lên kế hoạch)
- [ ] **max-model-len:** ≥ 262144? (KHÔNG BAO GIỜ giảm)
- [ ] **Không có flag cấm:** Kiểm tra danh sách 🚫 ở trên.
- [ ] **Accuracy check:** Nếu dùng quantization mới → kiểm tra accuracy_drop ≤ 10%.
- [ ] **Đã ghi file:** `submissions/DDMMYYYY/HHMM-docker-compose.yml` + `HHMM-result.md`.
- [ ] Sau khi có kết quả → cập nhật `submissions/logs.md` + plan ngày.
- [ ] Nếu điểm tăng → cập nhật Best Config Reference.

---

## 8. 🧭 Decision Tree — Chọn hướng đi tiếp theo

```
Kết quả Slot 6-9 (Tuần 2)?
├── TPOT < 30ms ĐẠT + Điểm > 30
│   ├── Track B (Warmup) → Kết hợp → Test thêm
│   ├── Track C (Custom Kernel) → Giảm TTFT 20-30%
│   └── Mục tiêu: 45-55 điểm cuối Tuần 2
│
├── TPOT < 30ms ĐẠT + Điểm 20-30 (TTFT quá tệ)
│   ├── Ưu tiên Track C (Custom Kernel) → Cải thiện prefill speed
│   ├── Track D (Scheduler) → Decode-priority
│   └── Mục tiêu: 40-50 điểm cuối Tuần 2
│
├── TPOT VẪN > 40ms (Ghost Strategy fail)
│   ├── Debug: Kiểm tra hijack script có chạy đúng không
│   ├── Fallback: Test trực tiếp trên image gốc (không hijack)
│   └── Pivot: Tập trung 100% vào TTFT optimization
│
└── Container crash / Timeout
    ├── Kiểm tra OOM (8GB RAM constraint)
    ├── Thử `--enforce-eager` trong hijack (tắt CUDA graphs)
    └── Giảm `--gpu-memory-utilization` xuống 0.92
```

---

## 9. 📊 Bảng Theo dõi Mục tiêu Hàng Tuần

| Tuần | Mục tiêu (điểm) | Tầng hoàn thành  | Deliverable chính                              |
| :--- | :-------------: | :--------------- | :--------------------------------------------- |
| 1 ✅ |      18.99      | —                | Best Config FP8 + Flag map                     |
| 2    |    ≥ **50**     | Tầng 0 proto+1+2 | INT4 KV prototype + Batch size + Warmup        |
| 3    |    ≥ **80**     | Tầng 0-4         | INT4 KV stable + Scheduler + Full stack        |
| 4    |  ≥ **90+** 🏆   | Tầng 0-6         | Micro-optimized + Final submission → **Top 3** |

---

## 10. ⚡ Hành động TỨC THÌ (10/07 — Hôm nay)

1. **Tiếp tục Grid Search Batch Size** (Slot 6-9) → Baseline tạm ≥ 30 điểm.
2. **Bắt đầu phân tích vLLM source code** → Tìm KV cache memory layout, PagedAttention kernel.
3. **Phân tích trace structure** → Xác định conversation chains, prefix overlap.
4. **Nghiên cứu INT4 KV quantization** → Tìm paper/implementation reference (vLLM, FlashInfer, TensorRT-LLM).
5. **Đọc source FlashInfer** → Xem có sẵn INT4 KV kernel không (FlashInfer đã hỗ trợ FP8 KV).
