# Kết quả Benchmark - 09:49 28/07/2026 (Slot 01 - v21.0 INT4 Online Quantization + Marlin/Triton GEMM)

- **Cấu hình**: Image `vllm-lfm25:v21-int4-marlin` (vLLM V1 Engine + sitecustomize F.linear mock hook).
- **Mục đích**: Chuyển đổi weights sang INT4 (symmetric, group=128) khi start container để ép TPOT xuống dưới 2ms (phá vỡ giới hạn băng thông HBM). Ưu tiên dùng `marlin_gemm` (Tensor Cores), dự phòng bằng custom Triton INT4 GEMM.

## Chỉ số đo được

**THẤT BẠI (FAIL - POD READY TIMEOUT / ENGINE CRASH)**

### Nguyên nhân lỗi (Root Cause):

```
RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
```

1. **Xung đột PyTorch Dynamo JIT**: Cấu hình truyền vào có `VLLM_COMPILATION_LEVEL=3` (sử dụng `torch.compile`). Khi khởi tạo Engine Core, vLLM kích hoạt quá trình compile graph. Trình dịch Dynamo của PyTorch cố gắng trace (dịch) các hàm mock của chúng ta trong `sitecustomize.py`, nhưng không thể xử lý được các Kernel `@triton.jit` và C++ ops (`vllm_ops.gptq_marlin_gemm`). Hậu quả là Dynamo JIT tung lỗi Internal RuntimeError làm văng toàn bộ tiến trình khởi tạo Engine Core của vLLM V1.
2. **Kiến trúc vLLM V1**: Trong kiến trúc V1, `ModelRunner` thông thường không được sử dụng. Cần phải thiết lập Eager Quantization Hook cho `GPUModelRunner` (vllm.v1.worker.gpu_model_runner) để tránh lượng tử hóa bị trễ nhịp và lọt vào bên trong tiến trình CUDA Graph capture.

### Hành động tiếp theo:

- Đã gỡ bỏ cờ `VLLM_COMPILATION_LEVEL=3` khỏi cấu hình.
- Đã nâng cấp `sitecustomize.py` (v21.1) bổ sung thuật toán chèn Eager Quantization Hook vào `GPUModelRunner`.
- Chuyển sang **Slot 02 (10:30)** để thử nghiệm lại cấu hình v21.1 đã vá lỗi.
