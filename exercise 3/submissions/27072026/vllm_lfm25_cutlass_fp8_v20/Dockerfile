FROM ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14

# Copy patch directory
COPY patch /patch

# Ghi đè sitecustomize.py
COPY sitecustomize.py /patch/sitecustomize.py

# Ghi đè python3_hijack
COPY python3_hijack /usr/bin/python3
RUN sed -i 's/\r$//' /usr/bin/python3 && chmod +x /usr/bin/python3
