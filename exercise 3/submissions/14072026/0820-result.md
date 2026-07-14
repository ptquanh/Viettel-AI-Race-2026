# Kết quả Benchmark - 14/07/2026 (STT 92 - Ghost v9.2: Warmup Ablation - Seqs 32 - 0820)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2` + `OMP_NUM_THREADS=3` + `max-num-seqs=32` + `quantization=fp8` + `kv-cache-dtype=fp8` + Warmup Disabled (`VLLM_WARMUP=0`) + Tắt Chunked Prefill.
- **Mục đích**: Nghiên cứu đối chứng (ablation study) khi tắt warmup. Thử nghiệm này giúp đánh giá chính xác tác động của Warmup JIT đến TTFT, đồng thời đóng vai trò là phương án dự phòng an toàn nếu cơ chế Warmup gặp trục trặc kỹ thuật hoặc gây lỗi runtime trên Portal.

## Chỉ số đo được

- **Điểm số**: **2.24**
- **Số request vượt qua SLO**: 3/120 (passed_slo)
- **TTFT P50**: **3773 ms**
- **TTFT P95**: **11112 ms**
- **TPOT Median**: **56 ms**
- **Accuracy drop**: 0 (GPQA)

## Phân tích kết quả

1. **Hiệu ứng khi tắt Warmup & Chunked Prefill**:
   - TPOT tăng lên **56ms** (giống như không dùng FP8 KV Cache) vì không có prefill chunking giúp co-scheduling các decode step với prefill chunk. Đồng thời, việc thiếu warmup khiến các requests đầu tiên chịu trễ cực lớn.
   - TTFT P50 vọt lên tới **3.7s** do hàng đợi prefill (20k tokens hệ thống) bị ùn tắc nghiêm trọng khi 20 requests đầu tiên ập vào cùng lúc. Do không bật chunked prefill, vLLM thực hiện prefill tuần tự toàn bộ mà không thể phân mảnh chia sẻ tài nguyên, dẫn đến nghẽn cổ chai hàng đợi khủng khiếp.
2. **Hướng đi kế tiếp**:
   - Nộp thử **Slot 2** (Seqs=32, bật Warmup v2 với System Prompt đầy đủ và tắt Chunked Prefill) để xem Prefix Cache hit có giải quyết hoàn toàn TTFT hay không.
