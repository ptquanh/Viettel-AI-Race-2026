# EXERCISE 1 RULES - DIGITAL TWIN BTS

> Đây là bộ quy tắc và ràng buộc kỹ thuật ĐẶC THÙ dành riêng cho **Bài 1 (3D Reconstruction & Novel View Synthesis)**. Các quy tắc này có độ ưu tiên cao nhất khi thao tác trong phạm vi thư mục `exercise 1`.

---

## 1. PROTOCOL ĐỌC THÔNG TIN & NHẬT KÝ (MANDATORY BEFORE ACTION)

Trước khi thực hiện bất kỳ đề xuất thay đổi hoặc tạo cấu hình training/inference mới nào, Agent **BẮT BUỘC** phải:

1. **Đọc lịch sử cuộc thi & logs:** Đọc file `submissions/logs.md` để:
   - Hiểu rõ baseline tốt nhất hiện tại (ví dụ: mô hình đạt bao nhiêu điểm).
   - Nhận diện các cấu hình đã thử nghiệm thất bại (Fail) để tránh lặp lại sai lầm.
2. **Đọc tài liệu Specs:** Đọc `docs/challenge_specification.md` để nắm rõ yêu cầu ảnh đầu ra, cấu trúc folder nộp bài (submission.zip) và công thức tính điểm LPIPS/SSIM/PSNR.
3. **Hiểu rõ phương pháp hiện tại:** Nắm vững mã nguồn trong các file Notebook (`kaggle_train.ipynb`, `kaggle_inference_submission.ipynb`) và các hyper-parameters đang được sử dụng.

---

## 2. QUY TRÌNH NỘP BÀI CHUẨN (SUBMISSION WORKFLOW)

Mỗi lần đề xuất một cấu hình nộp bài mới, Agent phải tuân thủ nghiêm ngặt quy trình sau:

### Bước 1: Tạo cấu trúc thư mục nộp bài chuẩn
Tất cả các thử nghiệm phải được lưu trong thư mục theo định dạng: `submissions/{DDMMYYYY}/` (ví dụ: `09072026`).
Mỗi lượt nộp cần lưu lại code/cấu hình sinh ra file ZIP và 1 file kết quả:
- **File Kết quả:** `{HHMM}-result.md` (ví dụ: `0732-result.md`) hoặc `slot{n}-result.md` nếu đang chờ kết quả.

### Bước 2: Cấu trúc chuẩn của file kết quả
File kết quả ban đầu khi vừa nộp bài (trạng thái chờ chấm) phải có định dạng:

```markdown
# Kết quả Submission - {HH:MM} {DD/MM/YYYY} (STT {Số thứ tự} - {Tên cấu hình/Ý tưởng tối ưu})

- **Cấu hình**: {Mô tả hyper-parameters, thay đổi kiến trúc hoặc dữ liệu}.
- **Mục đích**: {Mô tả ngắn gọn ý tưởng thử nghiệm}.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
```

Khi đã có kết quả từ portal chấm điểm, **bắt buộc** phải cập nhật file kết quả theo cấu trúc mẫu chuẩn dưới đây:

```markdown
# Kết quả Submission - {HH:MM} {DD/MM/YYYY} (STT {Số thứ tự} - {Tên cấu hình/Ý tưởng tối ưu})

- **Cấu hình**: {Mô tả hyper-parameters, thay đổi kiến trúc hoặc dữ liệu}.
- **Mục đích**: {Mô tả ngắn gọn ý tưởng thử nghiệm}.

## Chỉ số đo được

| Chỉ số             |    Giá trị    | Ý nghĩa                                             |
| :----------------- | :-----------: | :-------------------------------------------------- |
| `Điểm` (Score)     | **{Điểm}**    | Điểm số tổng hợp cuối cùng                          |
| `PSNR`             | **{Số}**      | Peak Signal-to-Noise Ratio (càng cao càng tốt)      |
| `SSIM`             | **{Số}**      | Structural Similarity (càng cao càng tốt)           |
| `LPIPS`            | **{Số}**      | Learned Perceptual Image Patch Similarity (càng thấp càng tốt)|
| `num_scenes`       | **{Số}**      | Tổng số scene được hệ thống đánh giá                |
| `matched_scenes`   | **{Số}**      | Số scene khớp với ground-truth                      |

## Phân tích kết quả
1. **Phân tích chất lượng ảnh**:
   - {Chi tiết phân tích các chỉ số so với baseline. Tại sao LPIPS tăng/giảm? PSNR cải thiện ở điểm nào?}
2. **Kết luận**:
   - {Đánh giá chung cấu hình này có nên đưa làm baseline mới hay loại bỏ/thay đổi}.
```

---

## 3. PROTOCOL CẬP NHẬT PLAN & LOGS SAU MỖI LẦN NỘP

Ngay sau khi có kết quả (hoặc phát hiện lỗi tạo ảnh), Agent **BẮT BUỘC** phải:
1. **Cập nhật File Kết quả `{HHMM}-result.md`:** Điền kết quả chi tiết các metrics.
2. **Cập nhật Nhật ký tổng hợp `submissions/logs.md`:** 
   - Thêm dòng mới vào bảng lịch sử theo định dạng chuẩn:
     `| {STT} | {Thư mục nộp} | {Mô tả thay đổi} | **{Điểm số}** | PSNR/SSIM/LPIPS | {Kết luận rút ra} |`
3. **Đánh giá lại Plan:** Xem xét lại định hướng tối ưu trong các file kế hoạch (`docs/` hoặc trong ngày).

---

## 4. QUY ĐỊNH VỀ TỰ ĐỘNG HÓA VÀ DỮ LIỆU
- **Dữ liệu:** Tuyệt đối không dùng dữ liệu ngoài (ảnh, video khác ngoài tập train).
- **Tự động hóa:** File nộp (submission.zip) phải được sinh tự động 100% bằng code. Không can thiệp sửa ảnh thủ công.
