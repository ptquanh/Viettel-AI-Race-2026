# Kết quả Submission - 17:37 09/07/2026 (STT 7 - Baseline GS 30k Iterations - Run 6 / Test Sai Số)

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
- **Mục đích**: Thử nghiệm lặp lại cấu hình mặc định (lần thứ 6) nhằm thu thập thêm dữ liệu phân tích về sai số và độ biến động kết quả của hệ thống chấm bài.

## Chỉ số đo được

| Chỉ số           |    Giá trị    | Ý nghĩa                                                        |
| :--------------- | :-----------: | :------------------------------------------------------------- |
| `Điểm` (Score)   | **53.87740**  | Điểm số tổng hợp cuối cùng                                     |
| `PSNR`           | **19.165713** | Peak Signal-to-Noise Ratio (càng cao càng tốt)                 |
| `SSIM`           |  **53.4888**  | Structural Similarity (càng cao càng tốt)                      |
| `LPIPS`          |  **34.1716**  | Learned Perceptual Image Patch Similarity (càng thấp càng tốt) |
| `num_scenes`     |     **8**     | Tổng số scene được hệ thống đánh giá                           |
| `matched_scenes` |     **8**     | Số scene khớp với ground-truth                                 |

## Phân tích kết quả

1. **Phân tích sai số khi chấm bài (so sánh với các Run 1-5)**:
   - Điểm số của Run 6 (`53.87740`) nằm rất gần với Run 5 (`53.77280`).
   - LPIPS (`34.17%`) và PSNR (`19.17dB`) cũng tương đương với Run 5, tiếp tục củng cố mức điểm trung bình ổn định của baseline mặc định quanh khoảng 53-54 điểm.
2. **Kết luận**:
   - Dữ liệu tích lũy giúp tăng độ tin cậy của phép đo baseline mặc định. Điểm số dao động mạnh từ 52.48 đến 55.65, nhưng tập trung nhiều nhất ở vùng 53-54 điểm.
