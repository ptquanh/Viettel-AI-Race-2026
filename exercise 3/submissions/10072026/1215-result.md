# Kết quả Benchmark - 11:50 10/07/2026 (STT 65 - Ghost Strategy v2: vLLM v0.5.2 + Online FP8)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-modern-hijack` + script hijack tiêm cấu hình vLLM v0.5.2 tối ưu: `--max-model-len 43008`, `--gpu-memory-utilization 0.93`, `--quantization fp8`, `--enable-chunked-prefill`, `--max-num-batched-tokens 2048`, `--enable-prefix-caching`, `--max-num-seqs 64`, `--disable-log-requests`, `--disable-log-stats`.
- **Mục đích**: Lần chạy đầu tiên sử dụng Chiến thuật Bóng ma v2 trên nhân vLLM v0.5.2 đời mới nhằm khai thác vòng lặp giải mã bằng C++ và Chunked Prefill tối ưu sâu để bứt phá khỏi giới hạn TPOT 51ms (ceilling 45ms), kích hoạt điểm TPOT.

- **Điểm số**: `Chấm điểm thất bại (Fail)`
- **Lỗi startup**:
  ```
  ValueError: The checkpoint you are trying to load has model type `qwen3_5` but Transformers does not recognize this architecture. This could be because of an issue with the checkpoint, or because your version of Transformers is out of date.
  ```

## Phân tích kết quả

Thử nghiệm thất bại do lỗi không nhận diện cấu trúc mô hình (`KeyError: 'qwen3_5'`).

1. **Nguyên nhân:** Phiên bản vLLM v0.5.2 (phát hành giữa năm 2024) đi kèm thư viện `transformers` phiên bản cũ (v4.43.0), hoàn toàn không có định nghĩa cấu trúc cho mô hình Qwen3.5 (vốn được thêm vào các bản `transformers` muộn hơn vào năm 2025/2026).
2. **Đánh giá:** Bản vLLM v0.22.1 do BTC cung cấp là một phiên bản rất mới (chứ không phải bản cũ như nhầm lẫn ban đầu), chạy trên Python 3.12 và có tích hợp đầy đủ cấu trúc Qwen3.5. Chúng ta buộc phải sử dụng vLLM v0.22.1 làm nền tảng phát triển duy nhất.

**Kết luận:** Hủy bỏ toàn bộ hướng đi tối ưu bằng vLLM v0.5.2 hoặc các phiên bản cũ hơn. Quay lại tối ưu sâu trên nền tảng vLLM v0.22.1.
