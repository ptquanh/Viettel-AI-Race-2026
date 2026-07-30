# Kết quả Benchmark - 18:15 30/07/2026 (STT 208 - slot1-ngram-spec)

- **Cấu hình**: Image `sha256:2f1c` (Champion 0851 Base) + `--spec-method=ngram_gpu` + `--spec-tokens=3`.
- **Mục đích**: Kích hoạt N-gram Speculative Decoding trên GPU để giảm TPOT xuống ~2ms.

## Chỉ số đo được

**Chấm điểm thất bại (0.00 ERS)**

### Chi tiết lỗi

- **Thông báo**: `protocol aborted: long-context probe failed (0%) — truncation / dual-path likely`
- **Phân tích**:
  - N-gram speculative decoding tạo ra token draft gây lỗi khi verification với Mamba/Attention backend.
  - vLLM báo lỗi `truncation / dual-path likely`, đây là lỗi correctness do draft tokens và target tokens không đồng bộ trong mô hình Hybrid (Mamba+Attention).
  - Kết luận: Kiến trúc `LFM2.5` (Hybrid) không hỗ trợ speculative decoding dạng ngram_gpu do xung đột cơ chế tính toán nội bộ.

## Kết luận

- Lược bỏ hoàn toàn hướng đi Speculative Decoding.
- Chuyển hướng tập trung sang CUDA graph (Slot 3) và Phase 3 Scheduler Patch (Slot 5).
