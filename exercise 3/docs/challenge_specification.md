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
- **Hệ điều hành & Driver (host):** Ubuntu 24.04 LTS, NVIDIA driver 590.x (hỗ trợ CUDA 13.x).
- **Mô hình mục tiêu:** **LiquidAI/LFM2.5-1.2B-Instruct** (Kiến trúc Liquid Foundation Model, tải từ HuggingFace Hub với Hash cố định).
- **Serving Engine:** Thí sinh chỉ được phép sử dụng serving framework **vLLM** cho bài thi này.

---

## 3. Workload Trace & Cách tính điểm

### 3.1 Nguồn dữ liệu

BTC sử dụng bộ dữ liệu mô phỏng luồng request thực tế trong môi trường LLM serving quy mô lớn, chọn lọc để đại diện cho các pattern traffic phổ biến. Cấu trúc trace:

- **Multi-turn:** mỗi hội thoại gồm nhiều lượt; lượt kế tiếp chỉ gửi sau khi lượt trước hoàn tất kèm khoảng "think" mô phỏng thời gian người dùng, giữ nguyên tính nhân-quả của hội thoại thật.
- **Giới hạn độ dài:** mỗi prompt bị giới hạn độ dài context input và số token output, phản ánh tải prefill/decode thực tế trên slice được cấp.
- **Bản công khai vs bản chấm:** thí sinh nhận bản trace đã lược text (chỉ arrival + số token in/out mỗi lượt); BTC giữ bản đầy đủ và chỉ gửi prompt thật tới endpoint lúc chấm - chống pre-bake/học tủ theo nội dung.

### 3.2 ERS (Effective Request Score)

ERS là chỉ số đánh giá hiệu năng xử lý request thông qua cơ chế chấm điểm liên tục, tối ưu đồng thời TTFT và TPOT. Điểm ERS của hệ thống là trung bình cộng điểm của tất cả $N$ requests trong file trace:

$$ERS = \frac{1}{N} \sum_{i=1}^{N} S_{request, i} \in [0, 1]$$

Điểm của từng request ($S_{request}$) được tính như sau:

$$
S_{request} = \begin{cases}
0 & \text{nếu lỗi, timeout, hoặc trả về 0 token} \\
w \cdot s_{ttft} + (1 - w) \cdot s_{tpot} & \text{nếu xử lý thành công}
\end{cases}
$$

Trong đó, điểm thành phần độ trễ $s_{ttft}$ và $s_{tpot}$ được nội suy giữa ngưỡng lý tưởng (Floor - $F$) và ngưỡng giới hạn (Ceiling - $C$):

$$s_{ttft} = \left[ \text{clamp}\left( \frac{C_{ttft} - TTFT}{C_{ttft} - F_{ttft}}, 0, 1 \right) \right]^\gamma$$

$$s_{tpot} = \left[ \text{clamp}\left( \frac{C_{tpot} - TPOT}{C_{tpot} - F_{tpot}}, 0, 1 \right) \right]^\gamma$$

Giải thích các tham số cấu hình:

- $F_{ttft}$, $F_{tpot}$: Cận dưới (Floor) - độ trễ đạt mức này hoặc thấp hơn sẽ nhận điểm tối đa ($s=1$).
- $C_{ttft}$, $C_{tpot}$: Cận trên (Ceiling) - độ trễ chạm mức này hoặc cao hơn sẽ bị tính $0$ điểm ($s=0$).
- $w$: Trọng số ưu tiên của TTFT ($0 < w < 1$).
- $\gamma$: Hệ số lũy thừa ($\gamma \ge 1$) quy định độ dốc của hàm phạt (penalty curve).
- Hàm $\text{clamp}(x, 0, 1)$: Giới hạn giá trị của $x$ luôn nằm trong đoạn $[0, 1]$.

_(Tham khảo bảng cấu hình thực tế cập nhật gần nhất: $F_{ttft}=10ms, C*{ttft}=400ms, F*{tpot}=1ms, C*{tpot}=10ms, \gamma=2, w=0.5$)*

### 3.3 Accuracy Gate

Không chấm accuracy theo từng lượt nộp trong vòng online. Leaderboard online phản ánh chủ yếu ERS (điểm độ trễ) và mang tính tham khảo cho đến khi Accuracy Gate hoàn tất.

Quy trình sau khi kết thúc vòng online:

1. **Đội chọn submissions:** Mỗi đội chọn thủ công tối đa 5 bài submissions tốt nhất (image/digest đã nộp trong vòng online; không được đổi image sau khi chọn).
2. **Hậu kiểm tính hợp lệ (BTC):** BTC kiểm tra phương án có tuân thủ Rule & Anti-Cheating / tinh thần production hay không (image pin, hành vi serving, dấu hiệu gian lận, v.v.). Bài không hợp lệ bị loại khỏi vòng accuracy / có thể void.
3. **Chấm GPQA Diamond full:** Với mỗi submission còn hợp lệ, BTC dựng lại endpoint OpenAI-compatible và chạy lm-evaluation-harness (lm_eval) trên bộ GPQA do BTC công bố (baseline reference BF16; filter strict-match).

Hàm suy giảm độ chính xác $\Delta$ (accuracy drop) được tính như sau:

$$\Delta = Accuracy_{baseline} - Accuracy_{submission}$$

(Trong đó, $Accuracy_{baseline}$ là accuracy tham chiếu của mô hình gốc chạy bằng trọng số BF16 do BTC công bố; $Accuracy_{submission}$ là accuracy bài nộp của đội.)

Dựa trên $\Delta$, hệ thống áp dụng hàm phạt $f(\Delta)$ - piecewise linear, đầu ra thuộc $[0, 1]$:

