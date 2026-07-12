# Kết quả Submission - 16:34 09/07/2026 (STT 2 - Baseline GS 15k Iterations - Run 1)

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
- **Mục đích**: Đánh giá hiệu năng và điểm số của cấu hình baseline mặc định (15k iterations) trên hệ thống chấm bài.

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

1. **Phân tích chất lượng ảnh**:
   - So với cấu hình 7k iterations (STT 1), việc tăng số lượng iterations lên 15k giúp mô hình hội tụ tốt hơn hẳn: điểm số tăng từ `46.97` lên `54.98`.
   - Các chỉ số LPIPS giảm sâu xuống `31.93%` và PSNR tăng lên `19.26dB`, cho thấy độ chi tiết và sắc nét của ảnh tăng rõ rệt.
2. **Kết luận**:
   - Mức 15k iterations cung cấp chất lượng tương đối ổn định và là điểm bắt đầu (baseline) tốt để thử nghiệm các tối ưu hóa khác.
