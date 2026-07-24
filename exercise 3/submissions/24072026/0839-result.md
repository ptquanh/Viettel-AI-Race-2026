# Kết Quả Thử Nghiệm 0839 (Slot 01 - 24/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `0839`
- **File Compose**: `01-docker-compose.yml` (Slot 01)
- **Thời gian chấm**: 24/07/2026 (08:39)
- **Thay đổi**: Image v14 + `VLLM_QUANTIZATION=bitsandbytes` (INT4 Runtime Probe)

## Kết Quả Chấm Điểm

- **Điểm số**: `29.7100`
- **TTFT P50**: 94ms
- **TTFT P95**: 132ms
- **TPOT (TBT Median)**: 14ms (Tăng mạnh từ 4ms lên 14ms!)
- **Số request lỗi (Failed count)**: 9
- **Penalty**: 1
- **Accuracy Drop**: 0% (Chính xác tuyệt đối 100%)

## Phân Tích & Kết Luận

- **Overhead Dequantization quá lớn**: Chi phí giải nén INT4 sang FP16/BF16 runtime trên CUDA Cores của `bitsandbytes` quá cao, khiến TPOT tăng vọt từ 4ms lên 14ms (vượt trần 10ms của BTC), làm điểm ERS sụt giảm thảm hại xuống 29.71đ.
- **Điểm sáng duy nhất**: Độ chính xác giữ nguyên 100% (`accuracy_drop=0`).
- **Quyết định Gate**: Hủy bỏ ngay lập tức các slot thử nghiệm `bitsandbytes` (Slot 02, Slot 04). Chuyển sang Phase 2 & thử nghiệm Merge Best CLI Config (Slot 03).
