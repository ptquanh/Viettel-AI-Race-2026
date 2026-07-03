# Kế thừa 100% môi trường gốc của BTC
FROM vllm/vllm-openai:v0.22.1

# Tạo thư mục và copy weights của Qwen3.5-2B vào
# Thư mục ./Qwen3.5-2B-BTC phải chứa chính xác các file từ mã Hash của BTC
# Cấm đổi tên thư mục đích (/model/) theo luật của docker-compose
COPY ./Qwen3.5-2B-BTC /model/