# 🗺️ Kế hoạch Hành động Tổng thể Vòng 1 — Phase 1 Strategic Master Plan

Tài liệu này đóng vai trò là Bản kế hoạch chiến lược tổng thể (Master Plan) cho Vòng 1 cuộc thi Viettel AI Race 2026, hướng tới mục tiêu tối đa hóa điểm số trên hạ tầng MiG H200 giới hạn.

---

## 1. 🔍 Chẩn đoán Cổ chai Kỹ thuật (HBM Bandwidth)

Phân tích toán học và vật lý về kiến trúc **Qwen3.5-2B** (lai 18 layers linear attention và 6 layers full attention) chỉ ra:

- **Hiện tượng:** TPOT (Time-Per-Output-Token) của baseline BF16 luôn kẹt ở mức **51ms** (vượt quá ngưỡng trần 45ms của BTC, dẫn đến điểm TPOT bằng 0).
- **Nguyên lý cổ chai:** decode step bị giới hạn vật lý bởi băng thông bộ nhớ (HBM bandwidth) khi đọc KV Cache của 6 layers full attention:
  - _Kích thước KV cache/token/layer:_ $2 \times 256 \times 2 \times 2\text{ bytes} = 2,048\text{ bytes}$.
  - _Kích thước KV cache tổng (6 layers):_ $6 \times 2,048 = 12\text{ KB/token}$.
  - _Tổng KV đọc mỗi step (batch ~86 concurrent, context ~30k tokens):_ $86 \times 30k \times 12\text{ KB} \approx 31\text{ GB}$.
  - _Băng thông MiG H200:_ $\approx 685\text{ GB/s}$.
  - _Thời gian đọc KV lý thuyết:_ $31\text{ GB} / 685\text{ GB/s} \approx 46\text{ms}$ (cộng thêm 3ms đọc weights $\approx 49\text{ms}$).
- **Kết luận:** Không thể tối ưu TPOT bằng cách tinh chỉnh tham số scheduler hay đổi attention backend thông thường. Đòn bẩy duy nhất là **giảm dung lượng KV cache cần đọc** (thông qua quantization KV cache hoặc giảm tối đa concurrency).

---

## 2. 🎯 Chiến lược Tối ưu 4 Tầng

Để đạt mốc 70+ và hướng tới 90+ điểm, giải pháp phải can thiệp đồng thời vào cả 4 tầng:

### Tầng 1: Lượng tử hóa KV Cache (KV Cache Quantization) — ⚠️ [ĐANG THỰC NGHIỆM]

- **Mục tiêu:** Giảm kích thước KV cache từ 12KB/token (BF16) xuống còn 6KB (FP8/INT8) hoặc 3KB (INT4).
- **Đột phá:** vLLM v0.22.1 tích hợp cơ chế lượng tử hóa KV cache theo cơ chế per-token-head (`fp8_per_token_head`, `int8_per_token_head`).
- **Custom Kernel:** Nếu cơ chế mặc định của vLLM gây ra overhead CPU quá lớn (như đã thấy ở STT 71-72 khiến TPOT vọt lên 220ms), giải pháp là viết **Custom Triton Kernel** giải nén online ngay trong registers của GPU để triệt tiêu CPU scheduling overhead.
- _Hiện trạng:_ Đã thử nghiệm thành công FP8 KV Cache + Custom Triton Kernel (STT 83) đạt TPOT kỷ lục 31ms (giảm 40%). INT8 KV Cache (STT 82) thất bại do nghẽn tính toán.

### Tầng 2: JIT Warmup via Hijack (Prefix Cache Warmup) — 🔄 [ĐANG CHỜ KẾT QUẢ]

