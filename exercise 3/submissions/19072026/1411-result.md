# BÁO CÁO THỬ NGHIỆM SLOT 9 (1411 - TIMEOUT ERROR)

## 1. Thông tin cấu hình

- **File nộp**: `1411-docker-compose.yml`
- **Image**: `ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v2`
- **Draft Model**: `LiquidAI/LFM2.5-350M-Instruct` (`Spec_Tokens=6`)
- **Thời gian nộp**: 14:11 (19/07/2026)

## 2. Kết quả chấm từ BTC Portal

- **Trạng thái**: `Chấm điểm thất bại` (Exited with code 2)
- **Lỗi chi tiết**:
  ```text
  spawn contestant container: wait for pod ready: timed out waiting for contestant pod to be ready: context deadline exceeded
  ```

## 3. Phân tích nguyên nhân & Giải pháp khắc phục

- **Nguyên nhân cốt lõi**:
  1. Pod contestant của BTC là môi trường **OFFLINE** (không có kết nối Internet). BTC chỉ mount sẵn mô hình chính tại `/model` (`LFM2.5-1.2B-Instruct`).
  2. Khi truyền `VLLM_SPECULATIVE_MODEL=LiquidAI/LFM2.5-350M-Instruct`, vLLM trong container cố gắng tải weights của mô hình draft 350M từ HuggingFace over Internet.
  3. Do không có Internet, vLLM bị treo/chờ kết nối mãi mãi cho đến khi Kubernetes pod bị timeout (`context deadline exceeded`).
- **Bài học & Giải pháp**:
  1. Trong môi trường grader offline của BTC, không thể dùng draft models dạng Hugging Face repo name nếu chưa được đóng gói sẵn weights trực tiếp vào Docker image.
  2. Phương pháp Speculative Decoding duy nhất 100% offline không cần weights external là **Prompt Lookup N-gram Speculative Decoding** (`VLLM_SPECULATIVE_MODEL=ngram`).
  3. Bỏ qua Draft Model 350M external và tiến hành nộp bài cho các giả thuyết khả thi offline 100% tiếp theo (Compressed Tensors, Marlin INT4, MaxLen 16K/8K, N-gram).
