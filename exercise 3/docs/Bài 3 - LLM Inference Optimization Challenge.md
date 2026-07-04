---
tags:
  -  #ViettelAIRace2026
  -  #LLM
  -  #Inference_Optimization
  -  #System_Architecture
status: 📝 Planning
date: 2026-07-02
---

# 🚀 [Bài 3] LLM Inference Optimization Challenge

## 1. 📅 Lộ trình thi & Yêu cầu nộp bài (Phases & Submissions)

Cuộc thi được chia làm 3 vòng (Phases) với các yêu cầu nộp bài (submission format) có sự khác biệt về mức độ đóng gói hệ thống:

### Phase 1: Vòng 1 - Sơ loại (Trực tuyến) [[Vòng 1 - Bài 3]]

- **Thời gian:** `28/06/2026 → 30/07/2026`
- **Định dạng nộp bài:** **Tệp Docker Compose GPU**.
- **Phân tích:** Ở vòng này, bạn chỉ cần nộp mã nguồn và file `docker-compose.yml`. Hệ thống chấm điểm của BTC sẽ tự động pull các base image từ Docker Hub và build container dựa trên config của bạn để chạy test. Cần tối ưu kỹ các lệnh build để tránh timeout khi hệ thống BTC dựng môi trường.

### Phase 2: Vòng 2 - Sơ khảo (Hackathon Offline tại Hà Nội)

- **Thời gian:** `16/08/2026 → 19/08/2026`
- **Định dạng nộp bài:** **Docker Image GPU**.
- **Phân tích:** Top 24 đội xuất sắc nhất sẽ thi đấu trực tiếp. Khác với Vòng 1, yêu cầu nộp bài lúc này khắt khe hơn: Thí sinh phải tự đóng gói toàn bộ hệ thống (gồm OS, CUDA runtime, Python env, weights mô hình và custom code) thành một Docker Image hoàn chỉnh và đẩy lên registry do BTC cung cấp. Điều này giúp loại bỏ rủi ro lỗi mạng/môi trường khi BTC chạy chấm điểm offline.

### Phase 3: Vòng 3 - Chung kết (Offline)

- **Thời gian:** `08/09/2026 → 10/09/2026` (Lễ trao giải: `11/09/2026`)
- **Định dạng nộp bài:** **Docker Image GPU**.
- **Phân tích:** Top 12 đội mạnh nhất sẽ thi đấu chung kết. Các đội tiếp tục tối ưu hóa sâu kiến trúc (như tùy chỉnh CUDA kernel) tạo ra bản Docker Image hoàn thiện nhất, đồng thời phải chuẩn bị slide để trình bày và bảo vệ kiến trúc giải pháp trước Hội đồng chuyên môn của Viettel.

## 2. 🎯 Tổng quan bài toán

Sự bùng nổ của các mô hình ngôn ngữ lớn (Large Language Models — LLM) trong những năm gần đây đang tạo ra áp lực rất lớn lên hạ tầng tính toán của các tổ chức và doanh nghiệp. Một hệ thống inference trong môi trường sản xuất thực tế không chỉ cần đạt thông lượng (throughput) cao, mà còn phải đảm bảo đồng thời ba yêu cầu cốt lõi: Độ trễ thấp (Latency), Độ chính xác ổn định (Accuracy), và Khả năng vận hành hiệu quả trên tài nguyên GPU hữu hạn.

Đây là bài toán tối ưu hóa phục vụ LLM (LLM serving optimization) có ràng buộc về chất lượng. Mục tiêu chung của cuộc thi là: Tối đa hóa Effective Request Score (ERS) trên toàn bộ workload trace cố định do Ban tổ chức (BTC) phát hành, đồng thời vượt qua bài kiểm tra chất lượng (pass accuracy gate).

## 3. 📊 Cơ chế tính điểm (Scoring System)

### A. ERS (Effective Request Score)

ERS là chỉ số đánh giá hiệu năng xử lý request thông qua cơ chế chấm điểm liên tục (continuous scoring), tối ưu đồng thời TTFT (Time-To-First-Token) và TPOT (Time-Per-Output-Token). Điểm ERS của hệ thống là trung bình cộng điểm của tất cả $N$ requests trong file trace:

$$ERS = \frac{1}{N} \sum_{i=1}^{N} S_{request, i} \in [0, 1)$$

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

