# 🗺️ Kế hoạch Hành động Tổng thể Vòng 1 — Phase 1 Strategic Master Plan (LiquidAI/LFM2.5)

Tài liệu này đóng vai trò là Bản kế hoạch chiến lược tổng thể (Master Plan) cho Vòng 1 cuộc thi Viettel AI Race 2026, hướng tới mục tiêu tối đa hóa điểm số ERS trên mô hình **LiquidAI/LFM2.5-1.2B-Instruct** và hạ tầng MiG H200 giới hạn.

**Deadline Vòng 1**: 30/07/2026 | **Kỷ lục hiện tại**: 56.79 điểm (17/07/2026) | **Mục tiêu**: 80+ điểm

---

## 1. 🔍 Bối cảnh: Kinh nghiệm Custom Image từ Round 1 (Qwen3.5-2B)

> [!IMPORTANT]
> Đội đã có **kinh nghiệm sâu rộng** xây dựng Custom Docker Image trong Round 1 (Qwen3.5-2B), đạt tới **51.10 điểm** (STT 116). Hạ tầng này có thể **tái sử dụng trực tiếp** cho LFM2.5 ở Round 2.

### Thành tựu Round 1 (Qwen3.5-2B → 51.10 điểm)

| Phiên bản | Kỹ thuật đột phá                            |   TPOT   |   Điểm    |
| :-------: | :------------------------------------------ | :------: | :-------: |
| Ghost v4  | Hijack script + FP8 KV Cache per-token-head |   51ms   |   Fail    |
| Ghost v8  | Custom FP8 KV + Chunk 4096                  |   31ms   |   20.82   |
| Ghost v9  | + Warmup + Custom Kernel + Chunked Prefill  |   22ms   |   39.83   |
| Ghost v10 | + Chunk 16384 + OMP tuning                  |   21ms   |   42.27   |
| Ghost v11 | + Prefix Caching + GPU Mem 0.96             |   22ms   |   42.62   |
| **v11.6** | **+ Seqs 16 → TPOT đạt Floor**              | **16ms** | **51.10** |

### Hạ tầng có sẵn (tái sử dụng được)

- ✅ **Hijack Script** (python3 → python3_real): Ghost Strategy v4-v11
- ✅ **Custom Docker Image pipeline**: Build, push lên Docker Hub (`ptquanh/sandbox-runtime:*`)
- ✅ **Custom CUDA/Triton Kernels**: FP8 KV Cache quantization kernels
- ✅ **Warmup Strategy**: Pre-warm JIT compile + prefix cache
- ✅ **Environment variable injection**: `HIJACK_ENGINE`, `VLLM_*`, `OMP_NUM_THREADS`

### Khác biệt Round 1 vs Round 2

| Yếu tố                  | Round 1 (Qwen3.5-2B)           | Round 2 (LFM2.5-1.2B)            |
| :---------------------- | :----------------------------- | :------------------------------- |
| Kiến trúc               | Transformer thuần (24L GQA)    | **Hybrid Recurrent + Attention** |
| TPOT baseline (stock)   | 51ms                           | **4ms** (đã rất thấp!)           |
| TTFT baseline (stock)   | 670ms                          | **73ms** (đã rất thấp!)          |
| Cổ chai chính           | KV Cache bandwidth (31GB/step) | **Weight reads** (44% TPOT)      |
| TPOT Floor BTC          | 20ms                           | **1ms** (ngặt nghèo hơn 20x!)    |
| TPOT Ceiling BTC        | 45ms                           | **10ms**                         |
| Score tốt nhất          | 51.10                          | **56.79**                        |
| Custom image cần thiết? | Bắt buộc (cần FP8 KV kernel)   | **Cần thiết** (cần INT4 weights) |

