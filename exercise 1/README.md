# 🌐 Bài 1: Digital Twin BTS - Reconstruction & Synthesis

Thư mục này chứa mã nguồn, dữ liệu huấn luyện/suy luận và tài liệu đặc tả của **Bài 1 (Digital Twin cho trạm BTS)** thuộc cuộc thi Viettel AI Race 2026.

---

## 📂 Cấu trúc thư mục (Directory Structure)

```text
exercise 1/
├── docs/
│   └── challenge_specification.md  : Đặc tả bài toán, metrics và quy chế thi chi tiết
├── kaggle_train.ipynb              : Notebook chạy huấn luyện mô hình (training pipeline)
└── kaggle_inference_submission.ipynb: Notebook chạy suy luận và tạo file nộp bài (inference & submission)
```

---

## 📖 Tài liệu hướng dẫn (Documentation)

Chi tiết về bài toán, dữ liệu, định dạng file poses, metric đánh giá (LPIPS, SSIM, PSNR) và các quy định của cuộc thi được lưu trữ tại:
👉 **[Tài liệu Đặc tả Bài toán (Challenge Specification)](docs/challenge_specification.md)**

---

## 🛠️ Hướng dẫn sử dụng (Quick Start)

1. **Huấn luyện mô hình:**
   - Sử dụng notebook [kaggle_train.ipynb](kaggle_train.ipynb) để thiết lập môi trường và chạy huấn luyện mô hình dựa trên giải pháp baseline (ví dụ: _3D Gaussian Splatting_).
2. **Suy luận & Tạo submission:**
   - Sau khi hoàn tất training, sử dụng notebook [kaggle_inference_submission.ipynb](kaggle_inference_submission.ipynb) để thực hiện Novel View Synthesis dựa trên các camera poses mục tiêu trong tập test.
   - Kết quả đầu ra sẽ được đóng gói thành file `submission_round1.zip` để nộp lên hệ thống.
