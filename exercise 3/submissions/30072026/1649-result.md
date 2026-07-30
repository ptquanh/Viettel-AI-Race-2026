# Kết quả Benchmark - 16:49 30/07/2026 (STT 205 - Sai lầm đổi Base & Config)

- **Sự cố Build Docker**: Lệnh `docker build` Phase 3 (kế thừa kỷ lục `sha256:2f1c`) bị **LỖI (Exit Code 1)** do không tìm thấy class Scheduler trong file patch.
- **Hệ quả**: Lệnh `docker push` sau đó thực chất chỉ push lại cái **Image cũ (`sha256:dc9e`)** của đợt 16:30.
- **Nguyên nhân thảm họa**: Trong file compose `1649`, ta lại dùng image `dc9e` (vLLM v0.26.0) nhưng tôi lại đi đổi flag thành `--quantization=fp8` và `--kv-cache-dtype=bfloat16` (bắt chước theo Slot 0851 cũ).
- Kết quả: Config lệch pha hoàn toàn với engine v0.26.0 khiến hiệu năng tụt thê thảm.

## Chỉ số đo được

| Chỉ số          |   Giá trị   | Ý nghĩa                                             |
| :-------------- | :---------: | :-------------------------------------------------- |
| `final_score`   | **61.8400** | Điểm số cuối cùng (TỤT NẶNG)                        |
| `ers`           |  **61.84**  | Điểm số hiệu năng (Effective Request Score)         |
| `failed_count`  |    **6**    | Số lượng request thất bại                           |
| `tbt_median_ms` |  **4 ms**   | TPOT (Bị tăng lại lên 4ms do lệch config)           |
| `ttft_p50_ms`   |  **52 ms**  | TTFT P50 (Tăng từ 44ms lên 52ms)                    |
| `ttft_p95_ms`   |  **72 ms**  | TTFT P95                                            |

## Đánh giá & Rút kinh nghiệm
Chúng ta **không cần phải mạo hiểm lùi về Image `sha256:2f1c` nữa!**
Image Phase 3 hiện tại (`sha256:dc9e`) vốn đã đạt **68.20 ERS** (Slot 1630) với TPOT 3ms và TTFT P50 cực nhanh 44ms.
Điểm trừ duy nhất ở 1630 là có 9 request bị lỗi do `DECODE_PREFILL_CAP=128` hơi hẹp.
👉 Hướng đi đúng: **Quay về chuẩn xác config của Slot 1630 (68.20 ERS), và CHỈ tăng `DECODE_PREFILL_CAP=256` để loại bỏ 9 lỗi.**
