# 🗺️ Kế hoạch Hành động Tổng thể Vòng 1 — Phase 1 Strategic Master Plan (LiquidAI/LFM2.5)

Tài liệu này đóng vai trò là Bản kế hoạch chiến lược tổng thể (Master Plan) cho Vòng 1 cuộc thi Viettel AI Race 2026, hướng tới mục tiêu tối đa hóa điểm số ERS trên mô hình mới **LiquidAI/LFM2.5-1.2B-Instruct** và hạ tầng MiG H200 giới hạn.

---

## 1. 🔍 Chẩn đoán Đặc tính Kỹ thuật & Cổ chai của LFM

Khác với kiến trúc Transformer truyền thống (như Qwen3.5), mô hình **Liquid Foundation Model (LFM)** là một đại diện tiêu biểu của kiến trúc tuần hoàn/state-space model (SSM) thế hệ mới:

- **Độ phức tạp hằng số đối với Context Memory**: LFM nén toàn bộ thông tin ngữ cảnh vào một trạng thái ẩn (recurrent state) có kích thước cố định, thay vì lưu trữ toàn bộ các vector Key-Value như Transformer.
- **Thời gian Decode không phụ thuộc context length**: Do kích thước state cố định, việc đọc "KV Cache" (state) ở mỗi step decode tốn rất ít băng thông bộ nhớ và không tăng lên khi chuỗi dài ra (4k tokens). Điều này giải thích vì sao BTC đặt biên **TPOT Floor cực kỳ ngặt nghèo là 1 ms và Ceiling là 10 ms**.
- **Ưu thế VRAM**: Mô hình 1.2B parameters chỉ chiếm khoảng **2.4 GB** dung lượng ở định dạng BF16 gốc. Với **18 GB VRAM** được MiG H200 cấp phát, bộ nhớ GPU là cực kỳ dư dả. Chúng ta không gặp phải áp lực tràn bộ nhớ VRAM hay ép buộc phải quantization weights như Qwen3.5.

---

## 2. 🎯 Chiến lược Tối ưu hóa 3 Tầng cho LFM

### Tầng 1: Tối ưu hóa Scheduling & Batching (Bóp nghẹt hàng đợi)

Do TTFT Ceiling mới là **400 ms** (siêu nhanh) và TPOT Ceiling là **10 ms**:

- Bất kỳ request nào bị xếp xó trong hàng đợi (queuing delay) quá **400 ms** sẽ nhận ngay **0 điểm** cho TTFT. Với traffic Poisson gồm 70 hội thoại đến đồng thời, kiểm soát hàng đợi là nhiệm vụ sinh tử.
- **Tối ưu hóa Concurrency (`--max-num-seqs`)**: Cần cấu hình `max_num_seqs` đủ lớn để tiếp nhận và xử lý song song các requests turn 0 ngay khi chúng vừa đến, giảm tối đa queuing delay. Tuy nhiên, nếu concurrency quá cao, nó có thể làm tăng TPOT vượt quá ngưỡng 10ms.
- **Tinh chỉnh Prefill Chunk size (`--max-num-batched-tokens`)**: Thiết lập chunk size lớn để giải quyết nhanh phần prefill của các câu hỏi dài (4k tokens) nhằm giải phóng luồng cho decode.

### Tầng 2: Sử dụng Prefix Caching (`--enable-prefix-caching`)

- Do cấu trúc workload là hội thoại multi-turn (6 turns cho mỗi chain), turn sau kế thừa toàn bộ lịch sử turn trước.
- Bật Prefix Caching giúp vLLM lưu trữ recurrent state của các turn trước đó. Khi turn tiếp theo đến, vLLM chỉ cần load lại state cũ và xử lý thêm phần token mới, thay vì tính toán lại từ đầu context 4k tokens. Điều này giúp ép TTFT của turn 1-5 xuống sát mốc **10 ms** (Floor).

### Tầng 3: Tối ưu hóa CPU & OS Runtime

Với hạ tầng 3 Core CPU giới hạn, scheduling overhead của vLLM trên CPU là nhân tố quyết định:

- **CUDA Graphs**: Bắt buộc phải bật để giảm thiểu CPU overhead khi khởi chạy GPU kernels.
- **Thread tuning (`OMP_NUM_THREADS`)**: Tránh tranh chấp luồng và context switching trên 3 cores vật lý bằng cách giới hạn số luồng tính toán CPU thích hợp (thường là 3 hoặc 4).
- **Tắt các tác vụ phụ**: Bật `--no-enable-log-requests` và `--disable-log-stats` để giảm thiểu I/O ghi file trên đĩa gây nghẽn CPU.

---

## 3. 📦 Kế hoạch Triển khai & Kiểm thử Local

1.  **Cập nhật mã nguồn**: Cập nhật script tải model, cấu hình docker-compose và script giả lập benchmark local theo đúng mô hình LFM2.5 và biên latency mới.
2.  **Đo lường Baseline**: Chạy kiểm thử baseline với cấu hình mặc định của BTC trên trace grading public để lấy chỉ số TTFT P50, TPOT Median làm điểm tựa so sánh.
3.  **Grid Search Concurrency**: Thử nghiệm quét các mốc `max_num_seqs` từ 16, 24, 32, 48 để tìm ra điểm cân bằng giữa TTFT (< 400ms) và TPOT (< 10ms).
