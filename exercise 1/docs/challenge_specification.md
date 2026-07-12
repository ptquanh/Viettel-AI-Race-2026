# 🚀 [Bài 1] Digital Twin BTS - 3D Reconstruction & Novel View Synthesis - Specification

Tài liệu này tổng hợp toàn bộ thông tin chính thức từ Ban Tổ Chức (BTC) về yêu cầu, cấu trúc dữ liệu, cơ chế tính điểm, hình thức thi và quy định của bài toán Digital Twin cho trạm BTS.

---

## 1. 📝 Tổng quan bài toán

Mục tiêu của bài toán là xây dựng mô hình AI có khả năng tái dựng cấu trúc không gian 3D của một scene (cảnh) từ tập ảnh đa góc nhìn (multi-view) và sinh ra ảnh RGB tại các góc nhìn mới (novel view synthesis) chưa từng xuất hiện trong dữ liệu huấn luyện đầu vào.

Hướng tiếp cận này đóng vai trò quan trọng trong việc xây dựng **Digital Twin** (bản sao số 3D) có độ chính xác cao của hạ tầng viễn thông, phục vụ công tác giám sát, kiểm tra, bảo trì và quy hoạch lắp đặt thiết bị.

* **Nguồn dữ liệu:**
  * Drone bay quanh đối tượng.
  * Camera cầm tay (hand-held camera).
* **Đối tượng trong scene:**
  * Trạm BTS.
  * Công trình hạ tầng.
  * Các đối tượng thực tế khác.
* **Lĩnh vực chuyên môn:**
  * Computer Vision (Thị giác máy tính).
  * 3D Vision (Thị giác 3D).
  * Neural Rendering (Kết xuất đồ họa neural).
  * Novel View Synthesis (Tổng hợp góc nhìn mới).
  * Digital Twin (Bản sao số).

---

## 2. 📁 Cấu trúc dữ liệu

Mỗi scene dữ liệu được cung cấp dưới cấu trúc chuẩn sau:

```text
├── train/
│   ├── images/          : Tập ảnh RGB dùng cho training (huấn luyện)
│   └── sparse/0/        : Kết quả phục dựng thưa (Sparse reconstruction) từ COLMAP
│                           ├── cameras.bin  (Thông số camera intrinsics)
│                           ├── images.bin   (Thông số camera extrinsics / poses)
│                           └── points3D.bin (Tập điểm 3D thưa)
└── test/
    └── test_poses.csv   : Camera poses của các góc nhìn mục tiêu cần sinh ảnh test
```

---

## 3. 📊 Thông tin dữ liệu

* **Phân chia dữ liệu:**
  * **Train images:** Chiếm khoảng **~80%** lượng ảnh chụp của scene.
  * **Test images:** Chiếm khoảng **~20%** lượng ảnh còn lại.
* **Camera poses & Sparse reconstruction:** Đã được dựng sẵn bằng công cụ **COLMAP** và cung cấp trực tiếp cho thí sinh làm đầu vào định hướng hình học.

---

## 4. 📄 Định dạng file `test_poses.csv`

Mỗi dòng trong file `test_poses.csv` mô tả thông số camera và pose tương ứng với ảnh cần sinh ở tập test:

```csv
image_name, qw, qx, qy, qz, tx, ty, tz, fx, fy, cx, cy, width, height
```

**Chi tiết các trường dữ liệu:**

| Trường dữ liệu | Ý nghĩa |
| :--- | :--- |
| `image_name` | Tên của ảnh đầu ra cần sinh (ví dụ: `0001.png`) |
| `qw, qx, qy, qz` | Tham số Quaternion biểu diễn phép quay (Rotation) của camera theo định dạng COLMAP |
| `tx, ty, tz` | Phép dịch chuyển (Translation) của camera |
| `fx, fy` | Tiêu cự camera (Focal length) theo hai trục |
| `cx, cy` | Điểm chính (Principal point) của cảm biến camera |
| `width, height` | Kích thước (chiều rộng, chiều cao) của ảnh cần sinh |

---

## 5. 📥 Đầu vào & 📤 Đầu ra của bài toán

### A. Đầu vào (Inputs)
* Tập ảnh train đa góc nhìn (RGB).
* Thông số nội tại camera (Camera intrinsics).
* Thông số tư thế camera (Camera poses).
* Phục dựng thưa (Sparse reconstruction) từ COLMAP.
* Danh sách camera poses mục tiêu cần sinh (`test_poses.csv`).

### B. Đầu ra (Outputs)
* Sinh ảnh RGB tương ứng với toàn bộ các test poses được cung cấp trong `test_poses.csv`.
* **Yêu cầu đối với ảnh sinh:**
  * Đúng cấu trúc hình học của scene.
  * Đúng vị trí của các vật thể/hạ tầng trong không gian.
  * Đảm bảo chất lượng hình ảnh chân thực, sắc nét và nhất quán với tập train.

