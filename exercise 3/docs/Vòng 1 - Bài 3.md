---
tags:
  - 
  - 
  - 
  - 
status: 🏃 In Progress
date: 2026-07-03
deadline: 2026-07-30
---

# 🚀 [Bài 3] Vòng 1 - Sơ loại: LLM Inference Optimization

**Thời gian diễn ra:** `02/07/2026 - 30/07/2026`

## 1. 🎯 Tổng quan

Đây là vòng thi mô phỏng trực tiếp thách thức mà các đội ngũ hạ tầng AI đang đối mặt: phục vụ LLM đáp ứng đồng thời thông lượng cao, độ trễ thấp, độ chính xác ổn định và hiệu quả trên tài nguyên GPU hữu hạn.

- **Nhiệm vụ:** Triển khai và tối ưu một LLM inference server cho mô hình xử lý một file trace gồm 120 requests mô phỏng traffic production. Mục tiêu là tối đa hoá tỷ lệ request được đáp ứng đúng hạn (Effective Request Capacity) trong khi vẫn phải vượt qua bài kiểm tra chất lượng đầu ra (Accuracy Gate).
- **Hạ tầng & Môi trường đánh giá:** Toàn bộ quá trình chạy benchmark được thực hiện tự động trên hệ thống của Ban tổ chức (BTC). Thí sinh sẽ serve endpoint trên 1 instance MiG và BTC sẽ thực hiện benchmark trực tiếp vào endpoint đó.
  - **Hạ tầng Hardware:** 1 instance MiG H200 (18GB VRAM, 3 Core CPU, 8GB RAM) được cấp phát tự động cho mỗi lượt chấm.
  - **Hệ điều hành & Driver:** Ubuntu 22.04 LTS, CUDA 12.x.
  - **Model:** Qwen/Qwen3.5-2B (Dense Transformer, gốc BF16).
  - **Nguồn Weights:** Tải từ HuggingFace Hub (mã hash cố định do BTC công bố).

## 2. 📊 Tiêu chí Đánh giá & Cách tính điểm

Effective Request Score được đánh giá dựa theo tốc độ trên 2 metrics TTFT và TPOT. Công thức cụ thể như sau:

$$ERS = \frac{1}{120} \sum_{i=1}^{120} S_{request, i} \in [0, 1]$$
_(với N là tổng số request, ở đây N = 120)._

Trong đó:

$$
S_{request} = \begin{cases}
0 & \text{nếu lỗi / timeout / trả về 0 token} \\
w \cdot s_{ttft} + (1 - w) \cdot s_{tpot}
\end{cases}
$$

$$s_{ttft} = (x_{ttft})^\gamma = \left[ \text{clamp}\left( \frac{C_{ttft} - TTFT}{C_{ttft} - F_{ttft}}, 0, 1 \right) \right]^\gamma$$

$$s_{tpot} = (x_{tpot})^\gamma = \left[ \text{clamp}\left( \frac{C_{tpot} - TBT_{mean}}{C_{tpot} - F_{tpot}}, 0, 1 \right) \right]^\gamma$$

**Tham số cấu hình:**

| Ký hiệu    | Ý nghĩa           | Giá trị |
| :--------- | :---------------- | :------ |
| $F_{ttft}$ | Floor của TTFT    | 100 ms  |
| $C_{ttft}$ | Ceiling của TTFT  | 1500 ms |
| $F_{tpot}$ | Floor của TPOT    | 20 ms   |
| $C_{tpot}$ | Ceiling của TPOT  | 45 ms   |
| $\gamma$   | Hệ số lũy thừa    | 2       |
| $w$        | Trọng số của TTFT | 0.5     |

**Accuracy Gate (GPQA Diamond):**
Được đánh giá độc lập qua 100 câu hỏi cố định trích từ tập GPQA Diamond. Độ sụt giảm chất lượng ($\Delta$) được tính bằng điểm phần trăm tuyệt đối so với reference baseline chạy bằng trọng số BF16 gốc (mặc định baseline đạt 40%).

