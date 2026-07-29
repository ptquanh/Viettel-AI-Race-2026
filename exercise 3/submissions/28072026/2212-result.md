# Kết quả Benchmark - 22:12 28/07/2026 (Slot 10 - Image v20.0 CUTLASS FP8 + Seqs=24 Concurrency Tuning)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Đặt `VLLM_MAX_NUM_SEQS=24` nhằm giảm context switching và tranh chấp GPU compute).
- **Mục đích**: Thu hẹp hàng đợi scheduler để ép trễ TTFT P95 xuống mức kỷ lục mới.

## Kết quả thử nghiệm Slot 2212

🔥 **ĐỘT PHÁ KỶ LỤC MỚI BUỔI TỐI: 60.6300 ERS!**

- **Điểm chung cuộc (ERS)**: `60.6300`
- **F_delta**: `1.0`
- **Penalty**: `1.0`
- **Accuracy Drop**: `0%`
- **TTFT P50**: `53ms`
- **TTFT P95**: `69ms` (Ép trễ P95 xuống dưới 70ms!)
- **TPOT (TBT Median)**: `4ms`
- **Số request lỗi**: `5 / 420`
- **Tokens per sec**: `0.0524`

### Đánh giá

Giảm `VLLM_MAX_NUM_SEQS` về 24 mang lại hiệu quả vượt trội, giảm trễ đuôi TTFT P95 xuống **69ms** và đẩy điểm ERS đạt **60.63đ** (điểm số cao nhất buổi tối 28/07)!
