---
tags:
  -  #ViettelAIRace2026
  -  #LLM
  -  #Inference_Optimization
  -  #ActionPlan
status: 🚀 Active
date: 2026-07-03
---

# 🗺️ Kế hoạch Hành động Bài 3 (Vòng 1) - Hybrid Workflow

**Mục tiêu:** Qwen/Qwen3.5-2B (BF16).
**Hạ tầng BTC:** MiG H200 (18GB VRAM / 3 CPU cores / 8GB RAM).
**Deadline:** 30/07/2026 (Còn 27 ngày).
**Chiến lược cốt lõi:** Hybrid Workflow (Local Hardening + BTC A/B Testing Đơn biến).

## 1. ⚙️ Triết lý Vận hành (The Pipeline)

Thay vì phó mặc hoàn toàn cho local hoặc BTC, luồng làm việc sẽ được chia tách rõ ràng để tối đa hóa hiệu suất của 5 slot submit/ngày (cooldown 600s):

- **Tối ưu Docker (Chỉ build khi cần):** Không build nhiều image nếu chỉ thay đổi tham số cấu hình. Dùng 1 base image (chứa weights + runtime) và ghi đè tham số qua `command` trong `docker-compose.yml`.
- **Local (Máy có GPU bất kỳ):** Đóng vai trò màng lọc khắt khe. Phải verify container khởi động thành công, gọi API `/v1/completions` trả về đúng, không OOM với giới hạn `--cpus=3 --memory=8g`, và pass bài smoke test về độ trễ.
- **BTC Portal (Hạ tầng thật):** Môi trường A/B Test đơn biến. Mỗi slot submit chỉ thay đổi **DUY NHẤT 1 BIẾN** để dễ dàng truy vết nguyên nhân tăng/giảm ERS.

## 2. 📝 Nguyên tắc sử dụng 5 Slot/Ngày

Tuyệt đối tuân thủ kỷ luật thử nghiệm đơn biến để chống lại việc BTC không trả về log chi tiết:

- **Slot 1 (Reference):** Chạy lại config tốt nhất hiện tại làm mốc so sánh.
- **Slot 2 (Test Biến A):** Ví dụ thay đổi `--max-num-seqs`.
- **Slot 3 (Test Biến B):** Ví dụ thay đổi `--max-num-batched-tokens`.
- **Slot 4 (Test Biến C):** Ví dụ thay đổi `--num-scheduler-steps`.
- **Slot 5 (Verify / Edge case):** Chạy lại config thắng cuộc hoặc test một edge case cụ thể.

## 3. 🗓️ Lộ trình 27 Ngày Thực thi

### Tuần 1 (03/07 – 09/07): Setup Pipeline & Baseline (Strict BTC Version)

_Mục tiêu: Thiết lập luồng CI/CD dựa trên image v0.22.1 của BTC và thăm dò hệ thống log._

- **Ngày 1–2:** Tải weights Qwen3.5-2B (BF16) về máy. Viết Dockerfile kế thừa `FROM vllm/vllm-openai:v0.22.1` và `COPY` weights vào thư mục `/model`.
- **Ngày 3:** Viết script `build.sh` tự động build image và push lên Docker Hub. Khởi động file `docker-compose.yml` (giữ nguyên các rule cấm sửa của BTC) ở môi trường local.
- **Ngày 4 (Local hardening):** Gọi thử API `/v1/completions` vào server local vừa dựng để chắc chắn `v0.22.1` tương thích tốt với Qwen3.5-2B và không sinh lỗi lạ.
- **Ngày 5 (BTC Submit 1–2):** Nộp bản BF16 gốc với `docker-compose.yml` mẫu của BTC (chỉ đổi đường dẫn `image` của bạn). Xác định xem BTC trả về những log gì (ERS tổng hay có chi tiết TTFT/TPOT).
- **Ngày 6 (BTC Submit 3–5):** Test nhẹ độ nhạy của hệ thống bằng cách ghi đè biến `--gpu-memory-utilization` (chỉnh 0.90 vs 0.95) thông qua block `command`.
- **Ngày 7:** Phân tích trace data + kết quả submit Tuần 1. Chốt kế hoạch đóng gói weights FP8 cho Tuần 2.

### Tuần 2 (10/07 – 16/07): Quantization + KV Cache

_Mục tiêu: Đẩy giới hạn phần cứng với FP8._

- **Ngày 8–9:** Build image chứa weights **FP8**. Chạy Local sanity check cực căng.
- **Ngày 10 (BTC Slot):** A/B Test trực tiếp: BF16 vs FP8 weights (giữ nguyên toàn bộ flags). So sánh ERS và Accuracy.
- **Ngày 11–12:** Nếu FP8 thắng và Accuracy an toàn, dùng slot BTC để test bật/tắt **FP8 KV Cache** (`--kv-cache-dtype fp8`). Chốt KV cache config.
- **Ngày 13–14:** Thử nghiệm bật/tắt **CUDA graphs** và **chunked prefill**.
- **Ngày 15:** Trừ hao rủi ro: Nếu FP8 làm Accuracy drop > 3%, bắt đầu test INT8 SmoothQuant làm phương án dự phòng.
- **Ngày 16:** Review Tuần 2. Đóng băng "Reference Config" mới nhất.

### Tuần 3 (17/07 – 23/07): Scheduling + CPU Optimization

_Mục tiêu: Giải quyết triệt để nút thắt cổ chai 3 CPU Cores._

- **Ngày 17–19:** Grid search trên hạ tầng BTC các tham số batching: `max-num-seqs` × `max-num-batched-tokens`.
- **Ngày 20–21:** Bắt đầu ép CPU overhead: Test `--num-scheduler-steps` (1, 4, 8, 12) và ép luồng xử lý (`OMP_NUM_THREADS=1` vs default).
- **Ngày 22:** Kiểm tra lại Trace file. Nếu có shared prefix rõ ràng, test bật **Prefix caching**. Nếu không, bỏ qua để tiết kiệm CPU.
- **Ngày 23:** Chốt toàn bộ cấu hình tối ưu (Final Candidate Config).

### Tuần 4 (24/07 – 30/07): Variance + Final Submission

_Mục tiêu: Kiểm chứng độ ổn định và nộp bài an toàn._

- **Ngày 24–25:** Submit Final Candidate 3–5 lần vào các khung giờ khác biệt trong ngày để vẽ biểu đồ phân phối ERS/Accuracy (Variance check). Đảm bảo không bị ảnh hưởng bởi "hàng xóm" trên cùng server vật lý.
- **Ngày 26:** Backup plan: Chuẩn bị sẵn 1 phiên bản cực kỳ an toàn (vd: BF16 thuần) đề phòng FP8 có variance quá cao, lúc ăn lúc xịt.
- **Ngày 27:** Clean up code, rà soát lại docker-compose, image tags, command override. Không để sót bug ngớ ngẩn.
- **Ngày 28–29:** Buffer time. Xem xét kỹ variance của bản Final Candidate. Nếu rủi ro cao, chốt nộp bản Backup.
- **Ngày 30:** **Submit Final.**
