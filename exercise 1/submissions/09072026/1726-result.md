# Kết quả Submission - 17:26 09/07/2026 (STT 6 - Baseline GS 30k Iterations - Run 5 / Test Sai Số)

- **Cấu hình**:
  - Mô hình: 3D Gaussian Splatting (gốc từ repo graphdeco-inria)
  - Iterations (Số vòng lặp): 30,000 (mặc định)
  - Resolution (Độ phân giải): 1 (nguyên gốc)
  - Antialiasing (Rasterizer): Bật (use_antialiasing = True)
  - Optimizer: sparse_adam (Sparse Adam)
  - Siêu tham số Densification:
    - Bắt đầu từ: 500 iterations (densify_from_iter = 500)
    - Tần suất: 100 iterations (densification_interval = 100)
    - Ngưỡng gradient: 0.00010 (densify_grad_threshold = 0.0001)
    - Kết thúc densify ở: 22,000 iterations (densify_until_iter = 22000)
    - Reset opacity mỗi: 2,500 iterations (opacity_reset_interval = 2500)
  - Loss weights: lambda_dssim = 0.15 (SSIM weight: 0.15, L1 weight: 0.85)
- **Mục đích**: Thử nghiệm lặp lại cấu hình mặc định (lần thứ 5) nhằm củng cố dữ liệu phân tích về sai số và độ biến động kết quả của hệ thống chấm bài.

## Chỉ số đo được

| Chỉ số           |    Giá trị    | Ý nghĩa                                                        |
| :--------------- | :-----------: | :------------------------------------------------------------- |
| `Điểm` (Score)   | **53.77280**  | Điểm số tổng hợp cuối cùng                                     |
| `PSNR`           | **19.075612** | Peak Signal-to-Noise Ratio (càng cao càng tốt)                 |
| `SSIM`           |  **53.4198**  | Structural Similarity (càng cao càng tốt)                      |
| `LPIPS`          |  **34.2464**  | Learned Perceptual Image Patch Similarity (càng thấp càng tốt) |
| `num_scenes`     |     **8**     | Tổng số scene được hệ thống đánh giá                           |
| `matched_scenes` |     **8**     | Số scene khớp với ground-truth                                 |

## Phân tích kết quả

1. **Phân tích sai số khi chấm bài (so sánh với các Run 1-4)**:
   - Điểm số của Run 5 (`53.77280`) tiếp tục khẳng định mức độ dao động quanh khoảng `52.4 - 55.6` điểm.
   - Chỉ số PSNR đạt `19.08dB` và SSIM đạt `53.42%`, cho thấy sự cải thiện nhẹ so với Run 4 nhưng vẫn chưa đạt mức tối đa như Run 1 (`55.65`).
   - Tổng quan sau 5 lượt chạy của cùng một cấu hình mặc định:
     - Điểm cao nhất: `55.65110` (Run 1)
     - Điểm thấp nhất: `52.48840` (Run 3)
     - Biên độ lệch tối đa: `3.1627` điểm
     - Điểm số trung bình (Mean Score): `(55.6511 + 54.9763 + 52.4884 + 53.4167 + 53.7728) / 5 = 54.06106`
2. **Kết luận**:
   - Khoảng dao động điểm số của baseline là khoảng `±1.5` điểm quanh điểm trung bình `54.06`.
   - Bất kỳ cải tiến kỹ thuật nào đạt mức tăng điểm dưới `2.0` điểm trên portal đều cần được kiểm chứng lại kỹ càng (ví dụ chạy trung bình 3-5 seed) để loại trừ sai số ngẫu nhiên.