$$
f(\Delta) = \begin{cases}
1.0 & \text{nếu } \Delta \le 0.1 \\
1.0 - \frac{\Delta - 0.10}{0.06} & \text{nếu } 0.1 < \Delta < 0.16 \\
0.0 & \text{nếu } \Delta \ge 0.16
\end{cases}
$$

Với mỗi submission được chọn: $Score_i = 100 \times ERS_i \times f(\Delta_i)$. Điểm chính thức của đội là Score tốt nhất trong các bài còn hợp lệ sau hậu kiểm + GPQA (trừ khi BTC công bố quy tắc gộp khác).

### 3.4. Công thức tính điểm tổng

Điểm số cuối cùng kết hợp hiệu năng phục vụ (ERS từ vòng online) với hình phạt sụt giảm chất lượng sau Accuracy Gate:

$$Score = 100 \times ERS \times f(\Delta)$$

Score trên chỉ được chốt sau khi đội đã chọn tối đa 5 submissions và BTC hoàn tất hậu kiểm + GPQA Diamond full.

---

## 4. Mô hình sử dụng

Mô hình cụ thể do BTC chỉ định và công bố theo từng vòng. _(Hiện tại là LiquidAI/LFM2.5-1.2B-Instruct)_

---

## 5. Phương pháp tối ưu được phép

Thí sinh được toàn quyền tự do lựa chọn và kết hợp các phương pháp tối ưu, miễn không vi phạm quy định của cuộc thi. Các hướng tiếp cận được khuyến khích bao gồm:

- **KV Cache Optimization:** KV cache quantization (FP8, INT8), KV cache offloading (CPU/NVMe), prefix caching, semantic caching, Paged Attention, memory-aware scheduling.
- **Serving & Scheduling Optimization:** Dynamic/continuous batching, speculative decoding, disaggregated prefill/decode serving.
- **System-Level Optimization:** Custom CUDA / Triton kernels, fused attention kernels (FlashAttention, FlashInfer...), NCCL communication optimization, CUDA Graphs, memory layout optimization.
- **Runtime & Compiler Optimization:** Sử dụng vLLM.

---

## 6. Môi trường đánh giá chuẩn hóa

- **Hạ tầng phần cứng:** NVIDIA H200 GPU
- **Hệ điều hành:** Ubuntu 24.04 LTS
- **GPU Driver:** NVIDIA driver 590.x (hỗ trợ CUDA 13.x)

---

## 7. Rule & Anti-Cheating

Nguyên tắc cốt lõi: Giải pháp phải tối ưu hệ thống phục vụ trung thực, sẵn sàng triển khai cho người dùng thực tế. Mọi thủ thuật đánh lừa hệ thống đo lường hoặc chỉ hoạt động trên tập workload chấm thi đều bị xem là vi phạm nghiêm trọng.

### 7.1. Không gian tối ưu

❌ **Hành vi nghiêm cấm**

- **Pre-bake / Hardcode:** Tính sẵn đáp án thay vì suy luận thực tại thời điểm phục vụ.
- **Dual-path:** Rẽ nhánh hành vi xử lý giữa lúc đo độ trễ và lúc kiểm tra chất lượng.
- **Gaming metrics:** Đệm rỗng, cắt ngắn chuỗi sinh trái phép để né cổng hậu kiểm.
- **Can thiệp hạ tầng:** Gọi mạng ngoài, sửa tokenizer/weights, làm bẩn tài nguyên.
- **Bất trung thực quy trình:** Tráo image sau khi nộp, lộ dữ liệu.

### 7.2. Quy trình Hậu kiểm

Điểm số tự động trên hệ thống chưa phải là kết quả chốt cuối cùng.

- Ban tổ chức định kỳ hoặc đột xuất rà soát thủ công image, cấu hình, log và luồng serving.
- Bài nộp phát hiện gian lận sẽ bị hủy (void) kết quả hoặc điều chỉnh xếp hạng trực tiếp.
- Mọi quyết định xử lý đều được thông báo minh bạch qua email kèm lý do tóm tắt.

### 7.3. Phân định vùng sát điểm

Đối với các đội nằm trong vùng nhiễu đo lường ($\le 1–3$ điểm), thứ hạng sẽ được phân định tuần tự theo:

1. Mức độ suy giảm độ chính xác thấp hơn.
2. Chỉ số độ trễ p95 TTFT thấp hơn.
3. Tốc độ sinh văn bản cao hơn.
4. Thời điểm nộp bài hợp lệ sớm hơn.

### 7.4. Re-grade & Chế tài xử lý

- **Chấm lại:** Ban tổ chức có quyền chạy độc lập nhiều lần trên đúng bản Docker image đã chốt để lấy điểm trung vị. Các đội trong top đầu sẽ được ưu tiên rà soát.
- **Xử lý vi phạm:** Tùy mức độ, cá nhân hoặc đội thi có thể bị thu hồi điểm hoặc loại hoàn toàn khỏi giải đấu.
- **Quyền khiếu nại:** Hệ thống tiếp nhận phản hồi trong vòng 24 giờ kể từ thời điểm nhận email thông báo hoặc công bố kết quả hạng mục thi.

---

## Phụ lục 1: File `docker-compose.yml` mẫu của BTC cho LFM2.5

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

## Phụ lục 2: Đặc tả Workload Trace thực tế (Cập nhật 18/07/2026)

Workload chấm điểm của BTC được cấu hình dưới dạng multi-turn với context tăng dần và độ dài đầu ra được cố định, mô tả chi tiết trong `grading-workload-spec.json`:

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
