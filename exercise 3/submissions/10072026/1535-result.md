# Kết quả Benchmark - 15:35 10/07/2026 (STT 67 - Ghost Strategy v3: Slot 7 Aggressive TPOT Tweak)

- **Cấu hình**: Image `ptquanh/sandbox-runtime:vllm-v0.22.1-hijack-v3` + biến môi trường: `VLLM_MAX_NUM_SEQS=32`, `VLLM_MAX_NUM_BATCHED_TOKENS=1024`, `VLLM_ENABLE_CHUNKED_PREFILL=1`.
- **Mục đích**: Ép TPOT xuống mức tối thiểu (~20ms) bằng cách giảm tối đa số sequence xử lý đồng thời (`--max-num-seqs 32`) nhằm giảm lượng KV Cache cần load mỗi step. Chunked prefill giảm về 1024 để đảm bảo prefill không làm nghẽn decode. Thử nghiệm này có tính chất aggressive, chấp nhận hi sinh TTFT để đo đạc giới hạn điểm của $s_{tpot}$.

## Chỉ số đo được

- **Score (Điểm số)**: **2.77** (Passed SLO: 4/120)
- **erc**: 0.033333
- **ers**: 2.77
- **penalty**: 1
- **ttft_p50_ms**: 3701 ms
- **ttft_p95_ms**: 13122 ms
- **tbt_median_ms (TPOT)**: 52 ms
- **failed_count**: 0

### Nhận xét & Phân tích

- Thử nghiệm này thất bại thảm hại (chỉ có 4/120 request vượt qua SLO).
- Lý do: Ép `--max-num-seqs` xuống 32 làm cho các request bị kẹt trong hàng đợi quá lâu. TTFT P50 vọt lên **3701ms** và P95 vọt lên **13122ms** (13.1 giây), vượt xa ngưỡng SLO timeout của hệ thống chấm, dẫn đến việc bị trừ điểm nặng nề.
- Đáng chú ý là TPOT vẫn ở mức **52ms** (gần như bằng baseline 51ms), chứng tỏ việc giảm max-num-seqs xuống 32 kết hợp với chunked prefill không đem lại lợi thế về mặt TPOT để bù đắp cho sự sụt giảm nghiêm trọng của TTFT.
- Kết luận: Không thể sử dụng phương án ép batch size quá thấp (như 32) nếu dùng chung với chunked prefill trên v0.22.1.
