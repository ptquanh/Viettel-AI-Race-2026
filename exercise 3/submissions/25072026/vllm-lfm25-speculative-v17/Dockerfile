FROM ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14

# Cài đặt huggingface_hub nếu chưa có
RUN pip install --no-cache-dir huggingface_hub

# Tải trước model Draft vào image với hf-token
RUN hf download LiquidAI/LFM2.5-350M-Instruct --local-dir /draft_model --token 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
