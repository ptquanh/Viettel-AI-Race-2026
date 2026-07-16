# Phân tích Workload Trace & Công thức Điểm (LFM2.5-1.2B-Instruct)

Tài liệu này lưu trữ các phân tích về cấu trúc dữ liệu trace benchmark mới (`trace_grading_public.jsonl`) và suy diễn công thức tính điểm ERS mới của Ban tổ chức.

---

## 1. Phân tích Trace Data (Workload Structure)

### Cấu trúc Workload (dựa trên trace_grading_public.jsonl)

| Chỉ số                              | Giá trị                                                            |
| :---------------------------------- | :----------------------------------------------------------------- |
| **Tổng số lượt (turns/requests)**   | 420                                                                |
| **Số lượt khởi động (Warm-up)**     | 90 (15 hội thoại primer x 6 turns - không tính điểm)               |
| **Số lượt chấm điểm**               | 330 (55 hội thoại x 6 turns)                                       |
| **Cấu trúc hội thoại**              | **70 conversation chains x 6 turns**                               |
| **Arrival pattern**                 | Phân phối Poisson (khoảng thời gian arrival ~303 giây)             |
| **max_tokens**                      | 200 (tất cả output tối đa 200 tokens)                              |
| **Context input**                   | Tối đa ~4000 tokens (median ~3999 tokens)                          |
| **Tổng sequence length tối đa**     | ~4200 tokens (input + output)                                      |
| **User Thinking Time (`think_ms`)** | 3000 ms (Cố định 3s trước khi gửi turn tiếp theo trong cùng chain) |

### Chi tiết Conversation Chains & Turns

- File trace mô phỏng 70 hội thoại song song/xen kẽ:
  - `conv_id` từ 0 đến 14 (15 chains) có `in_warmup: true`, được dùng để pre-warmup hệ thống và không tính vào điểm ERS.
  - `conv_id` từ 15 đến 69 (55 chains) có `in_warmup: false`, được tính điểm trực tiếp.
- Mỗi chain có `turn_idx` từ 0 đến 5.
- Trường `timestamp_ms` chỉ khác 0 ở `turn_idx: 0` của mỗi chain để chỉ định thời điểm hội thoại đó bắt đầu xuất hiện (arrival time). Ở các turn sau, `timestamp_ms` bằng 0 và request kế tiếp sẽ được gửi đi sau khi nhận được phản hồi của turn trước đó cộng thêm thời gian nghĩ của User `think_ms: 3000`.

---

## 2. Phân tích Công thức Điểm ERS & Ràng buộc Latency mới

### Công thức ERS

$$ERS = \frac{1}{N} \sum_{i=1}^{N} S_{request, i}$$
Với $N = 330$ requests được chấm điểm.

$$S_{request} = 0.5 \cdot s_{ttft} + 0.5 \cdot s_{tpot}$$

$$s_{ttft} = \left[ \text{clamp}\left( \frac{400 - TTFT}{400 - 10}, 0, 1 \right) \right]^2 = \left[ \text{clamp}\left( \frac{400 - TTFT}{390}, 0, 1 \right) \right]^2$$

$$s_{tpot} = \left[ \text{clamp}\left( \frac{10 - TPOT_{mean}}{10 - 1}, 0, 1 \right) \right]^2 = \left[ \text{clamp}\left( \frac{10 - TPOT_{mean}}{9}, 0, 1 \right) \right]^2$$

### Biên Latency mới cho LFM2.5

Do mô hình **LFM2.5-1.2B-Instruct** thuộc lớp Liquid Foundation Model (có độ phức tạp hằng số đối với context memory/KV-like state), tốc độ sinh (generation speed) của nó nhanh hơn các mô hình Transformer rất nhiều. Vì vậy, BTC đã siết chặt giới hạn:

- **TTFT**:
  - **Floor ($F_{ttft}$): 10 ms** (Độ trễ $\le 10ms$ sẽ nhận điểm tối đa 1.0).
  - **Ceiling ($C_{ttft}$): 400 ms** (Độ trễ $\ge 400ms$ sẽ nhận 0 điểm).
- **TPOT**:
  - **Floor ($F_{tpot}$): 1 ms** (Độ trễ $\le 1ms$ sẽ nhận điểm tối đa 1.0).
  - **Ceiling ($C_{tpot}$): 10 ms** (Độ trễ $\ge 10ms$ sẽ nhận 0 điểm).

### Chiến lược bứt phá ERS cho LFM

1. **Ép TPOT $\le 10ms$**: Bất kỳ request nào có TPOT $\ge 10ms$ sẽ nhận điểm TPOT bằng 0. Để ăn điểm ERS cao, TPOT Median buộc phải kéo xuống dưới 10ms, lý tưởng nhất là $\le 5ms$ (tiến gần 1ms).
2. **Kéo TTFT $\le 400ms$**: TTFT phải nhỏ hơn 400ms để bắt đầu nhận điểm.
3. **Mô hình Recurrent/SSM**:
   - LFM không sử dụng ma trận Attention chuẩn của Transformer, mà nén context thành một trạng thái recurrent cố định. Do đó, chi phí prefill và decode không tăng tuyến tính theo context length dài (4k tokens).
   - vLLM hỗ trợ các kernel tính toán SSM cực nhanh. Chúng ta cần tìm hiểu xem vLLM lượng tử hóa mô hình này như thế nào và cách tối ưu hóa số lượng luồng xử lý (CPU Threads, GPU memory) để giữ cho TTFT < 400ms và TPOT < 10ms dưới traffic Poisson gồm 70 hội thoại đồng thời.
