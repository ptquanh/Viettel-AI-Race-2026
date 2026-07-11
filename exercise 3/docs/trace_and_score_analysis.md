# Phân tích Workload Trace & Công thức Điểm (Viettel AI Race)

Tài liệu này lưu trữ các phân tích dùng chung về cấu trúc dữ liệu trace benchmark và suy diễn công thức tính điểm của Ban tổ chức để tái sử dụng cho các kế hoạch tối ưu.

---

## 1. Phân tích Trace Data (Workload Structure)

### Cấu trúc Workload (dựa trên trace-round1.jsonl)

| Chỉ số | Giá trị |
| :--- | :--- |
| **Tổng requests** | 120 |
| **Cấu trúc** | **20 conversation chains x 6 turns** |
| **Arrival pattern** | 6 bursts x 20 requests, cách nhau 5 giây |
| **max_tokens** | 200 (tất cả) |
| **temperature** | 0 (deterministic) |
| **seed** | 42 (cố định) |
| **System prompt** | **Duy nhất 1 prompt cho tất cả 120 requests** |

### Chi tiết Conversation Chains

```
Chain #0: req[0] -> req[20] -> req[40] -> req[60] -> req[80] -> req[100]
Chain #1: req[1] -> req[21] -> req[41] -> req[61] -> req[81] -> req[101]
...
Chain #19: req[19] -> req[39] -> req[59] -> req[79] -> req[99] -> req[119]
```

### Các Batch Burst theo thời gian

| Batch | Thời điểm | Messages | Est. Tokens | Mô tả |
| :---: | :-------: | :------: | :---------: | :--- |
| 1 | t=0s | 2 msgs | ~20k tokens | System + User (turn 1) |
| 2 | t=5s | 4 msgs | ~24k tokens | + Assistant response + User (turn 2) |
| 3 | t=10s | 6 msgs | ~28k tokens | + Turn 3 |
| 4 | t=15s | 8 msgs | ~33k tokens | + Turn 4 |
| 5 | t=20s | 10 msgs | ~37k tokens | + Turn 5 |
| 6 | t=25s | 12 msgs | ~42k tokens | + Turn 6 (longest) |

> 💡 **100% Prefix Sharing**: Mỗi request trong batch N là **prefix chính xác** của request tương ứng trong batch N+1. Ví dụ: `req[0]` (2 msgs) là prefix của `req[20]` (4 msgs), `req[40]` (6 msgs), v.v.
>
> Điều này có nghĩa là nếu prefix caching hoạt động tốt, batch 2-6 **KHÔNG cần prefill lại toàn bộ context** mà chỉ cần prefill phần mới (~4k tokens/turn).

---

## 2. Phân tích Công thức Điểm (Reverse-Engineering)

### Công thức tổng quát

```
Score = 100 x ERS x f(Delta)
ERS = (1/120) x SUM(S_request_i)
S_request = w x s_ttft + (1-w) x s_tpot
```

### Kết luận rút ra từ thực nghiệm

- **TPOT 51ms (baseline)**: Đang ở vùng tiệm cận giới hạn dưới của cách tính điểm (ERS gần như không nhận được điểm TPOT).
- **TTFT**: Đóng vai trò quyết định điểm số hiện tại. Toàn bộ 18.99 điểm của baseline (STT 21) đến từ điểm TTFT của 85 requests pass SLO.
- **Để bứt phá (70+ điểm)**:
  1. Bắt buộc phải đưa TPOT xuống dưới 35ms (mục tiêu lý tưởng là < 30ms).
  2. Đồng thời duy trì TTFT thấp để nâng tỷ lệ `passed_slo` lên > 100/120 requests.