> [!NOTE]
> LFM2.5 đã cho điểm cao hơn Qwen3.5 trên **stock image** (56.79 vs 18.99) nhờ kiến trúc recurrent hiệu quả. Nhưng để tiến đến 80+, vẫn cần Custom Image tích hợp các **custom CUDA/Triton kernels** tối ưu recurrent layers và các cấu hình **Online Quantization** tiên tiến.

---

## 2. 📊 Phân tích Khoảng cách & Mục tiêu Điểm số

### Công thức chấm điểm

```
S_request = 0.5 × s_ttft + 0.5 × s_tpot
s_ttft = clamp((400 - TTFT) / 390, 0, 1)²
s_tpot = clamp((10 - TPOT) / 9, 0, 1)²
```

### Bảng mục tiêu TPOT & TTFT cho từng mốc điểm

| Mốc điểm | TPOT cần | s_tpot | TTFT P50 cần | s_ttft |  ERS  | Kỹ thuật cần thiết                          |
| :------: | :------: | :----: | :----------: | :----: | :---: | :------------------------------------------ |
|  **57**  |   4 ms   | 0.444  |    73 ms     | 0.703  | 0.574 | ✅ Đã đạt (Flag tuning FP8 stock image)     |
|  **65**  |   3 ms   | 0.605  |    55 ms     | 0.783  | 0.694 | Custom Image + Custom Kernels               |
|  **75**  |   2 ms   | 0.790  |    55 ms     | 0.783  | 0.787 | Custom Image + Operator Fusion + CUDA Graph |
|  **80**  |   2 ms   | 0.790  |    45 ms     | 0.828  | 0.809 | Custom Image + Custom Kernel + Warmup       |
|  **85**  |  1.5 ms  | 0.891  |    45 ms     | 0.828  | 0.860 | Speculative Decoding / Custom CUDA Kernel   |
| **90+**  |   1 ms   | 1.000  |    30 ms     | 0.900  | 0.950 | Custom Triton Kernels + Flash-Linear-Attn   |

> **Insight**: Giảm TPOT 1ms cho s_tpot tăng rất mạnh (do hàm bậc 2 trên dải 1-10ms). TPOT là đòn bẩy lớn nhất.

---

## 3. 🎯 Chiến lược Tối ưu hóa 3 Giai đoạn (Rút gọn)

> [!TIP]
> Nhờ kinh nghiệm Custom Image từ Round 1, lộ trình được **rút gọn từ 4 giai đoạn xuống 3**, bắt đầu custom image **ngay từ ngày 18/07** thay vì chờ đến ngày 21/07.

### Giai đoạn 1: Flag Tuning trên Stock Image ✅ HOÀN THÀNH (16-17/07)

_Mục tiêu: 55-57 điểm | Kết quả: **56.79 điểm**_

Đã hoàn thành tối ưu hóa toàn bộ các cờ vLLM trên stock image `vllm/vllm-openai:v0.22.1`:

- ✅ `OMP_NUM_THREADS=2` (Sweet-spot cho 3 CPU cores)
- ✅ `--enable-chunked-prefill` + `--max-num-batched-tokens=4096`
- ✅ `--quantization=fp8` (Online FP8 giảm TPOT từ 5ms → 4ms)
- ✅ `--enable-prefix-caching` + `--no-enable-log-requests` + `--disable-log-stats`
- ✅ `--max-num-seqs=32` + `--gpu-memory-utilization=0.95`

**Kết luận**: Flag tuning đã chạm ceiling ~57 điểm. Mọi biến thể thêm đều ≤ 56.79.

### Giai đoạn 2: Custom Image + Advanced Tuning (18-21/07)

_Mục tiêu: 58-75 điểm_

Kết hợp **song song** hai hướng:

#### Hướng A: Advanced Stock Image Flags (dùng hết slots không cần custom image)

1. **Compilation Optimization** (`--compilation-config '{"level": 3}'`)
2. **N-gram Speculative Decoding** (`--speculative-model [ngram]`)
3. **Chunk Size & Block Size Fine-tuning**
4. **Scheduling Policy** variations

