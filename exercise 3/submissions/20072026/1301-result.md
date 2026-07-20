# Kết Quả Thử Nghiệm 1301 (Slot 6 - 20/07/2026)

## Thông Tin Chung

- **Mã thử nghiệm**: `1301`
- **File Compose**: `1301-docker-compose.yml`
- **Thời gian chấm**: 20/07/2026 13:01
- **Cấu hình**: Image v4.1 (Deep Warmup + Delay LB) + `VLLM_MAX_NUM_SEQS=28`

## Kết Quả Chấm Điểm

- **Điểm số (ERS)**: `51.83`
- **f_delta**: `1`
- **Penalty**: `1`
- **Final Score**: `51.83`

## Chỉ Số Chi Tiết

- **Total Request**: `420`
- **TTFT P50**: `75 ms`
- **TTFT P95**: `102 ms`
- **TPOT Median**: `4 ms`
- **Failed Count**: `7`
- **Warmup Count**: `0`
- **Accuracy Drop**: `0%`
- **Config Hash**: `sha256:603c84f67bd0fadaa6ea739f2d1aa564761ff94e00dc61da25fe7e1d13853881`

## Phân Tích & Kết Luận

1. **Trễ TTFT P50 tăng mạnh (51ms -> 75ms)**: Thu hẹp `max_num_seqs` từ 32 xuống 28 làm tăng nghẽn hàng đợi (queueing delay) của vLLM scheduler khi gặp đợt Poisson burst.
2. **Failed Count không giảm (6 -> 7)**: Giảm concurrency không giúp hạn chế timeout hay OOM ở tail latencies của đợt 4.4K tokens.
3. **Khẳng định**: `VLLM_MAX_NUM_SEQS=32` chính là mốc tối ưu nhất (Golden Base). Không hạ xuống 28.
