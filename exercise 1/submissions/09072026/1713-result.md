# Kết quả Submission - 17:13 09/07/2026 (STT 4 - Baseline GS 15k Iterations - Run 3 / Test Sai Số)

- **Cấu hình**:
  - Mô hình: 3D Gaussian Splatting (gốc từ repo graphdeco-inria)
  - Iterations (Số vòng lặp): 15,000 (mặc định)
  - Resolution (Độ phân giải): 1 (nguyên gốc)
  - Antialiasing (Rasterizer): Bật (use_antialiasing = True)
  - Optimizer: sparse_adam (Sparse Adam)
  - Siêu tham số Densification:
    - Bắt đầu từ: 500 iterations (densify_from_iter = 500)
    - Tần suất: 100 iterations (densification_interval = 100)
    - Ngưỡng gradient: 0.00010 (densify_grad_threshold = 0.0001)
    - Kết thúc densify ở: 15,000 iterations (bị giới hạn bởi tổng iterations)
    - Reset opacity mỗi: 2,500 iterations (opacity_reset_interval = 2500)
  - Loss weights: lambda_dssim = 0.15 (SSIM weight: 0.15, L1 weight: 0.85)
- **Mục đích**: Thử nghiệm lặp lại cấu hình mặc định (lần thứ 3) nhằm tiếp tục thu thập dữ liệu về sai số và độ biến động kết quả của hệ thống chấm bài.

## Chỉ số đo được

| Chỉ số           |    Giá trị    | Ý nghĩa                                                        |
| :--------------- | :-----------: | :------------------------------------------------------------- |
| `Điểm` (Score)   | **53.41670**  | Điểm số tổng hợp cuối cùng                                     |
| `PSNR`           | **18.854722** | Peak Signal-to-Noise Ratio (càng cao càng tốt)                 |
| `SSIM`           |  **53.0785**  | Structural Similarity (càng cao càng tốt)                      |
| `LPIPS`          |  **34.5491**  | Learned Perceptual Image Patch Similarity (càng thấp càng tốt) |
| `num_scenes`     |     **8**     | Tổng số scene được hệ thống đánh giá                           |
| `matched_scenes` |     **8**     | Số scene khớp với ground-truth                                 |

## Phân tích kết quả

1. **Phân tích sai số khi chấm bài (so sánh với các Run 1 và Run 2 của 15k baseline)**:
   - Điểm số của Run 3 (`53.41670`) nằm ở mức trung bình của các lần chạy thử nghiệm trước: thấp hơn Run 1 (`54.97630`) nhưng cao hơn Run 2 (`52.48840`).
   - LPIPS (`34.55%`) và PSNR (`18.85dB`) cũng dao động nằm giữa khoảng min-max thu được ở các run trước.
   - Biên độ dao động tối đa của điểm số qua 6 lần chạy thử nghiệm cấu hình mặc định hiện đang ghi nhận là: `55.65110 - 52.48840 = 3.16270` điểm.
2. **Kết luận**:
   - Khẳng định sự tồn tại của sai số khá cao trên portal chấm điểm hoặc do tính chất bất định của GPU/hàm tối ưu trong training pipeline.
   - Để có đánh giá tin cậy, các lần chạy thử nghiệm sau cần chạy nhiều hạt giống (seeds) khác nhau hoặc các thử nghiệm cải tiến lớn mới có thể vượt qua biên sai số ngẫu nhiên này.
