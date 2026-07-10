# PROJECT RULES - VIETTEL AI RACE OPTIMIZATION

> Bộ quy tắc bắt buộc áp dụng đối với tất cả các Agent hoạt động trong workspace này nhằm đảm bảo tính kỷ luật, tránh lặp lại sai lầm và duy trì lịch sử thử nghiệm chuẩn xác.

---

## 1. PROTOCOL ĐỌC THÔNG TIN & NHẬT KÝ (MANDATORY BEFORE ACTION)

Trước khi thực hiện bất kỳ đề xuất thay đổi hoặc tạo file cấu hình mới nào, Agent **BẮT BUỘC** phải:

1. **Đọc lịch sử cuộc thi & logs:** Đọc file [logs.md](../exercise%203/submissions/logs.md) để:
   - Hiểu rõ baseline tốt nhất hiện tại (ví dụ: cấu hình STT 21 đạt 18.99 điểm).
   - Nhận diện các cấu hình đã thử nghiệm thất bại (Fail) hoặc bỏ qua (Skip) để tránh lặp lại sai lầm.
2. **Phân tích cấu hình Model & Kiến trúc:**
   - Đọc file `config.json` của model mục tiêu (ví dụ: [config.json](../exercise%203/Qwen3.5-2B-BTC/config.json)) để nắm rõ `model_type`, `architectures`, `layer_types` (như hybrid linear attention), tránh đưa các flag không tương thích hoặc chọn sai backend engine (ví dụ: chọn Turbomind khi model có linear attention).
3. **Kiểm tra giới hạn tài nguyên:** Xác định tài nguyên thực tế được cấp. Cấu hình phần cứng thực tế của BTC cấp phát tự động cho mỗi lượt chấm là: **1 instance MiG H200 (18GB VRAM, 3 Core CPU, 8GB RAM)**.

---

## 2. QUY TRÌNH NỘP BÀI CHUẨN (SUBMISSION WORKFLOW)

Mỗi lần đề xuất một cấu hình nộp bài mới, Agent phải tuân thủ nghiêm ngặt quy trình sau:

### Bước 1: Tạo cấu trúc thư mục nộp bài chuẩn

Tất cả các thử nghiệm phải được lưu trong thư mục theo định dạng: `exercise 3/submissions/{DDMMYYYY}/` (ví dụ: `09072026`).
Mỗi lượt nộp bao gồm 2 file bắt buộc:

1. **File Compose:** `{HHMM}-docker-compose.yml` (ví dụ: `0732-docker-compose.yml`).
2. **File Kết quả:** `{HHMM}-result.md` (ví dụ: `0732-result.md`).

### Bước 2: Cấu trúc chuẩn của file `{HHMM}-result.md`

File kết quả ban đầu khi nộp bài phải có định dạng:

```markdown
# Kết quả Benchmark - {HH:MM} {DD/MM/YYYY} (STT {Số thứ tự} - {Tên cấu hình/Ý tưởng tối ưu})

- **Cấu hình**: Image `{Tên image}` + các tham số bổ sung.
- **Mục đích**: {Mô tả ngắn gọn ý tưởng thử nghiệm, tham số đơn biến thay đổi}.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
```

---

## 3. PROTOCOL CẬP NHẬT PLAN & LOGS SAU MỖI LẦN NỘP

Ngay sau khi có kết quả từ portal (hoặc khi phát hiện lỗi khởi động/chấm điểm thất bại), Agent **BẮT BUỘC** phải:

1. **Cập nhật File Kết quả `{HHMM}-result.md`:**
   - Thay thế trạng thái `TBD` bằng kết quả chi tiết: điểm đạt được, số request passed SLO (ví dụ: `86/120`), TTFT, TPOT.
   - Nếu thất bại, phải copy toàn bộ trace lỗi/log container thu thập được và đưa ra phân tích nguyên nhân kỹ thuật cụ thể.
2. **Cập nhật Nhật ký tổng hợp [logs.md](../exercise%203/submissions/logs.md):**
   - Bổ sung một dòng mới vào bảng kết quả với định dạng chuẩn:
     `| {STT} | {Đường dẫn thư mục nộp} | {Mô tả cấu hình/Image} | **{Điểm số/Fail/Skip}** | {Chi tiết thay đổi/Ý tưởng} | {Kết luận rút ra/Lý do lỗi} |`
   - Cập nhật phần lưu ý nếu có phát hiện quan trọng.
3. **Cập nhật Implementation Plan (`implementation_plan.md`):** Đánh giá xem hướng đi hiện tại có cần điều chỉnh (ví dụ: chuyển từ tối ưu LMDeploy sang quay lại tối ưu vLLM).

---

## 4. QUY ĐỊNH VỀ QUANTIZATION

- **Quy tắc bắt buộc:** Hiện tại, bài thi này chỉ hỗ trợ **Online Quantization** (lượng tử hóa động khi load model), **KHÔNG** hỗ trợ offline quantization dưới dạng các pre-quantize model weight (như các checkpoint model AWQ, GPTQ được tải sẵn từ ngoài vào). Agent không được thử nghiệm nạp weights pre-quantized từ bên ngoài.

---

## 5. QUY ĐỊNH VỀ SERVING FRAMEWORK

- **Quy tắc bắt buộc:** Bài thi này chỉ hỗ trợ và chạy ổn định trên **vLLM framework**. Hệ thống grader chấm bài tự động ép buộc cấu hình chạy của vLLM. Không thử nghiệm các serving framework khác (như SGLang, LMDeploy, Aphrodite, v.v.) vì chúng không tương thích hoặc gây timeout/lỗi hệ thống khi chấm bài.
