# Kết quả Submission - 11:14 08/07/2026 (STT 1 - Baseline GS 7k Iterations)

- **Cấu hình**:
  - Mô hình: 3D Gaussian Splatting (gốc từ repo graphdeco-inria)
  - Iterations (Số vòng lặp): 7,000 (giảm từ 30,000)
  - Resolution (Độ phân giải): 1 (nguyên gốc)
  - Antialiasing (Rasterizer): Bật (use_antialiasing = True)
  - Optimizer: sparse_adam (Sparse Adam)
  - Siêu tham số Densification:
    - Bắt đầu từ: 500 iterations (densify_from_iter = 500)
    - Tần suất: 100 iterations (densification_interval = 100)
    - Ngưỡng gradient: 0.00010 (densify_grad_threshold = 0.0001)
    - Kết thúc densify ở: 7,000 iterations (bị giới hạn bởi tổng iterations)
    - Reset opacity mỗi: 2,500 iterations (opacity_reset_interval = 2500)
  - Loss weights: lambda_dssim = 0.15 (SSIM weight: 0.15, L1 weight: 0.85)
- **Mục đích**: Chạy thử nghiệm baseline với số lượng iteration tối thiểu (7k) để kiểm tra tốc độ hội tụ và điểm số ban đầu.

## Chỉ số đo được

| Chỉ số           |    Giá trị    | Ý nghĩa                                                        |
| :--------------- | :-----------: | :------------------------------------------------------------- |
| `Điểm` (Score)   | **46.96890**  | Điểm số tổng hợp cuối cùng                                     |
| `PSNR`           | **18.629489** | Peak Signal-to-Noise Ratio (càng cao càng tốt)                 |
| `SSIM`           |  **48.6272**  | Structural Similarity (càng cao càng tốt)                      |
| `LPIPS`          |  **46.9924**  | Learned Perceptual Image Patch Similarity (càng thấp càng tốt) |
| `num_scenes`     |     **8**     | Tổng số scene được hệ thống đánh giá                           |
| `matched_scenes` |     **8**     | Số scene khớp với ground-truth                                 |

## Phân tích kết quả

1. **Phân tích chất lượng ảnh**:
   - Với chỉ 7000 iterations, mô hình chưa hội tụ đầy đủ.
   - Chỉ số LPIPS rất cao (46.99%), cho thấy độ sắc nét và chi tiết cảm quan của ảnh sinh ra còn mờ nhạt.
   - PSNR dưới 19dB và SSIM dưới 50% chứng tỏ cấu trúc 3D chưa được định hình rõ ràng và mịn màng.
2. **Kết luận**:
   - 7000 iterations chỉ thích hợp để debug hoặc kiểm tra nhanh pipeline đầu cuối (end-to-end), không thích hợp để nộp lấy điểm cao do chất lượng hình ảnh quá kém.
