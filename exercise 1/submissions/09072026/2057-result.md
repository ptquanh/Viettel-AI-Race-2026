# Kết quả Submission - 20:57 09/07/2026 (STT 7 - Baseline GS 15k Iterations - Run 6 / Test Sai Số)

- **Cấu hình**:
  - Mô hình: 3D Gaussian Splatting (gốc từ repo graphdeco-inria)
  - Iterations (Số vòng lặp): 15,000 (mặc định)
  - Resolution (Độ phân giải): 1 (nguyên gốc)
  - Antialiasing (Rasterizer): Bật (use_antialiasing = True)
  - Optimizer: sparse_adam (Sparse Adam)
  - Siêu tham số Densification:
    - Bắt đầu từ: 500 iterations (densify_from_iter = 500)
    - Tần suất: 100 iterations (densification_interval = 100)
    - Ngưỡng gradient: 0.00020 (densify_grad_threshold = 0.0002)
    - Kết thúc densify ở: 12,000 iterations (densify_until_iter = 12000)
    - Reset opacity mỗi: 3,000 iterations (opacity_reset_interval = 3000)
  - Loss weights: lambda_dssim = 0.15 (SSIM weight: 0.15, L1 weight: 0.85)
- **Mục đích**: Thử nghiệm lặp lại cấu hình mặc định (lần thứ 6) nhằm thu thập thêm dữ liệu phân tích về sai số và độ biến động kết quả của hệ thống chấm bài.

## Chỉ số đo được

| Chỉ số           |    Giá trị    | Ý nghĩa                                                        |
| :--------------- | :-----------: | :------------------------------------------------------------- |
| `Điểm` (Score)   | **55.65110**  | Điểm số tổng hợp cuối cùng                                     |
| `PSNR`           | **19.491827** | Peak Signal-to-Noise Ratio (càng cao càng tốt)                 |
| `SSIM`           |  **54.8554**  | Structural Similarity (càng cao càng tốt)                      |
| `LPIPS`          |  **31.2514**  | Learned Perceptual Image Patch Similarity (càng thấp càng tốt) |
| `num_scenes`     |     **8**     | Tổng số scene được hệ thống đánh giá                           |
| `matched_scenes` |     **8**     | Số scene khớp với ground-truth                                 |

## Phân tích kết quả

1. **Phân tích sai số khi chấm bài (so sánh với các Run 1-5 của cấu hình 15k)**:
   - Run 6 (`55.65110` lúc 20:57) là lượt chạy đạt kết quả cao nhất trong tất cả các lượt chạy thử của cấu hình 15k baseline mặc định.
   - Khi so sánh với lượt chạy thấp nhất (Run 2 - `1658` đạt `52.48840`), sự chênh lệch lên đến `3.1627` điểm.
   - Thống kê chi tiết qua 6 lần chạy thử của cùng cấu hình mặc định:
     - Điểm cao nhất: `55.65110` (Run 6 / 20:57)
     - Điểm thấp nhất: `52.48840` (Run 2 / 16:58)
     - Khoảng biến động lớn nhất (Max-Min Spread): `3.1627` điểm
     - Điểm trung bình (Mean Score): `54.03045` điểm
2. **Kết luận**:
   - Ghi nhận phân phối điểm số của baseline mặc định 15k qua 6 lần chạy: `54.98 (R1), 52.49 (R2), 53.42 (R3), 53.77 (R4), 53.88 (R5), 55.65 (R6)`.
   - Có thể thấy kết quả dao động ngẫu nhiên quanh mức trung bình 54.03 điểm với biên độ sai số khoảng `±1.6` điểm. Việc đánh giá các cải tiến nhỏ cần hết sức lưu ý biên sai số này.
