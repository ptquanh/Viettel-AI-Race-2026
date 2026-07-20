# BÁO CÁO THỬ NGHIỆM SLOT 6 - NGÀY 20/07 (0917 - SUCCESS)

## 1. Thông tin cấu hình

- **File nộp**: `0917-docker-compose.yml` (Slot 6 ngày 20/07)
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v4`
- **Cấu hình chính**: `Seqs=32`, `MaxModelLen=32768` (Golden Base 32K), `Compilation Level 3`, `Quant=fp8`, **Deep Warmup (Profile-Guided)**
- **Thời gian nộp**: 09:17 (20/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Điểm số cuối cùng (Final Score)**: **61.11 điểm**
- **TTFT P50**: **47 ms**
- **TTFT P95**: **69 ms**
- **TPOT (tbt_median_ms)**: **4 ms**
- **Failed Requests**: **5 requests**
- **Accuracy Drop / Penalty**: `0` / `1.0`

## 3. Phân tích nguyên nhân & Đánh giá Kỹ thuật

1. **Hiệu quả của Deep Warmup**:
   - TTFT P95 giảm rất ấn tượng xuống **69 ms** (so với 95ms của các bản trước).
   - Điểm số tiệm cận kỷ lục (61.11 điểm).
2. **Phát hiện lỗi Load Balancer Race Condition**:
   - `api_server.py` của vLLM khởi động trả về `200 OK` cho endpoint `/health` quá sớm.
   - Kubernetes Readiness Probe của BTC thấy `200 OK` đã lập tức gửi load thực tế trong khi `deep_warmup.py` vẫn đang thực thi ở background.
   - Sự cạnh tranh tài nguyên này khiến 5 requests đầu tiên bị Timeout và kéo TTFT P50 ở mức 47ms.
3. **Giải pháp khắc phục cho v4.1**:
   - Tiêm Middleware FastAPI hoãn `/health` trả về `503 Service Unavailable` cho đến khi `deep_warmup.py` hoàn thành 100%.
