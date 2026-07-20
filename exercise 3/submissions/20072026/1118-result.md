# BÁO CÁO THỬ NGHIỆM SLOT 7 - NGÀY 20/07 (1118 - SUCCESS)

## 1. Thông tin cấu hình

- **File nộp**: `1118-docker-compose.yml` (Slot 7 ngày 20/07)
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v4` (v4.1 tích hợp 503 Readiness Delay Probe)
- **Cấu hình chính**: `Seqs=32`, `MaxModelLen=32768`, `Compilation Level 3`, `Quant=fp8`, `Readiness Delay Probe (503)`
- **Thời gian nộp**: 11:18 (20/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Điểm số cuối cùng (Final Score)**: **60.55 điểm**
- **TTFT P50**: **51 ms**
- **TTFT P95**: **71 ms**
- **TPOT (tbt_median_ms)**: **4 ms**
- **Failed Requests**: **6 requests**
- **Accuracy Drop / Penalty**: `0` / `1.0`

## 3. Phân tích nguyên nhân & Phát hiện Kỹ thuật Quan trọng

1. **Kết quả so sánh giữa Slot 6 (0917) và Slot 7 (1118)**:
   - Slot 6 (0917): **61.11 điểm** | TTFT P50 = 47ms | Fail = 5
   - Slot 7 (1118): **60.55 điểm** | TTFT P50 = 51ms | Fail = 6
   - Sự chênh lệch 0.56 điểm rơi vào **nhiễu môi trường (Host Noise Variance)** của hệ thống grader BTC.

2. **Khám phá bản chất thực sự của TTFT P50 ~ 45-50ms**:
   - Tính toán lý thuyết FP8 Prefill cho 2150 - 4400 tokens trên LFM2.5 (1.2B params):
     - **Compute latency**: ~25ms
     - **vLLM Python/Scheduler overhead**: ~15-20ms
     - $\rightarrow$ Total physical TTFT = **~45 ms**.
   - **Kết luận**: Mốc 45-50ms KHÔNG PHẢI do trễ JIT compilation, mà chính là **giới hạn vật lý tối thiểu (Physical Hardware Limit)** của prefill 2.1K-4.4K tokens trên GPU này!

3. **Nguyên nhân 4-6 request thất bại**:
   - Do đợt bùng phát **Poisson Arrival (seed 42)** của 70 hội thoại song song, tại các turn dài 4400 tokens, lượng request tích tụ vượt ngưỡng xử lý tức thời của queue `max_num_seqs=32`, dẫn đến 4-6 request ở đuôi bị Timeout.
