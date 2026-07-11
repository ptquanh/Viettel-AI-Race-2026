# Kết quả Benchmark - 12:03 11/07/2026 (STT 83 - FP8 weights + Custom INT8 KV + Chunk 4096)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-phase2-int8` + `--quantization fp8` + `--kv-cache-dtype int8_per_token_head` + `--enable-chunked-prefill` + `--max-num-batched-tokens=4096`
- **Mục đích**: Kiểm tra song song lượng tử hóa INT8 KV Cache (per-token-head) kết hợp với Chunked Prefill 4096 để xem có giải quyết được nghẽn CPU và nghẽn băng thông bộ nhớ cùng lúc hay không.

## Chỉ số đo được

- **Điểm số**: **2.34** (Giảm mạnh từ baseline 18.99)
- **Số request vượt qua SLO**: 31/120 (passed_slo)
- **TTFT P50**: **3252 ms** (Tăng khủng khiếp từ ~620ms)
- **TTFT P95**: **7762 ms**
- **TPOT Median**: **78 ms** (Tăng từ 51ms)
- **Accuracy drop**: 0 (Không giảm độ chính xác)

## Phân tích & Kết luận

1. **TTFT tăng vọt (3.2s vs 0.6s baseline)**: Lượng tử hóa `int8_per_token_head` KV cache đòi hỏi tính toán scaling factor động cho mỗi token và mỗi head. Khi xử lý prefill (đặc biệt là chunked prefill), việc thực thi các kernel trích xuất/lượng tử hóa này trên MiG H200 (độ trễ launch kernel cao và CPU chỉ có 3 cores làm nghẽn việc lập lịch) đã tạo ra bottleneck cực lớn.
2. **TPOT tăng lên 78ms (so với 51ms baseline)**: Dù TPOT được cải thiện hơn so với việc dùng `int8_per_token_head` không có chunked prefill (STT 71 đạt tới 220ms), con số 78ms vẫn cao hơn đáng kể so với FP16 KV cache (51ms). Điều này chứng minh overhead giải lượng tử (dequantization) per-token-head trong lúc decode lớn hơn nhiều so với băng thông lưu giữ khi dùng FP16.
3. **Kết luận**: Phương án Custom INT8 KV Cache per-token-head thất bại hoàn toàn. Không nên tiếp tục đi theo hướng này trên vLLM v0.22.1 cho mô hình nhỏ Qwen3.5-2B.
