# BÁO CÁO THỬ NGHIỆM SLOT 12 (2101 - SUCCESS)

## 1. Thông tin cấu hình

- **File nộp**: `2101-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Cấu hình chính**: `Seqs=32`, `Len=32768`, `Compilation Level 3`, `Chunked_Prefill=1`, `Chunk_Size=4096`
- **Thời gian nộp**: 21:01 (19/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Điểm số cuối cùng (Final Score)**: **59.21 điểm**
- **TTFT P50**: **54 ms**
- **TTFT P95**: **83 ms**
- **TPOT (tbt_median_ms)**: **4 ms**
- **Failed Requests**: **7 requests**
- **Accuracy Drop / Penalty**: `0` / `1.0`

## 3. Phân tích nguyên nhân & Kết luận kỹ thuật

1. **Tác động của Chunked Prefill lên kiến trúc Recurrent LFM2.5**:
   - Khác với Transformer chuẩn, LFM2.5 có các lớp tính toán tuần hoàn (Recurrent layers). Việc bật `Chunked Prefill` làm chia nhỏ giai đoạn prefill thành nhiều chunk step làm tăng overhead lập lịch CPU-GPU và phát sinh thêm các lệnh gọi kernel launch.
   - Trễ TTFT P50 bị tăng từ 48ms (ở mốc Baseline Slot 10) lên 54ms, TTFT P95 tăng từ 76ms lên 83ms.
2. **Bài học định hướng**:
   - **Không bật Chunked Prefill cho LFM2.5** khi context length nằm trong mức 32K. Chế độ Prefill mặc định (Non-chunked) giúp LFM2.5 duy trì TTFT P50 48ms và độ ổn định cao hơn (4 failed vs 7 failed).
