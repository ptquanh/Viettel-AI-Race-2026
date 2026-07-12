# Kết quả Submission - 16:34 09/07/2026 (STT 3 - Baseline GS 30k Iterations - Run 2)

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
- **Mục đích**: Đánh giá độ ổn định và tính lặp lại của baseline 30k iterations trên hệ thống chấm bài.

## Chỉ số đo được

| Chỉ số           |    Giá trị    | Ý nghĩa                                                        |
| :--------------- | :-----------: | :------------------------------------------------------------- |
| `Điểm` (Score)   | **54.97630**  | Điểm số tổng hợp cuối cùng                                     |
| `PSNR`           | **19.260133** | Peak Signal-to-Noise Ratio (càng cao càng tốt)                 |
| `SSIM`           |  **53.9697**  | Structural Similarity (càng cao càng tốt)                      |
| `LPIPS`          |  **31.9267**  | Learned Perceptual Image Patch Similarity (càng thấp càng tốt) |
| `num_scenes`     |     **8**     | Tổng số scene được hệ thống đánh giá                           |
| `matched_scenes` |     **8**     | Số scene khớp với ground-truth                                 |

## Phân tích kết quả

1. **Phân tích so sánh với Run 1 (14:15)**:
   - Điểm số của Run 2 (`54.97630`) thấp hơn một chút so với Run 1 (`55.65110`).
   - LPIPS tăng nhẹ từ `31.25%` lên `31.92%` (tệ hơn), PSNR giảm từ `19.49dB` xuống `19.26dB`, và SSIM giảm từ `54.85%` xuống `53.97%`.
   - Sự dao động này có thể do tính chất ngẫu nhiên trong quá trình khởi tạo điểm hoặc tối ưu hóa (optimizer stochasticity), hoặc do biến động nhẹ trong quá trình sinh ảnh rasterization.
2. **Kết luận**:
   - Baseline 30k iterations có độ dao động điểm số nhẹ khoảng ~0.67 điểm giữa các lần chạy. Điều này cần được lưu ý khi đánh giá các cải tiến nhỏ để tránh nhầm lẫn giữa cải tiến thực sự với sai số ngẫu nhiên.
