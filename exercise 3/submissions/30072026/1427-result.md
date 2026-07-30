# Kết quả Slot 1427 (R23 FlashInfer LowRAM Graphs)

- **Điểm số**: 0.0000 (Thất bại)
- **Thời gian chấm**: 30/07/2026
- **Cấu hình**: 
  - `image`: docker.io/taze05/lfm25-h200-ers@sha256:875149
  - `--no-enable-flashinfer-autotune`
  - `--compilation-config={"cudagraph_mode":"FULL_DECODE_ONLY", ...}`
  - `--dtype=float16` + `--attention-backend=FLASHINFER`

## Thông báo lỗi từ BTC
```
multi-turn bench timed out after 1800s with no result — the contestant endpoint stopped responding mid-run (it may still be serving /health while its completions hang or return invalid tokens)
```

## Đánh giá & Phân tích nguyên nhân
1. **Deadlock / Hang mid-run**: Cờ CLI `--compilation-config` với `cudagraph_mode: FULL_DECODE_ONLY` kết hợp tắt autotune (`--no-enable-flashinfer-autotune`) trên FlashInfer Backend khiến runtime bị deadlock hoặc treo vô thời hạn khi nhận các batch requests ở lượt thứ 2 (Turn 2+).
2. **Khẳng định**: Việc cấu hình `--compilation-config` qua CLI JSON flag của vLLM trong môi trường FlashInfer + Float16 không tương thích và gây treo server (Timeout 1800s).
3. **Giải pháp**: Phải dùng Image đã patch trực tiếp ở cấp source code Python (`ptquanh/sandbox-runtime:phase1`) thay vì truyền CLI JSON flags phức tạp.
