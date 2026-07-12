# Nhật ký thử nghiệm & nộp bài (Submission Logs) - Bài 1

File này được sử dụng để theo dõi toàn bộ lịch sử các lần chạy thử nghiệm, thông số sử dụng và kết quả trả về từ portal, giúp đối chiếu và tìm ra baseline tốt nhất cho bài toán 3D Reconstruction & Novel View Synthesis.

---

## 📊 Bảng tổng hợp kết quả (Leaderboard nội bộ)

| STT | File/Thư mục nộp                                   | Mô tả cấu hình / Thay đổi                                        | **Điểm số (Score)** |  PSNR / SSIM / LPIPS  | Kết luận / Ghi chú                                              |
| :-: | :------------------------------------------------- | :--------------------------------------------------------------- | :-----------------: | :-------------------: | :-------------------------------------------------------------- |
|  1  | [08072026/1114-result.md](08072026/1114-result.md) | Cấu hình giống `kaggle_train.ipynb` hiện tại (Iteration = 7000)  |    **46.96890**     | 18.63 / 48.63 / 46.99 | Iteration 7000 chưa hội tụ đầy đủ, LPIPS cao.                   |
|  2  | [09072026/1634-result.md](09072026/1634-result.md) | Baseline 3D Gaussian Splatting mặc định (Iteration = 30000) - R1 |    **54.97630**     | 19.26 / 53.97 / 31.93 | Baseline mặc định chạy lần 1, điểm số ở mức tốt.                |
|  3  | [09072026/1658-result.md](09072026/1658-result.md) | Baseline 3D Gaussian Splatting mặc định (Iteration = 30000) - R2 |    **52.48840**     | 18.39 / 52.09 / 35.42 | Lượt chạy thứ 2 để test sai số, sụt giảm mạnh ~2.49 điểm.       |
|  4  | [09072026/1713-result.md](09072026/1713-result.md) | Baseline 3D Gaussian Splatting mặc định (Iteration = 30000) - R3 |    **53.41670**     | 18.85 / 53.08 / 34.55 | Lượt chạy thứ 3 để test sai số, nằm ở mức trung bình.           |
|  5  | [09072026/1726-result.md](09072026/1726-result.md) | Baseline 3D Gaussian Splatting mặc định (Iteration = 30000) - R4 |    **53.77280**     | 19.08 / 53.42 / 34.25 | Lượt chạy thứ 4 để test sai số, dao động quanh mức trung bình.  |
|  6  | [09072026/1737-result.md](09072026/1737-result.md) | Baseline 3D Gaussian Splatting mặc định (Iteration = 30000) - R5 |    **53.87740**     | 19.17 / 53.49 / 34.17 | Lượt chạy thứ 5 để test sai số, tương đương Run 4.              |
|  7  | [09072026/2057-result.md](09072026/2057-result.md) | Baseline 3D Gaussian Splatting mặc định (Iteration = 30000) - R6 |    **55.65110**     | 19.49 / 54.86 / 31.25 | Lượt chạy thứ 6 để test sai số, đạt điểm cao nhất của baseline. |

---

## 📝 Nhật ký chi tiết theo ngày

_(Ghi chú các quan sát quan trọng, lỗi gặp phải hoặc định hướng dài hạn không nằm gọn trong bảng trên)_

- **12/07/2026**:
  - Thiết lập thành công hệ thống rules cục bộ (`RULES.md`) và khởi tạo log lịch sử nộp bài hoàn chỉnh.
  - Ghi nhận 7 lần chạy thử nghiệm đầu tiên vào các ngày 08/07 và 09/07 để làm mốc so sánh (baseline).
  - **Phân tích sai số (Grading Variance)**: Qua 6 lần chạy của cùng một cấu hình 30k baseline mặc định, kết quả dao động từ `52.48` đến `55.65` (biên độ tối đa là `3.16` điểm, điểm trung bình đạt `54.03`). Điều này phản ánh rõ tính chất bất định của quá trình huấn luyện/sinh ảnh hoặc hệ thống grader. Khuyên dùng cố định seed chặt chẽ khi huấn luyện để giảm thiểu dao động ngẫu nhiên này.