---

## 6. 📦 Định dạng nộp bài (Submission Format)

Thí sinh nộp bài dưới dạng một file nén **ZIP** chứa toàn bộ ảnh kết quả được phân chia theo từng thư mục scene tương ứng:

```text
submission.zip
├── scene_001/
│   ├── 0001.png
│   ├── 0002.png
│   └── ...
├── scene_002/
│   ├── 0001.png
│   └── ...
└── ...
```

> [!IMPORTANT]
> **Yêu cầu bắt buộc khi nộp bài:**
> * Đúng số lượng và tên các scene được yêu cầu.
> * Đúng tên file ảnh theo quy định của file `test_poses.csv`.
> * Đúng kích thước ảnh (`width`, `height`) được chỉ định.
> * Đúng số lượng ảnh ở mỗi scene.

---

## 7. 📏 Chỉ số đánh giá & Công thức tính điểm (Metrics & Evaluation)

Kết quả nộp bài được so sánh trực tiếp với ảnh ground-truth (ảnh thực tế do BTC giữ lại làm đáp án) thông qua 3 chỉ số chính:

### 7.1 LPIPS (Learned Perceptual Image Patch Similarity)
Đánh giá độ tương đồng cảm quan giữa ảnh sinh ra và ảnh gốc bằng cách trích xuất đặc trưng sâu (deep features).
* **Giá trị:** Càng **thấp** càng tốt.
* **Tham khảo:** Zhang et al., *"The Unreasonable Effectiveness of Deep Features as a Perceptual Metric"*, CVPR 2018. [arXiv:1801.03924](https://arxiv.org/abs/1801.03924)

### 7.2 SSIM (Structural Similarity Index Measure)
Đánh giá độ tương đồng cấu trúc, độ tương phản và độ sáng giữa hai ảnh.
* **Giá trị:** Càng **cao** càng tốt.
* **Tham khảo:** Wang et al., *"Image quality assessment: from error visibility to structural similarity"*, IEEE TIP 2004. [doi:10.1109/TIP.2003.819861](https://doi.org/10.1109/TIP.2003.819861)

### 7.3 PSNR (Peak Signal-to-Noise Ratio)
Đánh giá sai số trung bình bình phương (MSE) ở mức độ pixel giữa ảnh dự đoán và ground-truth.
* **Giá trị:** Càng **cao** càng tốt.
* **Chuẩn hóa giá trị (Normalize):** Để kết hợp với các metrics khác, PSNR sẽ được chuẩn hóa về khoảng $[0,1]$ theo công thức:

$$PSNR_{norm} = \text{clamp}\left( \frac{PSNR_{val}}{PSNR_{max}}, 0.0, 1.0 \right)$$

*Trong đó:*
* $PSNR_{val}$ là giá trị PSNR thực tế của ảnh sinh.
* $PSNR_{max}$ là ngưỡng PSNR tối đa được lựa chọn trước bởi BTC.
* Hàm $\text{clamp}(x, 0.0, 1.0)$ dùng để giới hạn giá trị của $x$ luôn nằm trong đoạn $[0, 1]$.

### 7.4 Công thức tính điểm cuối cùng (Final Score)

$$Score = 0.4 \times (1 - LPIPS) + 0.3 \times SSIM + 0.3 \times PSNR_{norm}$$

> [!NOTE]
> Điểm số hiển thị trên Bảng xếp hạng (Leaderboard) là điểm trung bình của toàn bộ các scene. Nếu bài nộp bị thiếu hoặc thừa scene so với dữ liệu ground-truth, kết quả chấm sẽ bị từ chối (không được tính điểm).

---

## 8. 🏁 Hình thức thi & Cập nhật vòng thi

* Dữ liệu và các scene hoàn toàn mới sẽ được cung cấp cho mỗi vòng thi.
* Cách thức tính điểm (công thức Score) được giữ nguyên giữa các vòng.

---

## 9. 🛡️ Quy định chống gian lận & Đảm bảo tính công bằng

### 9.1 Cấm sử dụng dữ liệu ngoài
* Thí sinh chỉ được sử dụng dữ liệu do BTC cung cấp chính thức trong từng vòng thi.
* **Nghiêm cấm:**
  * Sử dụng hình ảnh, video hoặc dữ liệu 3D từ các nguồn bên ngoài chứa cùng đối tượng hoặc cùng scene với bộ dữ liệu thi.
  * Tự thu thập thêm dữ liệu thực địa hoặc khai thác dữ liệu liên quan trực tiếp đến các trạm BTS từ Internet.
  * Sử dụng bất kỳ nguồn thông tin nào nhằm tái tạo hoặc suy luận ground-truth của tập test.

### 9.2 Cấm truy xuất hoặc suy đoán dữ liệu kiểm thử
* Nghiêm cấm mọi hành vi xâm nhập trái phép vào hệ thống chấm bài để lấy dữ liệu ground-truth.
* Nghiêm cấm khai thác lỗ hổng hệ thống để thu thập thông tin về ảnh kiểm thử.

### 9.3 Yêu cầu khả năng tái lập kết quả (Reproducibility)
BTC có quyền yêu cầu các đội đạt thứ hạng cao cung cấp đầy đủ:
* Mã nguồn huấn luyện (training code) và suy luận (inference code).
* File cấu hình hệ thống (config files).
* Danh sách các thư viện và phiên bản cụ thể (requirements.txt / environment.yml).
* Checkpoint của mô hình đã huấn luyện.
* Nhật ký chạy huấn luyện (training logs).

> [!WARNING]
> Đội thi có nghĩa vụ chứng minh kết quả nộp bài trên hệ thống hoàn toàn có thể được tái lập (reproduce) từ pipeline đã cung cấp.

### 9.4 Cấm chỉnh sửa thủ công ảnh đầu ra
* Toàn bộ ảnh kết quả nộp lên hệ thống bắt buộc phải được sinh hoàn toàn tự động bằng thuật toán hoặc mô hình AI.
* **Nghiêm cấm:**
  * Chỉnh sửa thủ công từng ảnh bằng các phần mềm chỉnh sửa đồ họa (Photoshop, GIMP...).
  * Thực hiện cắt ghép, vẽ thêm hoặc xóa bớt vật thể thủ công.
  * Can thiệp thủ công vào các test pose riêng lẻ.

---

## 10. 💡 Giải pháp Baseline tham khảo

Thí sinh có thể tham khảo cài đặt gốc của thuật toán phục dựng 3D nổi bật:
* **3D Gaussian Splatting:** [graphdeco-inria/gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting)

---

## 🏆 Vòng 1 - Sơ loại

### 1. Mô tả vòng thi
Vòng thi đầu tiên của VAR 2026 - Digital Twin cho trạm BTS.
* Ban tổ chức công bố tập **public set** và **private test #1** gồm các scenes khác nhau.
* Thí sinh xây dựng pipeline và tự đánh giá hiệu năng trên tập **public set**.
* Khi có tập **private test #1**, thí sinh sử dụng ảnh training của từng scene để tối ưu/huấn luyện mô hình và sinh ảnh RGB tại các góc nhìn mục tiêu chỉ định trong file `test_poses.csv`.

### 2. Thông tin dữ liệu Vòng 1

| Hạng mục | Thông tin chi tiết |
| :--- | :--- |
| **Số ảnh/scene** | 150 - 300 ảnh RGB |
| **Số poses mục tiêu/scene** | 40 - 70 poses |
| **Dung lượng bộ dữ liệu** | 200 - 300 MB |

*Cấu trúc thư mục tương tự cấu trúc chung được mô tả tại mục 2.*

### 3. Yêu cầu nộp bài Vòng 1
File nộp là file nén ZIP chứa toàn bộ ảnh sinh ra theo đúng cấu trúc:

```text
submission_round1.zip
├── scene_001/
│   ├── 0001.png
│   ├── 0002.png
│   └── ...
├── scene_002/
│   ├── 0001.png
│   └── ...
└── ...
```

* **Kích thước ảnh:** Đúng khớp với `width` và `height` trong `test_poses.csv`.
* **Tên file:** Đúng khớp với `image_name` trong `test_poses.csv`.
* **Độ đầy đủ:** Thiếu bất kỳ ảnh nào của bất kỳ scene nào đều không được tính điểm.

### 4. Kế hoạch thời gian (Timeline) Vòng 1

| Mốc thời gian | Sự kiện |
| :--- | :--- |
| **02/07/2026** | Công bố private test #1 - Mở tải dữ liệu |
| **30/07/2026** | Hạn cuối nộp bài (Deadline submission) |

*Thí sinh có quyền nộp nhiều lần. Hệ thống sẽ ghi nhận và chấm bản submit cuối cùng được tải lên trước thời điểm deadline.*

### 5. Một số lưu ý riêng cho Vòng 1
* Đây là vòng làm quen dữ liệu thực tế: Hãy kiểm tra kỹ pipeline trên dữ liệu training public trước khi chạy chính thức trên private test.
* Hạ tầng huấn luyện do thí sinh tự chuẩn bị. Hãy tính toán và ước lượng thời gian chạy để đảm bảo kịp deadline.
* **Cấu hình tham khảo khuyến nghị cho mỗi job inference:**
  * 1 × GPU NVIDIA RTX A4000 (20 GB VRAM)
  * 4 - 8 CPU Cores
  * 16 - 32 GB System RAM
* Mọi thắc mắc kỹ thuật về dữ liệu hoặc submission liên hệ kênh hỗ trợ chính thức của BTC.
