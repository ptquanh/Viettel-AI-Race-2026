# Kết quả thử nghiệm Slot 02 (07:59) - Ngày 26/07 - N-Gram + V1 Engine

## 1. Thông tin chung

- **Thời gian chấm**: 26/07/2026 07:59
- **Submission File**: `exercise 3/submissions/26072026/0759-docker-compose.yml`
- **Cấu hình**: Image v14 (FP8) + `VLLM_USE_V1=1` + `--speculative-model=ngram` + `COMPILATION_LEVEL=0`
- **Điểm số**: ❌ **THẤT BẠI (BỊ HỦY CHẤM)**

## 2. Chi tiết lỗi từ Grader

```text
protocol aborted: long-context probe failed (0%) — truncation / dual-path likely
```

## 3. Phân tích & Đánh giá (Vết rạn nứt Kiến trúc SSM)

Lỗi này **chính xác 100% giống với lỗi ở Slot 08 ngày 22/07 (`1430-result.md`)**.

1. **Kiến trúc Hybrid Recurrent (SSM)**: Mô hình LFM2.5 sử dụng kiến trúc State-Space Model (SSM) kết hợp GQA. Không giống như Transformer truyền thống (chỉ cần xóa KV-Cache khi reject token), kiến trúc SSM bắt buộc phải lưu trạng thái truy hồi (Recurrent State) qua từng token.
2. **Xung đột N-Gram**: Khi N-Gram đoán trước N token, vLLM sẽ đẩy cả N token này vào để verify. Khi mô hình LFM2.5 verify và **reject** một token sai, vLLM hiện tại (dù là V0 hay V1 Engine) **KHÔNG THỂ ROLLBACK được Recurrent State Buffer** về thời điểm trước đó.
3. **Hậu quả**: Trạng thái bộ nhớ của mô hình bị hỏng hoàn toàn. Ở các token tiếp theo, nó sinh ra chuỗi ký tự rác hoặc bị cắt cụt (truncation). Trọng tài (Grader) lập tức phát hiện Output rác (Long-context probe failed) và hủy bài thi ở mức điểm 0.

## 4. Hành động tiếp theo

- **Khẳng định**: Toàn bộ hệ sinh thái Speculative Decoding (N-gram, Draft Model, Lookahead) của vLLM hiện tại **VÔ DỤNG VÀ KHÔNG TƯƠNG THÍCH** với kiến trúc SSM của LFM2.5. Chúng ta buộc phải loại bỏ vĩnh viễn đòn bẩy này.
- **Chuyển hướng (Kế hoạch Z)**: Kích hoạt ngay **Phương án Z2: `TORCHINDUCTOR_MAX_AUTOTUNE=1`** để ép PyTorch sinh ra nhân CUDA tối ưu nhất ở tầng Assembly (kết hợp `COMPILATION_LEVEL=3`). Hoặc chuyển sang **Phương án Z1: INT4 Quantization** (Image v15) nếu Autotune thất bại.
