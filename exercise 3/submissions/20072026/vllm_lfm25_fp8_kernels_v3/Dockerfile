FROM vllm/vllm-openai:v0.22.1

# Prepare hijack wrapper v3 (transparent $@ forwarding + Offline Draft Model Speculative + Warmup JIT)
RUN mv /usr/bin/python3 /usr/bin/python3_real
COPY python3_hijack /usr/bin/python3
RUN sed -i 's/\r$//' /usr/bin/python3 && chmod +x /usr/bin/python3

# Inject Custom Kernel / Monkey Patch
RUN mkdir -p /patch
COPY sitecustomize.py /patch/sitecustomize.py
RUN sed -i 's/\r$//' /patch/sitecustomize.py

# Embed Draft Model for Speculative Decoding offline execution
RUN mkdir -p /draft_model
COPY draft_model /draft_model
