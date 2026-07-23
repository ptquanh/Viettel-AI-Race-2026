# Kết quả Benchmark - 15:28 23/07/2026 (STT 06 - Ép VLLM_USE_V1=0 + Draft LFM)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v12.1` + `VLLM_USE_V1=0` + `VLLM_SPECULATIVE_MODEL=/draft_model`
- **Mục đích**: Tắt Engine V1 để fix lỗi `Engine core initialization failed` khi dùng Draft LFM Speculative Decoding.

## Chỉ số đo được

| Chỉ số        | Giá trị  | Ý nghĩa                                     |
| :------------ | :------: | :------------------------------------------ |
| `final_score` | **FAIL** | Điểm số cuối cùng                           |
| `ers`         | **FAIL** | Điểm số hiệu năng (Effective Request Score) |

## Phân tích kết quả

1. **Lỗi khởi động (Init Failed)**:
   - Container tiếp tục văng lỗi `RuntimeError: Engine core initialization failed` tại `vllm/v1/engine/async_llm.py`.
   - Mặc dù đã truyền `VLLM_USE_V1=0`, hệ thống vẫn dùng V1 Engine hoặc lỗi thực chất xảy ra độc lập với V1 Engine.
2. **Nguyên nhân cốt lõi (Root Cause)**:
   - Truy xuất đường dẫn `/draft_model` nhưng **thực tế trong Image v12.1 không hề tồn tại thư mục này** (do chưa được COPY vào trong lúc build Docker).
   - BTC cô lập hoàn toàn mạng, nên vLLM crash lập tức khi không tìm thấy tệp tin `config.json` cục bộ tại `/draft_model` mà lại không thể tải từ HuggingFace Hub.
3. **Kết luận**:
   - Tạm dừng nhánh Speculative Decoding bằng Draft Model cho đến khi bake cứng được model `LiquidAI/LFM2.5-350M-Instruct` vào trong Image.
   - Chuyển hướng sang nhánh tối ưu Kernel Fusion (Slot 07).
