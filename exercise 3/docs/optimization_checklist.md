# 🚀 TỔNG HỢP & KIỂM KÊ KỸ THUẬT TỐI ƯU HÓA LFM2.5 (BÀI 3)

> **Cập nhật lần cuối**: 20/07/2026  
> **Mục tiêu**: Bứt phá 70+ điểm ERS (vLLM v0.22.1 trên MiG H200 18GB)

Tài liệu này đóng vai trò như một bản đồ chiến thuật, ghi nhận tất cả các kỹ thuật tối ưu hóa có thể áp dụng cho vLLM, trạng thái hiện tại của chúng trên mô hình Liquid Foundation Model (LFM2.5), và những ranh giới cấm không được vi phạm.

---

## 🟢 1. CÁC KỸ THUẬT ĐÃ ÁP DỤNG THÀNH CÔNG (GOLDEN BASE)

_Đây là bộ khung cấu hình đã được chứng minh thực tế mang lại kỷ lục 61.13 điểm._

- [x] **FP8 Native Quantization (`VLLM_QUANTIZATION=fp8`)**: Kéo TPOT từ 6ms xuống 4ms và giảm một nửa VRAM footprint. Kỹ thuật quan trọng nhất.
- [x] **Torch Compile Cấp Độ 3 (`VLLM_COMPILATION_LEVEL=3`)**: Kích hoạt PyTorch Dynamo JIT Graph sâu nhất. Kéo TTFT P50 từ ~100ms xuống còn ~45ms.
- [x] **Tối ưu Hàng Đợi Scheduler (`VLLM_MAX_NUM_SEQS=32`)**: Điểm "Sweet-spot" lý tưởng nhất. Nếu giảm (<32) sẽ làm nghẽn hàng đợi (TTFT vọt lên 75ms). Nếu tăng (48) sẽ gây tranh chấp compute.
- [x] **Tối ưu Context Buckets (`VLLM_MAX_MODEL_LEN=32768`)**: Giữ nguyên độ dài ngữ cảnh gốc giúp vLLM block allocator và CUDA Graph không bị phân mảnh. Hạ xuống 8K hay 16K đều làm trễ TTFT.
- [x] **Tối ưu hóa GPU Memory (`VLLM_GPU_MEMORY_UTILIZATION=0.95`)**: Cân bằng hoàn hảo giữa sức chứa KV Cache và không gian VRAM dành cho PyTorch overhead.
- [x] **Kích hoạt Prefix Caching (`--enable-prefix-caching`)**: Bắt buộc phải có để tái sử dụng 1000 tokens System Prompt chung trong Trace.
- [x] **Vô hiệu hóa toàn bộ IO Overhead (`VLLM_LOGGING_LEVEL=WARNING`, `--no-enable-log-requests`)**: Tránh CPU/IO block trong quá trình serving áp lực cao.
- [x] **Triệt tiêu tranh chấp CUDA Stream (`CUDA_DEVICE_MAX_CONNECTIONS=1`)**: Chống thắt cổ chai dòng lệnh trên GPU (Xóa bỏ 5-6 request failed).

---

## 🟡 2. CÁC KỸ THUẬT ĐANG & SẮP ÁP DỤNG (CHIẾN THUẬT BỨT PHÁ)

_Những "Đòn Bẩy" mới nhất đang được thử nghiệm trong các Slot ngày 20/07 nhằm tấn công mốc 70+ điểm._

- [/] **Gộp bước Decode đa luồng (`VLLM_NUM_SCHEDULER_STEPS=8`)**: Bỏ qua overhead của scheduler giữa các bước sinh token, nén thời gian sinh từ 4ms xuống hi vọng chạm mốc 3ms (Đang test ở Slot 10 & 11).
- [ ] **FlashInfer Attention Backend (`VLLM_ATTENTION_BACKEND=FLASHINFER`)**: Thay thế FlashAttention mặc định bằng FlashInfer (tối ưu cực tốt cho batch-size nhỏ), mục tiêu kéo TTFT P50 xuống dưới 40ms (Chuẩn bị ở Slot 12).
- [/] **Lean Image / Tận dụng BTC Primer (Image v7)**: Không tự JIT warmup cồng kềnh, mà để 90 request "primer" đầu tiên của BTC tự động làm mồi nhử cho Torch Compile, giúp server khởi động siêu tốc.

