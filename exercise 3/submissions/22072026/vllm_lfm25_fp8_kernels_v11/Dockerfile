FROM vllm/vllm-openai:latest

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Đổi tên python3 gốc
RUN mv /usr/bin/python3 /usr/bin/python3_real

# Copy patch directory
RUN mkdir -p /patch
COPY sitecustomize.py /patch/sitecustomize.py

# Copy script hijack mới nhất (Image v11 vLLM Modern Engine + Native Warmup + Speculative Edition)
COPY python3_hijack /usr/bin/python3

# Fix quyền và định dạng
RUN sed -i 's/\r$//' /usr/bin/python3 && chmod +x /usr/bin/python3
