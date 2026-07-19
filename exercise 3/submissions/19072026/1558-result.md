# BÁO CÁO THỬ NGHIỆM SLOT 10 (1558 - SUCCESS)

## 1. Thông tin cấu hình

- **File nộp**: `1558-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Cấu hình chính**: `Seqs=32`, `Len=32768`, `VLLM_COMPILATION_LEVEL=3` (`mode: 3`), `Quant=fp8`, `Warmup=1`, `Custom_Kernel=1`
- **Thời gian nộp**: 15:58 (19/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Điểm số cuối cùng (Final Score)**: **60.75 điểm**
- **TTFT P50**: **48 ms**
- **TTFT P95**: **76 ms**
- **TPOT (tbt_median_ms)**: **4 ms**
- **Failed Requests**: **4 requests** (Giảm xuống mức THẤP NHẤT từ trước đến nay!)
- **Accuracy Drop / Penalty**: `0` / `1.0`

## 3. Phân tích kết quả & Đánh giá

1. **Xác nhận tính ổn định của Image v2**: Bản Image `v2` với `COMPILATION_LEVEL=3` (`{"mode": 3}`) đã chính thức chạy thành công 100% trên hệ thống grader BTC.
2. **Độ tin cậy cực cao**: Số request bị lỗi giảm xuống chỉ còn **4 requests** (so với 6 requests ở mốc 61.13đ và 7 requests ở mốc 60.91đ), khẳng định torch.compile level 3 trên v2 vận hành cực kỳ ổn định.
3. **Mốc Baseline v2 hoàn hảo**: 60.75 điểm chính thức trở thành mốc Baseline đối chứng tuyệt đối cho các thử nghiệm đơn biến nâng cao tiếp theo (N-gram Speculative, Chunked Prefill 4K, Compressed Tensors).
