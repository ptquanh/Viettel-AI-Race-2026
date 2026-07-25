FROM vllm/vllm-openai:latest

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Rename original python3
RUN mv /usr/bin/python3 /usr/bin/python3_real

# Copy patch directory with fused kernels
RUN mkdir -p /patch
COPY sitecustomize.py /patch/sitecustomize.py
COPY patch/fused_kernels.py /patch/fused_kernels.py

# Copy hijack script
COPY python3_hijack /usr/bin/python3

# Fix permissions and line endings
RUN sed -i 's/\r$//' /usr/bin/python3 && chmod +x /usr/bin/python3
