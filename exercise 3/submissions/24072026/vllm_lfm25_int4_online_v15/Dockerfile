FROM ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14

# Cài torchao cho Online INT4 Quantization
RUN pip3 install --no-cache-dir torchao>=0.5.0

# Chèn Draft Model directory
RUN mkdir -p /draft_model
COPY draft_model /draft_model

# Copy patch directory
RUN mkdir -p /patch
COPY sitecustomize.py /patch/sitecustomize.py
COPY patch/fused_short_conv.py /patch/fused_short_conv.py

# Copy hijack script
COPY python3_hijack /usr/bin/python3

# Fix quyền và định dạng
RUN sed -i 's/\r$//' /usr/bin/python3 && chmod +x /usr/bin/python3
