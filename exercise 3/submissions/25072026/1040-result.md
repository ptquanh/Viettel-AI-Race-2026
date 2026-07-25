# Kết Quả Thử Nghiệm Slot 05 (10:40 AM - 25/07/2026)

- **Điểm số**: **56.8900** (Giảm -5.78đ so với Slot 04 62.67đ)
- **Chỉ số chi tiết**:
  - ERS: 56.89
  - Final Score: 56.89
  - Total Count: 420
  - TTFT P50: 61 ms (+16ms)
  - TTFT P95: 94 ms (+33ms)
  - TPOT (TBT Median): 4 ms
  - Failed Count: 4
  - Warmup Count: 0
  - Accuracy Drop: 0%
  - Penalty: 1
  - Tokens/sec: 0.0602

- **Cấu hình**: Image v14 FP8 (`UVLOOP=1` + `ERROR` + `FLASHINFER_WORKSPACE=32MB` + `GPU_MEM=0.95`, Slot 05)
- **Phân tích nguyên nhân**:
  1. `GPU_MEM=0.95` và `FLASHINFER_WORKSPACE_SIZE` gây tranh chấp VRAM static allocation làm CUDA Graph capture stride bị chậm (+33ms P95).
  2. `uvloop` gây context-switch overhead trên Python asyncio server của vLLM v0.6+ khi gặp burst requests.
- **Kết luận**: **HỦY BỎ UVLOOP, FLASHINFER_WORKSPACE_SIZE và GPU_MEM=0.95**. Quay lại 100% nền tảng Kỷ Lục `GPU_MEM=0.94` + `spawn`!
