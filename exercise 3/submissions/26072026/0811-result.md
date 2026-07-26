# Kết quả thử nghiệm Slot 03 (08:11) - Ngày 26/07 - PyTorch Max Autotune

## 1. Thông tin chung

- **Thời gian chấm**: 26/07/2026 08:11
- **Submission File**: `exercise 3/submissions/26072026/0811-docker-compose.yml`
- **Cấu hình**: Image v14 (FP8) + `COMPILATION_LEVEL=3` + `TORCHINDUCTOR_MAX_AUTOTUNE=1`
- **Điểm số**: **57.2400đ**

## 2. Chi tiết chỉ số

- **ERS**: 57.24
- **Total Requests**: 420
- **Failed Requests**: 5
- **TTFT P50**: 60 ms
- **TTFT P95**: 88 ms
- **TBT (TPOT) Median**: 4 ms
- **Tokens/sec**: 0.0579

## 3. Phân tích & Đánh giá (Giới hạn của FP8)

1. **Autotune Vô Tác Dụng**: Dù PyTorch đã dốc toàn lực compile các kernel C++/Triton bằng chế độ Max Autotune, TPOT vẫn kẹt cứng ở 4ms. Điều này chứng tỏ nút thắt cổ chai không nằm ở mặt tính toán (Compute-bound) mà nằm ở **Băng thông bộ nhớ (Memory Bandwidth-bound)**.
2. **TTFT tăng**: Quá trình compile/autotune nặng nề có vẻ để lại một chút overhead trong khâu khởi tạo/dispatch kernel, khiến TTFT P50 vọt lên 60ms (điểm tụt xuống 57.24đ so với mức 60đ chuẩn).

## 4. Hành động tiếp theo (The Final Weapon)

- **Kết luận**: Định dạng weights **FP8 (8-bit)** dù đã tối ưu đến mức nào cũng không thể đọc VRAM nhanh hơn 4ms/token trên kiến trúc phần cứng và framework hiện tại. Chúng ta đã đụng trần băng thông vật lý của FP8.
- **Kích hoạt Kế hoạch Z1 (INT4 Quantization)**: Lên nòng cho Slot 04. Chúng ta sẽ dùng Image `vllm_lfm25_int4_online_v15` (sử dụng `torchao` hoặc kernel AWQ/Marlin) để ép weights xuống **4-bit**. Lượng dữ liệu cần đọc từ VRAM sẽ giảm đi chính xác một nửa. Đây là con đường duy nhất còn lại để TPOT phá thủng mốc 4ms xuống 2ms!