- $F_{ttft}, F_{tpot}$: Cận dưới (Floor) của TTFT và TPOT — độ trễ đạt mức này hoặc thấp hơn sẽ nhận điểm tối đa ($s=1$).
- $C_{ttft}, C_{tpot}$: Cận trên (Ceiling) của TTFT và TPOT — độ trễ chạm mức này hoặc cao hơn sẽ bị tính $0$ điểm ($s=0$).
- $w$: Trọng số ưu tiên của TTFT ($0 < w < 1$).
- $\gamma$: Hệ số lũy thừa ($\gamma \ge 1$) quy định độ dốc của hàm phạt (penalty curve).
- Hàm $\text{clamp}(x, 0, 1)$: Giới hạn giá trị của $x$ luôn nằm trong đoạn $[0, 1]$.

### B. Accuracy Gate — GPQA Diamond

Accuracy được đánh giá độc lập bằng bộ 100 câu hỏi cố định trích xuất từ GPQA Diamond. Hàm suy giảm độ chính xác $\Delta$ (accuracy drop) được tính như sau:

$$\Delta = \text{baseline\_accuracy} - \text{GPQA\_accuracy\_của\_đội}$$

_(Trong đó, baseline_accuracy là điểm reference accuracy của mô hình gốc chạy bằng trọng số BF16)._

Dựa trên độ sụt giảm $\Delta$, hệ thống áp dụng hàm phạt $f(\Delta)$ (Accuracy decay function) — một hàm bậc nhất từng đoạn (piecewise linear) với giá trị đầu ra thuộc đoạn $[0, 1]$, quy định mức độ trừ điểm vào tổng điểm cuối cùng:

$$
f(\Delta) = \begin{cases}
1.0 & \text{khi } \Delta \le 10 \\
1.0 - \frac{\Delta - 10}{6} & \text{khi } 10 < \Delta < 16 \\
0.0 & \text{khi } \Delta \ge 16
\end{cases}
$$

### C. Công thức tính điểm tổng

Điểm số cuối cùng của mỗi đội được tính bằng cách kết hợp điểm hiệu năng phục vụ (ERS) với hình phạt sụt giảm chất lượng (Accuracy drop):

$$Score = 100 \times ERS \times f(\Delta)$$

Trong đó:

- **ERS (Effective Request Score):** Điểm số trung bình đánh giá hiệu năng xử lý request trên toàn bộ trace.
- **$f(\Delta)$:** Hệ số phạt dựa trên mức sụt giảm độ chính xác.

## 4. 🖥️ Môi trường & Mô hình đánh giá

| Thành phần        | Chi tiết cấu hình                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| **Phần cứng**     | NVIDIA H200 GPU                                                                                  |
| **Hệ điều hành**  | Ubuntu 22.04 LTS, CUDA 12.x                                                                      |
| **Mô hình**       | Dense Transformer do BTC chỉ định (Tải từ HuggingFace Hub với Hash cố định)                      |
| **Định dạng gốc** | BF16 (native release) — hỗ trợ các phương pháp quantization như FP8/AWQ/GPTQ, License Apache 2.0 |

## 5. 🛠️ Phương pháp tối ưu được phép

Thí sinh được toàn quyền tự do lựa chọn và kết hợp các phương pháp tối ưu, miễn không vi phạm quy định của cuộc thi. Các hướng tiếp cận được khuyến khích bao gồm:

- **KV Cache Optimization:** KV cache quantization (FP8, INT8), KV cache offloading (CPU/NVMe), prefix caching, semantic caching, Paged Attention, memory-aware scheduling.
- **Serving & Scheduling Optimization:** Dynamic/continuous batching, speculative decoding (sử dụng draft model hoặc self-speculative), disaggregated prefill/decode serving.
- **System-Level Optimization:** Custom CUDA / Triton kernels, fused attention kernels (FlashAttention, FlashInfer...), NCCL communication optimization cho NVLink topology, CUDA Graphs, memory layout optimization.
- **Runtime & Compiler Optimization:** Sử dụng các framework như vLLM, SGLang, TensorRT-LLM, Transformers, hoặc custom runtime; tùy chỉnh tensor parallelism và pipeline parallelism; overlap communication/computation.

## 6. 🚫 Rule & Anti-Cheating

Nghiêm cấm tuyệt đối các hành vi sau:

❌ Hardcode đáp án của probe subset trong mã nguồn.

❌ Pre-compute response (tính toán trước câu trả lời) cho các request nằm trong trace.

❌ Gọi network external từ inference server trong quá trình serving (Không call API ngoài, không pull model dynamically).

❌ Chỉnh sửa (sửa đổi) tokenizer của mô hình.

❌ Thay đổi arrival timestamp của trace hoặc cấu hình concurrency.

❌ Sử dụng account khác/account phụ để leak hidden trace giữa các đội.

> _Hình thức xử lý: Vi phạm → submission bị void. Vi phạm nghiêm trọng → đội bị loại._
