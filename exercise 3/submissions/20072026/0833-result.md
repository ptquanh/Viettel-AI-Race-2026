# BÁO CÁO THỬ NGHIỆM SLOT 9 - NGÀY 20/07 (0833 - FAILED)

## 1. Thông tin cấu hình
- **File nộp**: `0833-docker-compose.yml` (Slot 9 ngày 20/07)
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v3`
- **Cấu hình chính**: `SpeculativeModel=/draft_model` (Nhúng 350M offline), `SpecTokens=3`, `Compilation Level 0`, `Seqs=32`, `MaxModelLen=32768`
- **Thời gian nộp**: 08:33 (20/07/2026)

## 2. Kết quả chấm từ BTC Portal
- **Trạng thái**: **Chấm điểm thất bại (FAILED)**
- **Lỗi từ Pod**: `RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}`

## 3. Phân tích nguyên nhân Kỹ thuật Sâu sắc
1. **Bản chất Kiến trúc Hybrid Recurrent / SSM của LFM2.5**:
   - Mô hình LiquidAI LFM2.5 không sử dụng Attention chuẩn của Transformer mà dựa trên kiến trúc Recurrent/SSM (nén context thành recurrent state).
2. **Hạn chế của vLLM v0.22.1 đối với Speculative Decoding**:
   - Trong vLLM v0.22.1, cơ chế Speculative Decoding với Draft Model (`--spec-method draft_model`) chỉ hỗ trợ xác thực token proposal trên các lớp Transformer Attention chuẩn (Llama, Qwen, DeepSeek...).
   - Cơ chế này **chưa hỗ trợ vung ghép state giữa 2 mô hình Recurrent/SSM** (1.2B target và 350M draft).
   - Do đó, khi khởi chạy tiến trình `EngineCoreClient`, vLLM worker từ chối khởi tạo runner cho LFM recurrent draft layers và văng `RuntimeError: Engine core initialization failed`.

## 4. KẾT LUẬN QUAN TRỌNG:
- **Speculative Decoding (cả N-gram lẫn Draft Model)** hoàn toàn không tương thích với kiến trúc LFM2.5 trên vLLM v0.22.1.
- Không tiếp tục lãng phí slot vào các cấu hình Speculative Decoding.
