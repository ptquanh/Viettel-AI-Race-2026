# 🚀 [Bài 3] LLM Inference Optimization Challenge - Specification

Tài liệu này tổng hợp toàn bộ thông tin chính thức từ Ban Tổ Chức (BTC) về yêu cầu, môi trường, cơ chế tính điểm và quy định của cuộc thi sau khi cập nhật mô hình mục tiêu và các chỉ số đo lường mới.

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
- **Hệ điều hành & Driver (host):** Ubuntu 24.04 LTS, NVIDIA driver 590.x (hỗ trợ CUDA 13.x).
- **Mô hình mục tiêu:** **LiquidAI/LFM2.5-1.2B-Instruct** (Kiến trúc Liquid Foundation Model, tải từ HuggingFace Hub với Hash cố định).
- **Serving Engine:** Thí sinh chỉ được phép sử dụng serving framework **vLLM** cho bài thi này.

---

## 3. 📊 Cơ chế tính điểm (Scoring System)

Điểm số cuối cùng của mỗi đội được tính bằng cách kết hợp hiệu năng xử lý request (ERS) với hình phạt sụt giảm chất lượng (Accuracy drop):

$$Score = 100 \times ERS \times f(\Delta)$$

### A. ERS (Effective Request Score)

ERS là điểm số trung bình của $N$ requests ($N = 330$ requests được chấm điểm sau 15 hội thoại primer khởi động không tính điểm) trong file trace dữ liệu:

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

**Tham số cấu hình mới:**

| Ký hiệu    | Ý nghĩa           | Giá trị |
| :--------- | :---------------- | :------ |
| $F_{ttft}$ | Floor của TTFT    | 10 ms   |
| $C_{ttft}$ | Ceiling của TTFT  | 400 ms  |
| $F_{tpot}$ | Floor của TPOT    | 1 ms    |
| $C_{tpot}$ | Ceiling của TPOT  | 10 ms   |
| $\gamma$   | Hệ số lũy thừa    | 2       |
| $w$        | Trọng số của TTFT | 0.5     |

_Với kiến trúc recurrent đặc thù của LFM, các chỉ số Floor/Ceiling latency đã được siết chặt tối đa (TTFT Floor 10ms, TPOT Floor 1ms) để phản ánh tốc độ xử lý siêu nhanh của mô hình._

### B. Accuracy Gate (GPQA Diamond - Hậu kiểm sau vòng online)

Không chấm GPQA trên từng lượt nộp online. Sau khi vòng online kết thúc, đội thi chọn thủ công tối đa 5 submissions tốt nhất để BTC hậu kiểm và chạy GPQA full.

Độ sụt giảm chất lượng ($\Delta$) so với baseline BF16 (mặc định baseline đạt 0.4):

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

Thí sinh được khuyến khích sử dụng các kỹ thuật sau trên vLLM:

- **Quantization:** Các kỹ thuật Online Quantization.
- **KV Cache & Memory:** Tối đa hóa lượng request xử lý đồng thời bằng Paged Attention; KV cache quantization (FP8, INT8); Prefix caching và Semantic caching; Offloading xuống CPU/NVMe.
- **Serving & Scheduling:** Ứng dụng Dynamic/Continuous batching; Speculative decoding; Memory-aware scheduling.
- **System & Runtime:** Viết custom CUDA/Triton kernels; Tích hợp Fused attention kernels (FlashAttention, FlashInfer); Tối ưu hóa memory layout và CUDA Graphs.

---

## 5. 🚫 Quy định chống gian lận (Anti-Cheating)

- ❌ Nghiêm cấm pre-bake, hardcode kết quả, cơ chế dual-path hoặc lách luật (gaming) phương pháp đo lường.
- ❌ Không thực hiện cuộc gọi mạng ra ngoài (External Network Calls) từ inference server.
- ❌ Không can thiệp trái phép vào tokenizer hoặc weights của mô hình.
- ❌ Không tráo đổi Docker image sau khi đã chốt nộp bài.

---

## 6. File `docker-compose.yml` mẫu của BTC cho LFM2.5

