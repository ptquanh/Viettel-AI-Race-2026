# Kết quả Benchmark - 15:59 28/07/2026 (Slot 08 - v20.0 CUTLASS FP8 Record Baseline + Expanded CUDA Graph Capture)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0` (Loại bỏ toàn bộ sitecustomize hook không ổn định, sử dụng CUTLASS FP8 Scaled MM Kernel + CUDA Graph Capture sizes mở rộng `[1,2,4,8,16,24,32,48]`).
- **Mục đích**: Chấm dứt chuỗi lỗi crash Engine Core, thiết lập kỷ lục điểm số mới dựa trên nền tảng CUTLASS FP8 tối ưu nhất.

## Kết quả thử nghiệm Slot 1559

🔥 **KỶ LỤC MỚI VÒNG 2: 60.5000 ERS!**

- **Điểm chung cuộc (ERS)**: `60.5000`
- **F_delta**: `1.0`
- **Penalty**: `1.0`
- **Accuracy Drop**: `0%`
- **TTFT P50**: `52ms`
- **TTFT P95**: `74ms`
- **TPOT (TBT Median)**: `4ms`
- **Số request lỗi**: `4 / 420` (Thấp kỷ lục toàn giải!)
- **Tokens per sec**: `0.0530`

### Đánh giá & Kết luận

- **Phục hồi & Thiết lập Kỷ lục**: Việc khôi phục Image v20.0 (CUTLASS FP8) hoàn toàn đúng đắn, chấm dứt 100% rủi ro crash container và ngay lập tức đem về kỷ lục điểm số mới **60.50đ**.
- **Tối ưu TTFT & Cân bằng Error**: Việc mở rộng capture sizes `[1,2,4,8,16,24,32,48]` giúp giữ vững TTFT P50 ở mức 52ms, duy trì số request lỗi ở mức tối thiểu (chỉ 4/420 requests).
