# Kết quả Benchmark - Sáng 29/07/2026 (Slot 02 - Combo V23.1)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v23.1`
- **Mục đích**: Triển khai Phase 1 (Dynamic Prefix Tokenizer Caching 1ms) + Tích hợp Combo tối ưu cực hạn (Chunked Prefill + Async Scheduling + Interactivity Mode + 256 Seqs) từ Teammate. 

## Kết quả thử nghiệm Slot 1002 (02)

**Trạng thái**: Chấm điểm thất bại

`protocol aborted: text quality too low (0%) — likely garbage decode / dual-path`

