# 🚀 [Bài 3] LLM Inference Optimization Challenge - Specification

Tài liệu này tổng hợp toàn bộ thông tin chính thức từ Ban Tổ Chức (BTC) về yêu cầu, môi trường, cơ chế tính điểm và quy định của cuộc thi.

---

## 1. 📅 Lộ trình thi (Phases)

- **Phase 1: Vòng 1 - Sơ loại (Trực tuyến):** `28/06/2026 → 30/07/2026`
  - _Hình thức:_ Nộp file `docker-compose.yml` qua Portal. Hệ thống Grader tự động pull image từ Docker Hub và chạy benchmark.
- **Phase 2: Vòng 2 - Sơ khảo (Hackathon Offline tại Hà Nội):** `16/08/2026 → 19/08/2026`
  - _Hình thức:_ Đóng gói toàn bộ hệ thống (gồm model weights) thành một Docker Image GPU và đẩy lên registry riêng của BTC.
- **Phase 3: Vòng 3 - Chung kết (Offline):** `08/09/2026 → 10/09/2026`
  - _Hình thức:_ Tối ưu hóa sâu (CUDA kernel) + Trình bày giải pháp trước hội đồng chuyên môn.

---

## 2. 🖥️ Môi trường & Hạ tầng Grader (MiG H200)

Mỗi lượt nộp bài sẽ được chấm điểm tự động trên hạ tầng được cô lập vật lý:

- **Phần cứng:** **1 instance MiG H200** (Phân bổ: **18GB VRAM**, **3 Core CPU**, **8GB RAM**).
- **Hệ điều hành & Driver:** Ubuntu 22.04 LTS, CUDA 12.x.
- **Mô hình mục tiêu:** **Qwen/Qwen3.5-2B** (Dense Transformer, gốc BF16, tải từ HuggingFace Hub với Hash cố định).
- **Serving Engine:** Về mặt lý thuyết, BTC cho phép toàn quyền lựa chọn framework (vLLM, SGLang, TensorRT-LLM, custom runtime...). Tuy nhiên, trong thực tế Vòng 1, hệ thống chấm bài tự động ép buộc cấu hình và entrypoint của vLLM, các serving engine khác không tương thích/bị báo lỗi khởi động, do đó khuyến nghị chỉ sử dụng **vLLM framework**.

---

## 3. 📊 Cơ chế tính điểm (Scoring System)

Điểm số cuối cùng của mỗi đội được tính bằng cách kết hợp hiệu năng xử lý request (ERS) với hình phạt sụt giảm chất lượng (Accuracy drop):

$$Score = 100 \times ERS \times f(\Delta)$$

### A. ERS (Effective Request Score)

ERS là điểm số trung bình của $N$ requests ($N = 120$) trong file trace dữ liệu:

$$ERS = \frac{1}{N} \sum_{i=1}^{N} S_{request, i} \in [0, 1]$$

Điểm số của từng request ($S_{request}$) được tính như sau:

$$
S_{request} = \begin{cases}
0 & \text{nếu lỗi / timeout / trả về 0 token} \\
w \cdot s_{ttft} + (1 - w) \cdot s_{tpot} & \text{nếu xử lý thành công}
\end{cases}
$$

Trong đó:

$$s_{ttft} = (x_{ttft})^\gamma = \left[ \text{clamp}\left( \frac{C_{ttft} - TTFT}{C_{ttft} - F_{ttft}}, 0, 1 \right) \right]^\gamma$$

$$s_{tpot} = (x_{tpot})^\gamma = \left[ \text{clamp}\left( \frac{C_{tpot} - TPOT_{mean}}{C_{tpot} - F_{tpot}}, 0, 1 \right) \right]^\gamma$$

**Tham số cấu hình:**

