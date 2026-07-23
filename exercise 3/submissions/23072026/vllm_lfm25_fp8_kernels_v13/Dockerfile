FROM vllm/vllm-openai:v0.22.1

# Chuẩn bị hijack wrapper
RUN mv /usr/bin/python3 /usr/bin/python3_real
COPY python3_hijack /usr/bin/python3
RUN sed -i 's/\r$//' /usr/bin/python3 && chmod +x /usr/bin/python3

# Inject Profiler
RUN mkdir -p /patch
COPY sitecustomize.py /patch/sitecustomize.py
RUN sed -i 's/\r$//' /patch/sitecustomize.py
