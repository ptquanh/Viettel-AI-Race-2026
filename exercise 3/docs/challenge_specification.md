# 🚀 [Bài 3] LLM Inference Optimization Challenge - Specification

Tài liệu này tổng hợp toàn bộ thông tin chính thức từ Ban Tổ Chức (BTC) về yêu cầu, môi trường, cơ chế tính điểm và quy định của cuộc thi.

---

## 1. 📅 Lộ trình thi (Phases)

*   **Phase 1: Vòng 1 - Sơ loại (Trực tuyến):** `28/06/2026 → 30/07/2026`
    *   *Hình thức:* Nộp file `docker-compose.yml` qua Portal. Hệ thống Grader tự động pull image từ Docker Hub và chạy benchmark.
*   **Phase 2: Vòng 2 - Sơ khảo (Hackathon Offline tại Hà Nội):** `16/08/2026 → 19/08/2026`
    *   *Hình thức:* Đóng gói toàn bộ hệ thống (gồm model weights) thành một Docker Image GPU và đẩy lên registry riêng của BTC.
*   **Phase 3: Vòng 3 - Chung kết (Offline):** `08/09/2026 → 10/09/2026`
    *   *Hình thức:* Tối ưu hóa sâu (CUDA kernel) + Trình bày giải pháp trước hội đồng chuyên môn.

---

## 2. 🖥️ Môi trường & Hạ tầng Grader (MiG H200)

Mỗi lượt nộp bài sẽ được chấm điểm tự động trên hạ tầng được cô lập vật lý:

*   **Phần cứng:** **1 instance MiG H200** (Phân bổ: **18GB VRAM**, **3 Core CPU**, **8GB RAM**).
*   **Hệ điều hành & Driver:** Ubuntu 22.04 LTS, CUDA 12.x.
*   **Mô hình mục tiêu:** **Qwen/Qwen3.5-2B** (Dense Transformer, gốc BF16, tải từ HuggingFace Hub với Hash cố định).
*   **Serving Engine:** Bắt buộc sử dụng **vLLM framework**. Lệnh khởi chạy được grader kiểm soát thông qua entrypoint vLLM của container. các serving engine khác (SGLang, LMDeploy...) không tương thích và sẽ bị báo lỗi khởi động.

---

## 3. 📊 Cơ chế tính điểm (Scoring System)

Điểm số cuối cùng của mỗi đội được tính bằng cách kết hợp hiệu năng xử lý request (ERS) với hình phạt sụt giảm chất lượng (Accuracy drop):

$$Score = 100 \times ERS \times f(\Delta)$$

### A. ERS (Effective Request Score)
ERS là điểm số trung bình của $N$ requests ($N = 120$) trong file trace dữ liệu:

$$ERS = \frac{1}{N} \sum_{i=1}^{N} S_{request, i}$$

Điểm số của mỗi request $S_{request}$ được tính dựa trên TTFT (Time-To-First-Token) và TPOT (Time-Per-Output-Token):

$$
S_{request} = \begin{cases}
0 & \text{nếu lỗi, timeout, hoặc trả về 0 token} \\
0.5 \cdot s_{ttft} + 0.5 \cdot s_{tpot} & \text{nếu xử lý thành công}
\end{cases}
$$

Trong đó, điểm TTFT ($s_{ttft}$) và TPOT ($s_{tpot}$) được nội suy phi tuyến tính (lũy thừa $\gamma = 2$):

$$s_{ttft} = \left[ \text{clamp}\left( \frac{1500 - TTFT}{1400}, 0, 1 \right) \right]^2$$

$$s_{tpot} = \left[ \text{clamp}\left( \frac{45 - TPOT}{25}, 0, 1 \right) \right]^2$$

*   **Ngưỡng Lý tưởng (Floor):** $TTFT \le 100\text{ms}$ và $TPOT \le 20\text{ms}$ sẽ đạt điểm thành phần tối đa ($s = 1.0$).
*   **Ngưỡng Giới hạn (Ceiling):** $TTFT \ge 1500\text{ms}$ hoặc $TPOT \ge 45\text{ms}$ sẽ nhận điểm thành phần bằng $0$.

### B. Accuracy Gate (GPQA Diamond)
Đánh giá độ chính xác độc lập qua bộ 100 câu hỏi GPQA Diamond. Độ sụt giảm accuracy $\Delta$ so với baseline BF16 (reference):

$$\Delta = \text{baseline\_accuracy} - \text{GPQA\_accuracy\_của\_đội}$$

Hàm phạt $f(\Delta)$ được định nghĩa như sau:

$$
f(\Delta) = \begin{cases}
1.0 & \text{khi } \Delta \le 10\% \\
1.0 - \frac{\Delta - 10}{6} & \text{khi } 10\% < \Delta < 16\% \\
0.0 & \text{khi } \Delta \ge 16\%
\end{cases}
$$

---

## 4. 🛠️ Phạm vi tối ưu được phép

Thí sinh được khuyến khích sử dụng các kỹ thuật sau:
*   **Quantization:** FP8 (F8_E4M3), INT8, AWQ, GPTQ (Quantization động online khi load model được phép; cấm dùng weights đã được offline pre-quantized từ bên ngoài).
*   **KV Cache:** Lượng tử hóa KV cache (FP8, INT8), prefix caching, semantic caching, Paged Attention.
*   **Serving Runtime:** Continuous batching, speculative decoding (draft model/self-speculative), custom CUDA/Triton kernels, fused attention (FlashAttention, FlashInfer).
*   **System Tuning:** Overlap communication/computation, CUDA Graphs, CPU thread configuration (`OMP_NUM_THREADS`).

---

## 5. 🚫 Quy định chống gian lận (Anti-Cheating)

*   ❌ Không hardcode đáp án của GPQA Diamond probe subset.
*   ❌ Không pre-compute response (tính toán trước kết quả đầu ra cho trace).
*   ❌ Không thực hiện cuộc gọi mạng ra ngoài (External Network Calls) từ inference server.
*   ❌ Không thay đổi tokenizer hoặc cấu hình arrival timestamp của trace benchmark.

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
