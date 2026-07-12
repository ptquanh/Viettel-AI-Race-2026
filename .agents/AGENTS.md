# VIETTEL AI RACE - WORKSPACE GENERAL RULES

> Bộ quy tắc này áp dụng chung cho tất cả các Agent hoạt động trong workspace, nhằm đảm bảo quy trình làm việc chuẩn mực, có hệ thống và thống nhất cho mọi bài thi (exercise).

---

## 1. WORKFLOW CHUẨN KHI BẮT ĐẦU TASK

Khi nhận được yêu cầu xử lý một bài thi cụ thể, Agent **BẮT BUỘC** phải tuân thủ luồng làm việc tuyến tính sau đây trước khi thực hiện bất kỳ thay đổi nào:

1. **Hiểu cấu trúc thư mục & Đọc README (Directory Tree & README):**
   - Đọc và phân tích cây thư mục của bài thi (`exercise {N}/`) để xác định chính xác vị trí các folder quan trọng như `docs/`, `submissions/`, `src/`, v.v.
   - Kiểm tra và đọc file `README.md` ở thư mục gốc của bài thi (nếu có) để nắm được tổng quan chung và hướng dẫn chạy mã nguồn/notebook.
2. **Đọc tài liệu quy định (Docs & Local Rules):**
   - Đọc các tài liệu đặc tả trong thư mục `docs/` của bài thi đó (ví dụ: `challenge_specification.md`).
   - Kiểm tra và đọc file quy định riêng của bài thi (ví dụ: `RULES.md` nằm trong thư mục bài thi) nếu có. File này chứa các ràng buộc kỹ thuật ngặt nghèo riêng biệt cho bài thi đó.
3. **Đọc lịch sử thử nghiệm (Logs):**
   - Đọc file `logs.md` trong thư mục `submissions/` để hiểu rõ tiến độ, những thử nghiệm đã làm, baseline tốt nhất hiện tại, cũng như các thử nghiệm thất bại (Fail) nhằm tránh lặp lại sai lầm.
4. **Đọc kế hoạch cũ (Old Plans):**
   - Đọc các bản kế hoạch (plans) đã được tạo và thực thi trước đó (thường nằm trong thư mục submit theo ngày hoặc trong `docs/`).
5. **Đánh giá & Tìm lỗ hổng (Analyze Gaps):**
   - Phân tích nguyên nhân lỗi, điểm nghẽn (bottleneck) hoặc những hạn chế của plan cũ dựa trên thông tin từ log, trace hoặc phản hồi của user.
6. **Đề xuất kế hoạch mới (Propose New Plan):**
   - Dựa trên các phân tích lỗ hổng, đề xuất một định hướng giải quyết vấn đề và vạch ra kế hoạch (plan) mới, sau đó mới tiến hành code hoặc chạy thử nghiệm.

---

## 2. QUY ĐỊNH VỀ TỔ CHỨC CẤU TRÚC BÀI THI

Mỗi bài thi (Exercise) được quản lý gọn gàng trong thư mục riêng của nó (`exercise 1`, `exercise 2`, `exercise 3`...). Bên trong mỗi bài thi cần duy trì cấu trúc chuẩn mực:

- **`docs/`**: Chứa tất cả tài liệu phân tích, đặc tả đề bài, phân tích trace và chiến lược dài hạn.
- **`submissions/`**: Chứa các bản nộp (được gom theo từng ngày), lịch sử nộp bài và file tổng hợp `logs.md`.
- **`RULES.md` (Tuỳ chọn)**: Chứa các quy định chuyên biệt, công thức tính điểm và ràng buộc kỹ thuật _chỉ áp dụng riêng cho bài thi đó_.
- Các thư mục mã nguồn (`src/`), dữ liệu (`data/`), hoặc scripts tuỳ thuộc vào yêu cầu bài toán.

---

## 3. QUY ĐỊNH GHI NHẬT KÝ (LOGGING) VÀ BÁO CÁO

- Mọi sự thay đổi đáng kể mang tính thử nghiệm (chỉnh sửa cấu hình, tham số, thêm thuật toán, thay đổi image) đều **bắt buộc phải được ghi nhận vào `logs.md`** của bài thi tương ứng.
- Khi ghi log, cần nêu bật được: Ý tưởng thay đổi là gì? Mục đích của sự thay đổi đó? Kết quả đạt được như thế nào? Nếu lỗi thì do nguyên nhân gì?
- Sau mỗi lần nộp bài hoặc chạy benchmark thành công/thất bại, phải cập nhật file kết quả tương ứng và file logs.md ngay lập tức.