| Ký hiệu    | Ý nghĩa           | Giá trị |
| :--------- | :---------------- | :------ |
| $F_{ttft}$ | Floor của TTFT    | 100 ms  |
| $C_{ttft}$ | Ceiling của TTFT  | 1500 ms |
| $F_{tpot}$ | Floor của TPOT    | 20 ms   |
| $C_{tpot}$ | Ceiling của TPOT  | 45 ms   |
| $\gamma$   | Hệ số lũy thừa    | 2       |
| $w$        | Trọng số của TTFT | 0.5     |

**Giải thích các tham số cấu hình:**

- $F_{ttft}, F_{tpot}$: Cận dưới (Floor) của TTFT và TPOT — độ trễ đạt mức này hoặc thấp hơn sẽ nhận điểm tối đa ($s=1.0$).
- $C_{ttft}, C_{tpot}$: Cận trên (Ceiling) của TTFT và TPOT — độ trễ chạm mức này hoặc cao hơn sẽ bị tính $0$ điểm ($s=0.0$).
- $w$: Trọng số ưu tiên của TTFT ($0 < w < 1$).
- $\gamma$: Hệ số lũy thừa ($\gamma \ge 1$) quy định độ dốc của hàm phạt (penalty curve).
- Hàm $\text{clamp}(x, 0, 1)$: Giới hạn giá trị của $x$ luôn nằm trong đoạn $[0, 1]$.

### B. Accuracy Gate (GPQA Diamond)

Đánh giá độ chính xác độc lập qua bộ 100 câu hỏi GPQA Diamond. Độ sụt giảm accuracy $\Delta$ so với baseline BF16 (reference, mặc định baseline đạt 0.4):

$$\Delta = \text{baseline\_accuracy} - \text{GPQA\_accuracy\_của\_đội}$$

Hàm phạt $f(\Delta)$ được định nghĩa như sau:

$$
f(\Delta) = \begin{cases}
1.0 & \text{nếu } \Delta \le 0.1 \\
1.0 - \frac{\Delta - 0.10}{0.06} & \text{nếu } 0.1 < \Delta < 0.16 \\
0.0 & \text{nếu } \Delta \ge 0.16
\end{cases}
$$

---

## 4. 🛠️ Phạm vi tối ưu được phép

Thí sinh được khuyến khích sử dụng các kỹ thuật sau:

- **Quantization:** FP8 (F8_E4M3), INT8, AWQ, GPTQ (Quantization động online khi load model được phép; cấm dùng weights đã được offline pre-quantized từ bên ngoài).
- **KV Cache:** Lượng tử hóa KV cache (FP8, INT8), prefix caching, semantic caching, Paged Attention.
- **Serving Runtime:** Continuous batching, speculative decoding (draft model/self-speculative), custom CUDA/Triton kernels, fused attention (FlashAttention, FlashInfer).
- **System Tuning:** Overlap communication/computation, CUDA Graphs, CPU thread configuration (`OMP_NUM_THREADS`).

---

## 5. 🚫 Quy định chống gian lận (Anti-Cheating)

- ❌ Không hardcode đáp án của GPQA Diamond probe subset.
- ❌ Không pre-compute response (tính toán trước kết quả đầu ra cho trace).
- ❌ Không thực hiện cuộc gọi mạng ra ngoài (External Network Calls) từ inference server.
- ❌ Không thay đổi tokenizer hoặc cấu hình arrival timestamp của trace benchmark.

---

## 6. File `docker-compose.yml` mẫu của BTC

```yaml
services:
  model:
    image: vllm/vllm-openai:v0.22.1
    entrypoint:
      - python3
      - -m
      - vllm.entrypoints.openai.api_server
    command:
      - --model=/model
      - --served-model-name=Qwen3.5-2B
      - --host=0.0.0.0
      - --port=8000
      - --max-model-len=262144
      - --gpu-memory-utilization=0.95
      - --tensor-parallel-size=1
      - --enable-prefix-caching
    ports:
      - "8000:8000"
    shm_size: "2g"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```
