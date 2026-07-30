# Kết quả Benchmark - 21:01 30/07/2026 (STT 211 - Slot 2056 - CUDA Graph V2)

- **Cấu hình**: Base 0851 + V2 Runner + CUDA Graph FULL Mode + gpu_memory 0.90 (Slot 3.2).
- **Mục đích**: Dùng CUDA Graph triệt tiêu CPU overhead để ép TPOT xuống < 2.5ms.

## Chỉ số đo được

- **Điểm số**: **61.97 ERS** (TỤT ĐIỂM)
- `ttft_p50_ms`: 54ms
- `ttft_p95_ms`: 73ms
- `tbt_median_ms` (TPOT): **4ms** (TĂNG LÊN)
- `failed_count`: 6

### Phân tích

- **Cú sốc lớn**: CUDA Graph và V2 Runner không những không giảm được TPOT mà còn làm nó **TĂNG LÊN** từ 3ms lên 4ms!
- **Nguyên nhân**: Kiến trúc hybrid Mamba-Attention của LFM2.5 sử dụng các trạng thái SSM động (dynamic state). Khi bị ép vào khuôn CUDA Graph cố định, vLLM phải tốn thêm thời gian padding, đồng bộ hóa (synchronization) và luân chuyển state memory, khiến chi phí overhead của đồ thị tĩnh còn cao hơn cả overhead của CPU thông thường (eager mode)!
- **Kết luận tối quan trọng**: Tính năng CUDA Graph là **Negative Optimization (Tối ưu ngược)** đối với LFM2.5! Đường đua giảm TPOT bằng CUDA Graph chính thức là NGÕ CỤT. Trễ vật lý của hardware H200 cho nhân Mamba này chốt cứng ở mức 3ms.

## Kế hoạch 3 slots cuối

Vì không thể giảm TPOT, con đường duy nhất để leo lên 70-75+ là **ÉP TTFT** (Trễ token đầu tiên) và **GIẢM FAILED COUNT về 0**.

- Phải quay lại dùng kiến trúc chuẩn (V2 Runner = 0, Không CUDA Graph).
- Kết hợp Image `phase3` (Hack Scheduler ép TTFT) với bộ cờ an toàn của kỷ lục `1711` (F16Accum giúp triệt tiêu trễ đuôi và giảm fail).
