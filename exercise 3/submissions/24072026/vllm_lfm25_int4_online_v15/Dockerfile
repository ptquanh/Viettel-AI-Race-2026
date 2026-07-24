FROM ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14

# Install torchao for online INT4 quantization
RUN pip3 install --no-cache-dir torchao>=0.5.0

# Copy the v15 hijack script which includes the torchao hook
COPY python3_hijack_v15 /usr/local/bin/python3_hijack_v15
RUN mv /usr/local/bin/python3_hijack_v15 /usr/bin/python3

# Fix permissions
RUN sed -i 's/\r$//' /usr/bin/python3 && chmod +x /usr/bin/python3
