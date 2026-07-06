# Kết quả Benchmark - 18:20 06/07/2026 (Slot 9 - max-model-len 131072 Test)

- **Cấu hình**: Baseline mới (STT21: `--enable-chunked-prefill` + `--no-enable-log-requests` + `--quantization=fp8`) + `--max-model-len=131072` (sử dụng image gốc `vllm/vllm-openai:v0.22.1`).
- **Mục đích**: Xác minh xem việc hạ giới hạn độ dài mô hình xuống 131k (vẫn lớn hơn mức 42k tokens thực tế) khi đi kèm quantization weights có cải thiện hiệu năng nhờ tối ưu hóa metadata lưu trữ hay không.

## Chỉ số đo được

- **Điểm số cuối cùng:** **12.74** (ERS = 12.74, Accuracy Drop = 0%, Penalty = 1)
- **Số lượng passed SLO:** **83 / 120** (Giảm từ 85)
- **TTFT P50:** **739 ms** (Tệ hơn nhiều so với 569 ms)
- **TTFT P95:** **12682 ms** (Tệ hơn nhiều so với 8520 ms)
- **TPOT Median (tbt_median):** **68 ms** (Tệ hơn nhiều so với 51 ms)
- **Failed count:** 0
- **Accuracy drop (GPQA Diamond):** **0%** (An toàn tuyệt đối)

### Nhận xét & Phân tích:
1. **Hiệu năng suy giảm nghiêm trọng (-6.25 điểm):** Điểm số sụt sâu từ 18.99 xuống 12.74. Cả TTFT và TPOT đều tăng vọt (TPOT tăng từ 51ms lên 68ms).
2. **Nguyên lý ảnh hưởng:** Khi hạ `--max-model-len`, mặc dù giải phóng được một phần nhỏ VRAM cho KV Cache block, nhưng nó làm thay đổi phân bổ chú ý (attention context window) hoặc ảnh hưởng đến hiệu quả của prefix caching trong các phiên multi-turn dài. Việc này gây ra cache eviction thường xuyên hơn hoặc kích hoạt các thuật toán attention kém tối ưu hơn.
3. **Kết luận:** **CẤM HẠ `--max-model-len` dưới 262144**. Mức context mặc định lớn của Qwen giúp vLLM tận dụng tối đa RadixAttention và tối ưu hóa bộ nhớ đệm.

---
