# EXERCISE 3 RULES - LLM INFERENCE OPTIMIZATION

> Đây là bộ quy tắc và ràng buộc kỹ thuật ĐẶC THÙ dành riêng cho **Bài 3**. Các quy tắc này có độ ưu tiên cao nhất khi thao tác trong phạm vi thư mục `exercise 3`.

---

## 1. PROTOCOL ĐỌC THÔNG TIN & NHẬT KÝ (MANDATORY BEFORE ACTION)

Trước khi thực hiện bất kỳ đề xuất thay đổi hoặc tạo file cấu hình mới nào, Agent **BẮT BUỘC** phải:

1. **Đọc lịch sử cuộc thi & logs:** Đọc file `submissions/logs.md` để:
   - Hiểu rõ baseline tốt nhất hiện tại (ví dụ: cấu hình STT 21 đạt 18.99 điểm).
   - Nhận diện các cấu hình đã thử nghiệm thất bại (Fail) hoặc bỏ qua (Skip) để tránh lặp lại sai lầm.
2. **Đọc tài liệu Specs & Kế hoạch chiến lược:** Đọc `docs/challenge_specification.md` và `docs/phase1_execution_plan.md` để nắm rõ luật thi, cơ chế tính điểm ERS/Accuracy và định hướng tối ưu chung đã được thống nhất.
3. **Phân tích cấu hình Model & Kiến trúc:**
   - Đọc file `config.json` của model mục tiêu (ví dụ: `Qwen3.5-2B-BTC/config.json`) để nắm rõ `model_type`, `architectures`, `layer_types` (như hybrid linear attention), tránh đưa các flag không tương thích hoặc chọn sai backend engine (ví dụ: chọn Turbomind khi model có linear attention).
4. **Kiểm tra giới hạn tài nguyên:** Xác định tài nguyên thực tế được cấp. Cấu hình phần cứng thực tế của BTC cấp phát tự động cho mỗi lượt chấm là: **1 instance MiG H200 (18GB VRAM, 3 Core CPU, 8GB RAM)**.

---

## 2. QUY TRÌNH NỘP BÀI CHUẨN (SUBMISSION WORKFLOW)

Mỗi lần đề xuất một cấu hình nộp bài mới, Agent phải tuân thủ nghiêm ngặt quy trình sau:

### Bước 1: Tạo cấu trúc thư mục nộp bài chuẩn
Tất cả các thử nghiệm phải được lưu trong thư mục theo định dạng: `submissions/{DDMMYYYY}/` (ví dụ: `09072026`).
Mỗi lượt nộp bao gồm 2 file bắt buộc:
1. **File Compose:** `{HHMM}-docker-compose.yml` (ví dụ: `0732-docker-compose.yml`) hoặc `slot{n}-docker-compose.yml` nếu chưa nộp.
2. **File Kết quả:** `{HHMM}-result.md` (ví dụ: `0732-result.md`) hoặc `slot{n}-result.md` nếu chưa nộp.

- **Quy định đặt tên theo trạng thái**:
  - Đối với cấu hình **chưa nộp hoặc chưa có kết quả benchmark**, file phải đặt tên là `slot{n}-docker-compose.yml` và `slot{n}-result.md` (với `n` là 1, 2, 3...).
  - Ngay sau khi đã nộp hoặc có kết quả từ portal, **bắt buộc** phải đổi tên file từ `slot{n}` sang giờ nộp thực tế dạng `{HHMM}`.

### Bước 2: Cấu trúc chuẩn của file kết quả
File kết quả ban đầu khi nộp bài (trạng thái chờ) phải có định dạng:

```markdown
# Kết quả Benchmark - {HH:MM} {DD/MM/YYYY} (STT {Số thứ tự} - {Tên cấu hình/Ý tưởng tối ưu})

- **Cấu hình**: Image `{Tên image}` + các tham số bổ sung.
- **Mục đích**: {Mô tả ngắn gọn ý tưởng thử nghiệm, tham số đơn biến thay đổi}.

## Chỉ số đo được

**Đang chờ kết quả benchmark (TBD)**
```

Khi đã có kết quả từ portal, **bắt buộc** phải cập nhật file kết quả theo cấu trúc mẫu chuẩn dưới đây:

```markdown
# Kết quả Benchmark - {HH:MM} {DD/MM/YYYY} (STT {Số thứ tự} - {Tên cấu hình/Ý tưởng tối ưu})

- **Cấu hình**: Image `{Tên image}` + các tham số bổ sung.
- **Mục đích**: {Mô tả ngắn gọn ý tưởng thử nghiệm, tham số đơn biến thay đổi}.

## Chỉ số đo được

| Chỉ số          |    Giá trị    | Ý nghĩa                                             |
| :-------------- | :-----------: | :-------------------------------------------------- |
| `final_score`   |  **{Điểm}**   | Điểm số cuối cùng                                   |
| `ers`           |  **{Điểm}**   | Điểm số hiệu năng (Effective Request Score)         |
| `erc`           |   **{ERC}**   | Tỷ lệ hoàn thành hiệu quả (Effective Request Ratio) |
| `penalty`       | **{Penalty}** | Hệ số phạt (1 = Không bị phạt)                      |
| `passed_slo`    |   **{Số}**    | Số lượng request đạt chuẩn SLO                      |
| `total_count`   |    **120**    | Tổng số request benchmark                           |
| `failed_count`  |   **{Số}**    | Số lượng request thất bại                           |
| `warmup_count`  |   **{Số}**    | Số lượng request warmup                             |
| `accuracy_drop` |   **{Số}%**   | Độ sụt giảm độ chính xác                            |
| `tbt_median_ms` |  **{Số} ms**  | Median Time Between Tokens (TPOT)                   |
| `ttft_p50_ms`   |  **{Số} ms**  | Time To First Token (P50)                           |
| `ttft_p95_ms`   |  **{Số} ms**  | Time To First Token (P95)                           |

## Phân tích kết quả
1. **{Tiêu đề phân tích hiệu năng}**:
   - {Chi tiết phân tích, so sánh với baseline, ảnh hưởng của cấu hình đối với TTFT/TPOT}.
2. **{Tiêu đề phân tích độ chính xác}**:
   - {Ảnh hưởng của cấu hình đến độ sụt giảm accuracy (GPQA Diamond)}.
3. **Kết luận**:
   - {Đánh giá chung cấu hình này có nên đưa làm baseline mới hay loại bỏ/thay đổi}.
```

---

## 3. PROTOCOL CẬP NHẬT PLAN & LOGS SAU MỖI LẦN NỘP

Ngay sau khi có kết quả từ portal (hoặc phát hiện lỗi), Agent **BẮT BUỘC** phải:
1. **Cập nhật File Kết quả `{HHMM}-result.md`:** Điền kết quả chi tiết (điểm, passed SLO, TTFT, TPOT). Nếu thất bại, copy toàn bộ trace/log và phân tích lỗi kỹ thuật.
2. **Cập nhật Nhật ký tổng hợp `submissions/logs.md`:** 
   - Thêm dòng mới vào bảng: `| {STT} | {Đường dẫn} | {Mô tả cấu hình/Image} | **{Điểm số/Fail/Skip}** | {Chi tiết thay đổi} | {Kết luận rút ra} |`
3. **Cập nhật Implementation Plan (`docs/implementation_plan.md`):** Đánh giá hướng đi hiện tại có cần điều chỉnh không.

---

## 4. QUY ĐỊNH VỀ QUANTIZATION
- **Bắt buộc:** Chỉ hỗ trợ **Online Quantization** (lượng tử hóa động khi load model), **KHÔNG** hỗ trợ offline quantization (pre-quantized weights như AWQ, GPTQ tải sẵn từ ngoài vào). 

---

## 5. QUY ĐỊNH VỀ SERVING FRAMEWORK
- **Bắt buộc:** Chỉ chạy ổn định trên **vLLM framework**. Grader ép buộc cấu hình vLLM. Tuyệt đối không thử nghiệm framework khác (SGLang, LMDeploy, Aphrodite...) vì sẽ gây timeout hoặc lỗi khởi động.

---

## 6. QUY ĐỊNH GHI NHẬT KÝ THAY ĐỔI IMAGE & HIJACK
- Mỗi lần sửa đổi docker image (đổi tên/tag) hoặc script hijack, phải:
  1. Ghi chi tiết vào `submissions/logs.md`.
  2. Tạo/cập nhật file kế hoạch ngày hôm đó (ví dụ: `submissions/{DDMMYYYY}/plan-{DDMM}.md`) để ghi nhận ý tưởng, tham số.
  3. Các phân tích chung về trace/score phải tham chiếu tới `docs/trace_and_score_analysis.md`.
