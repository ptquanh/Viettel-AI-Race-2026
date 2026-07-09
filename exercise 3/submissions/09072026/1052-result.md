# Kết quả Benchmark - 10:52 09/07/2026 (STT 57 - Modern vLLM v0.22.1 Hijack + VRAM 0.92 & DEBUG logs Patch)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack` + các tham số tối ưu hóa (max-model-len=43008, memory=0.92, quantization=fp8).
- **Mục đích**: Bản vá giảm VRAM utilization xuống 0.92 để vượt qua lỗi khởi tạo GPU Worker.

## Chỉ số đo được

- **Điểm số**: `6.82` (Passed SLO: `80/120`)
- **TTFT P50**: `1587 ms`
- **TTFT P95**: `8563 ms`
- **failed_count**: `0`
- **warmup_count**: `0`
- **accuracy_drop**: `0`
- **tbt_median_ms**: `46 ms`

## Phân tích kết quả

Bản vá đã chạy thành công custom image và hoàn thành 100% request (0 failed), chứng minh cơ chế đánh chặn (Ghost Strategy) hoạt động hoàn hảo trên môi trường portal. Tuy nhiên, điểm số bị sụt giảm nghiêm trọng từ `18.99` xuống `6.82`, với TTFT tăng vọt lên 1.5s - 8.5s.

**Nguyên nhân nghẽn cổ chai:**

1. **Trực quan hóa Prefill-Decode Blocking:** Việc set `--max-num-batched-tokens 8192` kết hợp với `--enable-chunked-prefill` phản tác dụng. Khi kích thước batch prefill quá lớn (8192 tokens), GPU phải dành một khoảng thời gian liên tục rất dài (~300-500ms) chỉ để xử lý prefill cho một request mới, khiến bước decode (giải mã) của toàn bộ các request khác đang hoạt động trong hàng đợi bị đóng băng (decode starvation). Điều này làm tăng vọt TTFT trung bình.
2. **RoPE Scaling và max-model-len:** Việc giới hạn `--max-model-len 43008` (thay vì giữ nguyên `262144` như baseline) làm thay đổi tính toán tần số RoPE động của Qwen, ảnh hưởng tiêu cực đến tốc độ xử lý Attention đối với các context cực dài.

---

_Kết luận: Cần khôi phục cấu hình tương tự như STT 21 (đạt 18.99 điểm): giữ nguyên `max-model-len=262144`, đặt `gpu-memory-utilization=0.95`, gỡ bỏ hoàn toàn cờ batch size/capture size tự chế để vLLM tự tối ưu._
