# Kết quả Benchmark - 12:35 11/07/2026 (STT 84 - FP8 weights + Custom FP8 KV + Chunk 4096)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-fp8` + `--quantization fp8` + `--kv-cache-dtype fp8` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096`
- **Mục đích**: Kiểm tra song song lượng tử hóa FP8 KV Cache kết hợp với Chunked Prefill 4096 để giảm tải băng thông bộ nhớ và CPU scheduling overhead đồng thời.

## Chỉ số đo được

- **Điểm số**: **20.82** (Vượt qua baseline tốt nhất 18.99!)
- **Số request vượt qua SLO**: 45/120 (passed_slo)
- **TTFT P50**: **2036 ms** (Vẫn rất cao so với baseline ~620ms, nhưng tốt hơn nhiều so với 3252ms của INT8 KV)
- **TTFT P95**: **3023 ms**
- **TPOT Median**: **31 ms** (Cực kỳ ấn tượng! Giảm tới 40% so với baseline 51ms)
- **Accuracy drop**: 0 (Không bị suy giảm độ chính xác)

## Phân tích & Hướng đi tiếp theo

1. **Bứt phá TPOT (31ms vs 51ms baseline)**: Việc lượng tử hóa FP8 KV Cache (`fp8_per_token_head`) đã giải phóng đáng kể băng thông bộ nhớ (HBM Bandwidth) trong pha decode trên GPU MiG H200. Đây là minh chứng rõ ràng cho thấy FP8 KV Cache là chìa khóa để đạt điểm số cao (giảm TPOT từ 51ms xuống 31ms).
2. **Nghẽn cổ chai TTFT (2036ms)**: Dù TPOT rất nhanh, điểm số tổng thể bị kìm hãm ở mức 20.82 do TTFT quá lớn (2.0s). Do TTFT chậm, chỉ có 45/120 request đạt chuẩn SLO (thời gian phản hồi đầu tiên).
   * **Nguyên nhân**: Lượng tử hóa KV Cache per-token-head đòi hỏi tính toán động lúc prefill. Việc này kết hợp với `--enable-chunked-prefill` (chia nhỏ prefill thành nhiều chunk) vô tình bắt CPU phải khởi chạy kernel lượng tử hóa nhiều lần hơn, làm tăng JIT/Triton scheduling overhead trên CPU 3 cores.
3. **Ý tưởng tối ưu tiếp theo**:
   * **Tắt Chunked Prefill khi dùng FP8 KV Cache**: Thử nghiệm chạy FP8 KV Cache mà không bật `--enable-chunked-prefill`. Nếu không chia chunk, prefill chỉ thực hiện trong 1 bước duy nhất, giảm số lần CPU gọi kernel lượng tử hóa xuống mức tối thiểu, từ đó hy vọng đưa TTFT về lại mức ~600ms mà vẫn giữ được TPOT 31ms.
   * **Tăng OMP_NUM_THREADS**: Kiểm tra xem tăng số luồng CPU lên 4 hoặc 6 có giúp giảm trễ lập lịch kernel lượng tử hóa hay không.
   * **Chạy thử Chunk size lớn hơn**: Tăng chunk size từ 4096 lên 8192 hoặc 16384 để giảm số lượng chunk và số lần gọi kernel.
