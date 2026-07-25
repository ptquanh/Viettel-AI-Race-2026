# Kết Quả Thử Nghiệm Slot 07 (11:43 AM - 25/07/2026)

- **Điểm số**: **58.2000** (-4.47đ so với Kỷ kỷ lục Slot 04 62.67đ)
- **Chỉ số chi tiết**:
  - ERS: 58.2
  - Final Score: 58.2
  - Total Count: 420
  - TTFT P50: 59 ms (+14ms)
  - TTFT P95: 81 ms (+20ms)
  - TPOT (TBT Median): 4 ms
  - Failed Count: 5
  - Warmup Count: 0
  - Accuracy Drop: 0%
  - Penalty: 1
  - Tokens/sec: 0.0599

- **Cấu hình**: Image v14 FP8 (`LOG=ERROR` + `FLASHINFER_WORKSPACE_SIZE=32MB` + `GPU_MEM=0.94` + `spawn`, Slot 07)
- **Phân tích nguyên nhân**:
  - Cấu hình tĩnh `FLASHINFER_WORKSPACE_SIZE=33554432` phát sinh overhead cấp phát/quản lý bộ nhớ hoặc can thiệp tiêu cực tới cơ chế dynamic workspace tự động của FlashInfer kernel, làm TTFT P50 vọt +14ms và P95 vọt +20ms.
- **Kết luận**: **LOẠI BỎ HOÀN TOÀN `FLASHINFER_WORKSPACE_SIZE` TĨNH!** Giữ nguyên Champion Config nguyên bản (`1012-docker-compose.yml`).
