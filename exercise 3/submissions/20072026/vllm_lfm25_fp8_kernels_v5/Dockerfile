FROM vllm/vllm-openai:v0.22.1

# Prepare hijack wrapper v2 (transparent $@ forwarding + Warmup JIT)
RUN mv /usr/bin/python3 /usr/bin/python3_real
COPY python3_hijack /usr/bin/python3
RUN sed -i 's/\r$//' /usr/bin/python3 && chmod +x /usr/bin/python3

# Inject Custom Kernel / Monkey Patch / Deep Warmup
RUN mkdir -p /patch
COPY sitecustomize.py /patch/sitecustomize.py
RUN sed -i 's/\r$//' /patch/sitecustomize.py
COPY deep_warmup.py /patch/deep_warmup.py
RUN sed -i 's/\r$//' /patch/deep_warmup.py
COPY fused_lfm_kernel.py /patch/fused_lfm_kernel.py
RUN sed -i 's/\r$//' /patch/fused_lfm_kernel.py