```yaml
services:
  model:
    image: vllm/vllm-openai:v0.22.1
    entrypoint:
      - python3 #Don't change this to vllm-server
      - -m #Don't change this to vllm-server
      - vllm.entrypoints.openai.api_server #Don't change this to vllm-server
    command:
      - --model=/model #Don't change this to vllm-server
      - --served-model-name=LFM2.5-1.2B-Instruct #Don't change this to vllm-server
      - --host=0.0.0.0 #Don't change this to vllm-server
      - --port=8000 #Don't change this to vllm-server
      - --max-model-len=32768
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

---

## 7. 📈 Đặc tả Workload Trace thực tế (Cập nhật 18/07/2026)

workload chấm điểm của BTC được cấu hình dưới dạng multi-turn với context tăng dần và độ dài đầu ra được cố định, mô tả chi tiết trong [grading-workload-spec.json](exercise 3/input/grading-workload-spec.json):

```json
{
  "workload": "vLLM multi-turn (shared prefix + growing context, output length pinned)",
  "num_conversations": 70,
  "user_turns_per_conversation": 6,
  "total_requests": 420,
  "shared_system_prefix_tokens": 1000,
  "per_conversation_prefix_tokens": 1000,
  "new_user_tokens_per_turn": 150,
  "output_tokens_per_turn_pinned": 300,
  "arrival": "Poisson, seed 42"
}
```

### Ý nghĩa chi tiết các tham số:

- **`num_conversations` (70)**: Số hội thoại độc lập chạy đồng thời.
- **`user_turns_per_conversation` (6)**: Số lượt hỏi của user trên mỗi hội thoại.
- **`total_requests` (420)**: Tổng số request gửi đến server ($70 \times 6 = 420$).
- **`shared_system_prefix_tokens` (1000)**: System prompt dùng chung cho tất cả các hội thoại (thích hợp tối ưu hóa bằng prefix caching).
- **`per_conversation_prefix_tokens` (1000)**: Ngữ cảnh riêng cho từng hội thoại (bổ sung input cho turn 1 của từng hội thoại).
- **`new_user_tokens_per_turn` (150)**: Số lượng token prompt mới của user tại mỗi turn (ở turn 1 có thêm 2 khối prefix 1000 + 1000 tokens).
- **`output_tokens_per_turn_pinned` (300)**: Số lượng token output cố định tại mỗi turn.
- **`arrival` (Poisson, seed 42)**: Phân phối nhịp đến của các requests mô phỏng traffic thực tế.

### Phân tích độ dài ngữ cảnh lũy tiến (Turn 1 $\rightarrow$ Turn 6):

Tại mỗi turn $k$ trong hội thoại, độ dài prompt đầu vào tăng dần do cộng dồn lịch sử hội thoại trước đó:

- **Turn 1**: $1000 \text{ (shared)} + 1000 \text{ (conv prefix)} + 150 \text{ (prompt 1)} = \mathbf{2150 \text{ tokens}}$. Sinh thêm $300 \text{ tokens}$ output.
- **Turn 2**: $2150 \text{ (Turn 1 context)} + 300 \text{ (Turn 1 output)} + 150 \text{ (prompt 2)} = \mathbf{2600 \text{ tokens}}$. Sinh thêm $300 \text{ tokens}$ output.
- **Turn 3**: $2600 + 300 + 150 = \mathbf{3050 \text{ tokens}}$. Sinh thêm $300 \text{ tokens}$ output.
- **Turn 4**: $3050 + 300 + 150 = \mathbf{3500 \text{ tokens}}$. Sinh thêm $300 \text{ tokens}$ output.
- **Turn 5**: $3500 + 300 + 150 = \mathbf{3950 \text{ tokens}}$. Sinh thêm $300 \text{ tokens}$ output.
- **Turn 6**: $3950 + 300 + 150 = \mathbf{4400 \text{ tokens}}$. Sinh thêm $300 \text{ tokens}$ output.

$\rightarrow$ **Chiều dài context tối đa (Max Context Length) của bất kỳ request nào trong trace là $4700 \text{ tokens}$**. Điều này cho phép thí sinh giới hạn `--max-model-len=8192` (thay vì $32768$ mặc định) giúp giải phóng VRAM cực lớn và đẩy nhanh tốc độ warmup CUDA Graph.