#### Hướng B: Custom Docker Image cho LFM2.5 (tái sử dụng hạ tầng Round 1)

Adapting Ghost Strategy infrastructure cho model mới:

| Bước | Công việc                                                              | Thời gian | Tái sử dụng từ R1      |
| :--: | :--------------------------------------------------------------------- | :-------: | :--------------------- |
|  1   | Adapt hijack script v11 cho LFM2.5                                     |   2-3h    | ✅ Ghost v11 scripts   |
|  2   | Build custom image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v1` |   1-2h    | ✅ Dockerfile pipeline |
|  3   | Online Quantization & Kernel tuning (FP8/INT8 KV)                      |   2-4h    | ⚠️ Mới (LFM2.5 arch)   |
|  4   | Custom FP8 KV Cache cho attention layers                               |   1-2h    | ✅ FP8 KV kernels      |
|  5   | Warmup strategy cho LFM2.5                                             |    1h     | ✅ Warmup infra        |
|  6   | Submit & Test (15 slots/ngày)                                          |  Ongoing  | ✅ Compose templates   |

**Tổng thời gian ước tính**: 1-2 ngày (nhờ tái sử dụng ~70% hạ tầng Round 1).

**Tuân thủ quy định & Ràng buộc cứng**:

- ✅ Luôn giữ nguyên `--model=/model` và nạp model BF16 gốc do BTC mount. Không thay đổi weights model offline (tuân thủ mục 5 chống gian lận).
- ✅ Sử dụng Online Quantization (`--quantization=fp8` động của vLLM) kết hợp custom Triton kernels viết sẵn trong image để tăng tốc tính toán trực tiếp từ weights gốc.
- ⚠️ Cần tối ưu lại FP8 KV kernels cho cấu trúc hybrid recurrent đặc thù của LFM2.5.

### Giai đoạn 3: Deep Optimization + Speculative Decoding (22-30/07)

_Mục tiêu: 75-90+ điểm_

1. **Speculative Decoding với LFM2.5-350M Draft Model**
   - Custom image chứa cả target (chỉ đường dẫn `/model` gốc) + draft model LFM2.5-350M đóng gói sẵn trong image (load qua `--speculative-model=/draft_model`).
   - Tiềm năng 2-3x decode speedup → TPOT 1-2ms.
   - Rủi ro: LFM2.5 hybrid arch có thể không hỗ trợ spec dec hoặc overhead cao trên 3 core CPU.

2. **Custom Triton Kernels cho Recurrent Layers**
   - Viết kernel tối ưu cho gated short-convolution blocks.
   - Fuse LayerNorm + Linear + Activation trực tiếp trên weights nạp online.
   - Giảm kernel launch overhead.

3. **Flash-Linear-Attention Integration**
   - Tích hợp kernel attention tối ưu cho hybrid arch.
   - Giảm TTFT prefill time.

---

## 4. 📅 Lộ trình Chi tiết theo Tuần

### Tuần 3 (16-20/07): Foundation & Custom Image Build

| Ngày  | Trọng tâm                                        | Mục tiêu điểm | Giai đoạn |
| :---: | :----------------------------------------------- | :-----------: | :-------: |
| 16/07 | ✅ Baseline + Flag sweep (15 slots)              |     42-55     |   GĐ 1    |
| 17/07 | ✅ Multi-factor combo (15 slots)                 | **56.79** ✅  |   GĐ 1    |
| 18/07 | Advanced flags (B1-B3) + Adapt hijack cho LFM2.5 |     57-62     |  GĐ 1→2   |
| 19/07 | Custom Image build + Online Quant testing        |     58-68     |   GĐ 2    |
| 20/07 | Custom Image fine-tune + FP8 KV adapt            |     62-72     |   GĐ 2    |

### Tuần 4 (21-27/07): Custom Image Optimization & Spec Dec

| Ngày  | Trọng tâm                                    | Mục tiêu điểm | Giai đoạn |
| :---: | :------------------------------------------- | :-----------: | :-------: |
| 21/07 | Online Quant + Custom Kernel combo tối ưu    |     68-75     |   GĐ 2    |
| 22/07 | Speculative Decoding prototype (LFM2.5-350M) |     70-78     |  GĐ 2→3   |
| 23/07 | Spec Dec submit + Custom Triton kernel R&D   |     73-82     |   GĐ 3    |
| 24/07 | Custom Triton kernel submit + Combo          |     75-85     |   GĐ 3    |
| 25/07 | Deep optimization sweep                      |     78-88     |   GĐ 3    |
| 26/07 | Final optimization + Stability test          |     80-90     |   GĐ 3    |
| 27/07 | Buffer day: Fix bugs + Best config retries   |     80-90     |   GĐ 3    |

### Tuần 5 (28-30/07): Polish & Lock-in

| Ngày  | Trọng tâm                      | Mục tiêu điểm | Giai đoạn |
| :---: | :----------------------------- | :-----------: | :-------: |
| 28/07 | Best config stability test     |     80-90     |   Chốt    |
| 29/07 | GPQA accuracy verification     |     80-90     |   Chốt    |
| 30/07 | ⏰ **DEADLINE** - Final submit |   **80-90**   |   Chốt    |

---

## 5. 📋 Tiến độ & Kỷ lục

### Kỷ lục Progression

#### Round 1 (Qwen3.5-2B) — Kết thúc 15/07

| Mốc | Ngày  |   Điểm    | Cấu hình đột phá                                      |
| :-: | :---: | :-------: | :---------------------------------------------------- |
| #1  | 03/07 | **15.26** | Baseline gốc BTC                                      |
| #2  | 06/07 | **18.99** | + FP8 Quantization                                    |
| #3  | 11/07 | **20.82** | Custom FP8 KV Cache (Ghost v8)                        |
| #4  | 11/07 | **25.09** | + Warmup (Ghost v8.2)                                 |
| #5  | 14/07 | **39.83** | + Custom Kernel + Chunked Prefill (Ghost v9.4)        |
| #6  | 14/07 | **42.27** | + Chunk 16384 (Ghost v10.2)                           |
| #7  | 15/07 | **42.62** | + GPU Mem 0.96 (Ghost v11.4)                          |
| #8  | 15/07 | **51.10** | + Seqs 16 → TPOT 16ms (Ghost v11.6) ← **R1 Champion** |

#### Round 2 (LFM2.5-1.2B) — Bắt đầu 16/07

| Mốc | Ngày  |   Điểm    | Cấu hình đột phá                        | Giai đoạn |
| :-: | :---: | :-------: | :-------------------------------------- | :-------: |
| #1  | 16/07 | **42.91** | Baseline BTC + OMP=4 + Seqs=48          |   GĐ 1    |
| #2  | 16/07 | **45.08** | Seqs=32 + Chunk=4096                    |   GĐ 1    |
| #3  | 16/07 | **55.04** | FP8 Quantization                        |   GĐ 1    |
| #4  | 17/07 | **56.79** | FP8 + OMP=2 + Chunk=4096                |   GĐ 1    |
| #5  |  ???  |  **65+**  | _Custom Image + Custom Kernels?_        |   GĐ 2    |
| #6  |  ???  |  **75+**  | _Custom Kernel + Warmup?_               |   GĐ 2    |
| #7  |  ???  |  **80+**  | _Speculative Decoding / Custom Triton?_ |   GĐ 3    |

### Checklist Tổng thể

- [x] **GĐ 1**: Flag tuning stock image → 56.79 điểm (16-17/07)
- [ ] **GĐ 2**: Custom Image + Custom Kernels + Online Quant → 65-75 điểm (18-21/07)
- [ ] **GĐ 3**: Speculative Decoding + Custom Kernels → 80-90+ điểm (22-30/07)
- [ ] **Chốt**: GPQA verification + Final submit (28-30/07)
