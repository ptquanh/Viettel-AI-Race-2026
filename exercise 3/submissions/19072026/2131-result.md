# BÁO CÁO THỬ NGHIỆM SLOT 14 (2131 - FAIL ERROR)

## 1. Thông tin cấu hình
- **File nộp**: `2131-docker-compose.yml` (Slot 14)
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Cấu hình chính**: `Seqs=32`, `Len=32768`, `Compilation Level 3`, `VLLM_QUANTIZATION=compressed-tensors`
- **Thời gian nộp**: 21:31 (19/07/2026)

## 2. Kết quả chấm từ BTC Portal
- **Trạng thái**: **Chấm điểm thất bại (FAILED)**
- **Lỗi chi tiết**: `TypeError: CompressedTensorsConfig.__init__() missing 3 required positional arguments: 'target_scheme_map', 'ignore', and 'quant_format'`

## 3. Phân tích nguyên nhân gốc & Đánh giá
1. **Xác nhận bản chất bộ weights `/model` của BTC**:
   - vLLM yêu cầu file `config.json` của checkpoint mô hình phải chứa sẵn cấu hình lượng tử hóa `compressed-tensors` (`quantization_config`).
   - Checkpoint `LFM2.5-1.2B-Instruct` mà BTC đặt sẵn tại `/model` là định dạng FP8 Native. Do đó, khi ta ép cờ `compressed-tensors`, vLLM khởi tạo `CompressedTensorsConfig()` nhưng bị thiếu metadata và crash ngay tại dòng khởi động `api_server.py`.
2. **Khẳng định VỊ THẾ TỐI ƯU TUYỆT ĐỐI CỦA FP8 NATIVE**:
   - Thử nghiệm này giải mã lý do tại sao ở Image v1 (STT 50 - 61.13đ), cờ `compressed-tensors` bị v1 hijack bỏ qua nên vLLM chạy dưới dạng **FP8 Native**.
   - **FP8 Native (`VLLM_QUANTIZATION=fp8`) là cấu hình duy nhất tương thích 100% và đạt hiệu năng đỉnh cao nhất (60.75đ - 61.13đ)** trên bộ weights của BTC!