- **Mục tiêu:** Khắc phục tình trạng Triton kernel biên dịch on-the-fly (JIT compilation) lúc prefill đợt đầu làm tăng vọt TTFT (lên tới 2036ms ở STT 83).
- **Giải pháp:** Sử dụng script hijack entrypoint `python3` của vLLM. Sau khi API server khởi động thành công, tự động gửi một dummy request nhỏ trước khi hệ thống chấm bài của BTC bắt đầu. Kernel Triton được compile sẵn giúp đưa TTFT về lại ngưỡng tối ưu (~600ms).
- _Hiện trạng:_ Đã đóng gói vào image `vllm-phase2-fp8-warmup` và cấu hình trong `slot4`. Đang chờ Grader trả kết quả benchmark (STT 89) để xác nhận.

### Tầng 3: Tinh chỉnh Batch Size & Chunked Prefill — ✅ [ĐÃ TRIỂN KHAI]

- **Mục tiêu:** Cân bằng giữa TTFT và TPOT (bài toán tối ưu Pareto).
- **Cấu hình:** Sử dụng `--enable-chunked-prefill` để xen kẽ xử lý prefill và decode, tránh nghẽn luồng.
- **Tham số:** Tinh chỉnh `--max-num-seqs` (giới hạn số request concurrent) và `--max-num-batched-tokens` (kích thước chunk prefill) để giảm tranh chấp tài nguyên GPU.
- _Hiện trạng:_ Đã chạy grid search nhiều mốc chunk size (2048, 4096, 8192) kết hợp điều phối concurrency (seqs 48/64/128/256/512). Chunk size 4096-8192 là tối ưu nhất.

### Tầng 4: Tối ưu hóa Tài nguyên Hệ thống (CPU/RAM Hardening) — ✅ [ĐÃ TRIỂN KHAI]

- **Mục tiêu:** Ngăn chặn hiện tượng nghẽn luồng trên 3 cores CPU được cấp phát.
- **Cài đặt:**
  - Giới hạn CPU threads: Set `OMP_NUM_THREADS=3` (hoặc thấp hơn) để tránh CPU context switching.
  - Tắt logging I/O dư thừa: Sử dụng `--no-enable-log-requests` và `--disable-log-stats`.
  - CUDA Graphs: Luôn bật CUDA Graphs mặc định của vLLM để giảm thiểu thời gian CPU gọi CUDA kernel.
- _Hiện trạng:_ Đã áp dụng triệt để trên tất cả các slot nộp bài từ STT 19/21 trở đi, mang lại độ ổn định cao và giảm jitter.

---

## 3. 📦 Chiến lược đóng gói Docker Image

Để tránh lỗi tràn bộ nhớ (RAM 8GB giới hạn) và đảm bảo tính ổn định:

1.  **Dùng Base Image chuẩn:** Khởi đầu từ `vllm/vllm-openai:v0.22.1` chính thức.
2.  **Đóng gói tinh gọn:** Chỉ cài đặt thêm các thư viện custom kernel cần thiết (như Triton), loại bỏ hoàn toàn các package giám sát hay công cụ thừa thãi.
3.  **Tối ưu hóa dung lượng:** Hạn chế số layer trong Dockerfile, sử dụng cơ chế multi-stage build nếu cần thiết để giữ size image nén dưới 4GB, tăng tốc độ pull của hệ thống BTC.

---

## 4. 🚫 Danh sách Đỏ các cờ bị CẤM (Dead-ends)

Dựa trên dữ liệu từ hàng chục lần submit thử nghiệm, tuyệt đối **không** dùng lại các cấu hình sau:

- `--max-model-len < 65536`: Gây lỗi/cắt cụt token khi prompt chain dài lên tới 42k tokens.
- `--enforce-eager`: Tắt CUDA graphs khiến CPU overhead tăng vọt dưới tải lớn.
- `VLLM_USE_V1=0` (Engine V0): Engine cũ đã bị loại bỏ hoàn toàn trong vLLM v0.22.1.
- `--kv-cache-dtype fp8` (per-tensor kiểu cũ): Khiến TPOT tăng từ 51ms -> 63ms và sụt giảm nghiêm trọng độ chính xác GPQA.
- `Speculative Decoding` (Draft model): Tiêu tốn quá nhiều năng lượng tính toán của 3 core CPU, khiến TTFT tăng gấp 3 lần.