$$\Delta = \text{baseline\_accuracy} - \text{GPQA\_accuracy\_của\_đội}$$
_(Trong đó, baseline_accuracy là điểm reference accuracy của mô hình gốc chạy bằng trọng số BF16)._ Dựa trên độ sụt giảm $\Delta$, hệ thống áp dụng hàm phạt $f(\Delta)$ (Accuracy decay function) — một hàm bậc nhất từng đoạn (piecewise linear) với giá trị đầu ra thuộc đoạn $[0, 1]$, quy định mức độ trừ điểm vào tổng điểm cuối cùng:

$$
f(\Delta) = \begin{cases}
1.0 & \text{khi } \Delta \le 10 \\
1.0 - \frac{\Delta - 10}{6} & \text{khi } 10 < \Delta < 16 \\
0.0 & \text{khi } \Delta \ge 16
\end{cases}
$$

**Điểm số cuối cùng** của mỗi đội được tính bằng cách kết hợp điểm hiệu năng phục vụ (ERS) với hình phạt sụt giảm chất lượng (Accuracy drop):

$$Score = 100 \times ERS \times f(\Delta)$$

Trong đó:

- **ERS (Effective Request Score):** Điểm số trung bình đánh giá hiệu năng xử lý request trên toàn bộ trace (đã mô tả ở phần ERS).
- **$f(\Delta)$:** Hệ số phạt dựa trên mức sụt giảm độ chính xác.

## 3. 🛠️ Không gian Tối ưu (Optimization Scope)

Thí sinh chỉ được sử dụng framework vLLM (hệ thống chấm bài tự động ép buộc entrypoint của vLLM và không hỗ trợ/tương thích các framework khác như SGLang, LMDeploy, Aphrodite, v.v.) và áp dụng mọi kỹ thuật tối ưu hóa miễn không vi phạm luật thi. Các hướng tiếp cận cốt lõi bao gồm:

- **Quantization:** Tối ưu hóa dung lượng trọng số (Weight quantization) thông qua FP8 (F8_E4M3), INT8, INT4, mixed-precision, AWQ, GPTQ; Tối ưu hóa kích hoạt (Activation quantization, Dynamic quantization).
- **KV Cache & Memory:** Tối đa hóa lượng request xử lý đồng thời bằng Paged Attention; KV cache quantization (FP8, INT8); Prefix caching và Semantic caching; Offloading xuống CPU/NVMe.
- **Serving & Scheduling:** Ứng dụng Dynamic/Continuous batching; Speculative decoding (với draft model hoặc self-speculative); Memory-aware scheduling.
- **System & Runtime:** Viết custom CUDA/Triton kernels; Tích hợp Fused attention kernels (FlashAttention, FlashInfer); Tối ưu hóa memory layout và CUDA Graphs.

## 4. 📦 Quy trình & Quy chuẩn Nộp bài (Submission)

### Quy trình thực hiện (Workflow)

1. **Develop & Package:** Thí sinh phát triển code giải pháp, tối ưu hệ thống và đóng gói toàn bộ thành một Docker Image.
2. **Push Image:** Đẩy (Push) Docker Image hoàn chỉnh lên Docker Hub cá nhân hoặc tổ chức dưới dạng công khai (Public).
3. **Submit:** Thí sinh truy cập hệ thống Portal của BTC, gửi file cấu hình `docker-compose.yml` (trong đó có khai báo chính xác đường dẫn Image trên Docker Hub và lệnh thực thi).
4. **Automated Evaluation:** Hệ thống tự động pull Image từ Docker Hub về, dựng container trên 1 instance MiG H200 (18GB VRAM), kiểm tra trạng thái hoạt động (Healthcheck) và tiến hành chạy benchmark tự động.
5. **Leaderboard:** Kết quả và log trả về trong khoảng 15 phút; Bảng xếp hạng tự động cập nhật.

### Tài nguyên & Baseline

- **File trace cho phase 1 vòng online:** `trace-round1.jsonl`
- **Docker image baseline:** `https://hub.docker.com/layers/vllm/vllm-openai/v0.22.1/images/sha256-55c9bcee9fc66644b139fddae8a7a03e4c0c8a25ab5c64b0ce614554a8abf5d5`

### File `docker-compose.yml` mẫu

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
      - --served-model-name=Qwen3.5-2B #Don't change this to vllm-server
      - --host=0.0.0.0 #Don't change this to vllm-server
      - --port=8000 #Don't change this to vllm-server
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