---

## 🔴 3. CÁC KỸ THUẬT ĐÃ THỬ NHƯNG THẤT BẠI (KHÔNG ÁP DỤNG)

_Đã chứng minh qua thực nghiệm là gây tác dụng ngược (trễ hơn, lỗi, hoặc timeout) trên LFM2.5._

- [x] ❌ **Custom Triton Kernels (RMSNorm + Conv1D + SiLU)**: Điểm nghẽn TPOT là Băng thông bộ nhớ (Bandwidth bound) 600GB/s của H200, không phải năng lực tính toán. Kernel fusion sinh ra thêm trễ JIT mà không giảm được ms nào.
- [x] ❌ **Deep Warmup bằng Python Hijack**: Trì hoãn Load Balancer (trả 503) làm hỏng nhịp "primer warmup" tự nhiên của BTC, khiến TTFT P50 tăng lên.
- [x] ❌ **Speculative Decoding (Draft Model 350M)**: vLLM v0.22.1 chưa hỗ trợ spec-decode chính thức cho họ mô hình LFM2.5 Recurrent. Engine lỗi ngay lúc khởi động.
- [x] ❌ **Speculative Decoding (N-gram Prompt Lookup)**: Vòng lặp N-gram matching xung đột chí mạng với `COMPILATION_LEVEL=3` (Torch Dynamo JIT) gây deadlock timeout toàn bộ server.
- [x] ❌ **Chunked Prefill (`--enable-chunked-prefill`)**: Phá vỡ tính liên tục của lớp Recurrent (LFM2.5 dựa vào hidden state liền mạch), làm TTFT tăng mạnh (P50 > 90ms).
- [x] ❌ **Torch Inductor Max Autotune (`TORCHINDUCTOR_MAX_AUTOTUNE=1`)**: Tính năng compile tốn quá nhiều overhead runtime autotuning, ép TTFT tăng vọt lên 64ms.
- [x] ❌ **Lượng tử hóa KV Cache (`VLLM_KV_CACHE_DTYPE=fp8`)**: Sinh ra overhead ép kiểu (de-quantization) mỗi lần decode, gây trễ. Mặc định fp16 đã tốt nhất.

---

## 🛑 4. DANH SÁCH "VÙNG CẤM" (QUY ĐỊNH BTC - ANTI-CHEATING)

_Nghiêm cấm áp dụng dưới mọi hình thức (Vi phạm = Loại trực tiếp)._

- 🚫 **Pre-Bake / Hardcode Kết Quả**: Cấm ghi đè, đoán trước output để trả lời nhanh mà không chạy model.
- 🚫 **Chạy Mô Hình Phụ / Dual-Path**: Cấm sử dụng model nhỏ chạy song song để bypass LFM2.5.
- 🚫 **External Network Calls**: Server cấm gửi request ra ngoài internet, Docker environment của BTC hoàn toàn cô lập.
- 🚫 **Can Thiệp Tokenizer / Trọng Số Mô Hình (Weights)**: Cấm thay thế file checkpoint gốc hoặc đổi tokenizer nhằm lách chuẩn đánh giá chất lượng (GPQA Diamond).
- 🚫 **Tráo Đổi Docker Image Sau Chấm**: Image nộp bài phải khóa cứng (hash) và được dùng trực tiếp cho vòng Offline Audit. Cấm trick backdoor load script độc hại.
- 🚫 **Cố Tình Gây Lỗi Tràn RAM/Gaming SLO**: Cố tình return rỗng để pass các requests lớn nhằm nâng điểm ERS ảo. BTC sẽ có hình phạt $f(\Delta)$ và penalty cho hành vi này.

---

> 📝 **Lưu ý triển khai (20/07):** Hiện tại chúng ta đang tập trung toàn bộ nguồn lực vào **Nhóm 2 (Vàng)**. Mọi thứ ở Nhóm 1 đã được chuẩn hóa trong `10-docker-compose.yml` trở đi. Tuyệt đối không thêm lại các cờ ở Nhóm 3.
