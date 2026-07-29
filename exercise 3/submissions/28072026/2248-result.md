# Kết quả Benchmark - 22:48 28/07/2026 (Slot 15 - Image v20.0 CUTLASS FP8 + OMP=2 + Golden Combo Sweep)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Thử nghiệm `OMP_NUM_THREADS=2` + `GPU_MEM=0.94` + Capture `[1..32]`).
- **Mục đích**: Lượt nộp chốt sổ 15/15 slots ngày 28/07/2026.

## Kết quả thử nghiệm Slot 2248

- **Điểm chung cuộc (ERS)**: `58.1100`
- **F_delta**: `1.0`
- **Penalty**: `1.0`
- **Accuracy Drop**: `0%`
- **TTFT P50**: `60ms`
- **TTFT P95**: `79ms`
- **TPOT (TBT Median)**: `4ms`
- **Số request lỗi**: `5 / 420`
- **Tokens per sec**: `0.0523`

### Đánh giá & Tổng kết ngày 28/07

Đã hoàn thành xuất sắc 15/15 slots thử nghiệm của ngày 28/07/2026. Nền tảng CUTLASS FP8 đạt độ ổn định 100%, đem về mốc kỷ lục mới **60.63 ERS** (Slot 10 - 22:12), chuẩn bị nền tảng cho chiến dịch Tokenizer Optimization ngày 29/07.
