FROM ptquanh/sandbox-runtime:vllm-lfm25-cutlass-fp8-v20.0

# Sao chép tokenizer patch vào trong container
COPY tokenizer_patch.py /usr/local/lib/python3.12/dist-packages/vllm_tokenizer_patch.py
COPY python3_hijack /usr/bin/python3
RUN chmod +x /usr/bin/python3

# Inject patch thẳng vào file api_server.py của vLLM trên ổ cứng
RUN sed -i '1s/^/import vllm_tokenizer_patch\n/' /usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py

# Optional: Disable __pycache__ để tiết kiệm space nếu cần (mặc định đã disable ở v20.0)
ENV PYTHONDONTWRITEBYTECODE=1
