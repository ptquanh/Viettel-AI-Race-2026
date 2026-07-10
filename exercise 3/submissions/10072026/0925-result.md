# Kết quả Benchmark - 09:25 10/07/2026 (STT 62 - MTP Speculative Decoding Retry)

- **Cấu hình**: Image gốc `vllm/vllm-openai:v0.22.1` + STT 21 config + `--speculative-config={"method":"mtp","num_speculative_tokens":1}`.
- **Mục đích**: Kiểm thử MTP speculative decoding (STT 50 bị Timeout 2700s). Qwen3.5 có native MTP head (`mtp_num_hidden_layers: 1`).

## Chỉ số đo được

- **Điểm số**: `10.53` (Passed SLO: `56/120`)
- **TTFT P50**: `2810 ms`
- **TTFT P95**: `17391 ms`
- **failed_count**: `0`
- **warmup_count**: `0`
- **accuracy_drop**: `1`
- **tbt_median_ms**: `47 ms`

## Phân tích kết quả

MTP Speculative Decoding mặc dù làm **giảm nhẹ TPOT** (tbt_median giảm từ `51ms` xuống `47ms`, khoảng ~8%), nhưng lại **gây suy giảm TTFT nghiêm trọng** khiến điểm số sụt giảm sâu xuống **10.53 điểm** và chỉ pass 56/120 SLO.

### Đánh giá nguyên nhân sụt giảm:
1.  **CPU Overhead cực cao khi chạy Speculative Decoding:** spec-dec đòi hỏi thêm quá trình chạy draft model (MTP head) và verify song song. Trên môi trường 3 CPU Cores của portal, việc điều phối này gây nghẽn CPU nặng, làm chậm quá trình xử lý prefill dẫn đến TTFT P50 tăng vọt lên `2.8s` (tăng gấp 4.5x lần).
2.  **Khả năng chấp nhận token (Acceptance Rate) thấp:** TPOT chỉ giảm từ 51ms về 47ms cho thấy tỷ lệ chấp nhận token từ MTP head trên workload này không cao, không đủ bù đắp lại thiệt hại khổng lồ về mặt TTFT.

**Kết luận:** Speculative decoding không phù hợp cho cấu hình phần cứng bị giới hạn CPU nghiêm trọng (3 cores) như của portal. Loại bỏ hoàn toàn speculative decoding khỏi chiến lược.
