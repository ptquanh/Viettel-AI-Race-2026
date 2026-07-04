# Viettel AI Race 2026 - Nhật ký thử nghiệm (Logs)

Bảng ghi nhận điểm số của các đợt chạy thử nghiệm cấu hình tối ưu hóa LLM Inference (Bài 3).

## Kết quả các cấu hình

| STT | Cấu hình (File)                        | Mô tả cấu hình                                     | Điểm số đạt được | Ghi chú                                                                                   | Kết luận                  |
| :-- | :------------------------------------- | :------------------------------------------------- | :--------------- | :---------------------------------------------------------------------------------------- | :------------------------ |
| 1   | `docker-compose-baseline`              | Cấu hình baseline ban đầu sử dụng image gốc từ BTC | **15.26**        | Baseline gốc                                                                              | Làm mốc so sánh (Baseline) |
| 2   | `docker-compose-baseline-custom-image` | Cấu hình baseline chạy trên custom image tự build  | **15.03**        | Khởi đầu với custom image (nhưng custom này tương tự image baseline, mục đích thử nghiệm) | Có thể dùng custom image  |

---
