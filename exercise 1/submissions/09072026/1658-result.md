# Kết quả Submission - 16:58 09/07/2026 (STT 3 - Baseline GS 15k Iterations - Run 2 / Test Sai Số)

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
- **Mục đích**: Thử nghiệm lặp lại cấu hình mặc định (lần thứ 2) nhằm đo lường sai số và độ biến động kết quả (grading variance) của hệ thống chấm bài với baseline 15k.

## Chỉ số đo được

| Chỉ số           |    Giá trị    | Ý nghĩa                                                        |
| :--------------- | :-----------: | :------------------------------------------------------------- |
| `Điểm` (Score)   | **52.48840**  | Điểm số tổng hợp cuối cùng                                     |
| `PSNR`           | **18.385057** | Peak Signal-to-Noise Ratio (càng cao càng tốt)                 |
| `SSIM`           |  **52.0853**  | Structural Similarity (càng cao càng tốt)                      |
| `LPIPS`          |  **35.4205**  | Learned Perceptual Image Patch Similarity (càng thấp càng tốt) |
| `num_scenes`     |     **8**     | Tổng số scene được hệ thống đánh giá                           |
| `matched_scenes` |     **8**     | Số scene khớp với ground-truth                                 |

## Phân tích kết quả

1. **Phân tích sai số khi chấm bài (so sánh với Run 1 và Run 6)**:
   - Điểm số của Run 2 (`52.48840`) giảm rất mạnh so với Run 1 (`54.97630` - giảm 2.49 điểm) và Run 6 (`55.65110` - giảm 3.16 điểm).
   - Sự sụt giảm xảy ra đồng đều ở tất cả chỉ số: PSNR giảm xuống `18.39dB`, SSIM giảm xuống `52.09%`, LPIPS tăng lên `35.42%`.
   - Kết quả này xác nhận hệ thống chấm điểm hoặc quá trình training/suy luận của mô hình (trên Kaggle/Colab của thí sinh) có độ bất ổn định và sai số ngẫu nhiên rất lớn (lên tới hơn 3 điểm), có thể do:
     - Tính ngẫu nhiên cao khi huấn luyện mô hình 3D Gaussian Splatting (khởi tạo điểm ngẫu nhiên, ngẫu nhiên hóa việc lựa chọn ảnh huấn luyện nếu không cố định seed).
     - Sự không đồng nhất về phần cứng hoặc môi trường chạy suy luận (sinh ảnh rasterization trên các thiết bị GPU khác nhau của hệ thống portal có thể tạo ra sai lệch pixel nhỏ ảnh hưởng đến PSNR/SSIM).
2. **Kết luận**:
   - Cần thiết lập cơ chế cố định seed (seed initialization, dataloader shuffle seed) trong code huấn luyện để giảm thiểu sự ngẫu nhiên này.
   - Khi đánh giá cải tiến, các thay đổi làm tăng dưới 3 điểm trên portal có thể chỉ là do sai số ngẫu nhiên (noise) chứ không phải do giải pháp thực sự tốt hơn.
