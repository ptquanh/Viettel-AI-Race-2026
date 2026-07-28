FROM vllm/vllm-openai:v0.22.1

# 1. Cài đặt các biến môi trường cấu hình tối ưu
ENV VLLM_WORKER_MULTIPROC_METHOD=spawn \
    VLLM_USE_TRITON_FLASH_INFER=1 \
    VLLM_CUDAGRAPH_NUM_OF_WARMUPS=10 \
    PYTHONPATH="/workspace"

# 2. Copy mã nguồn hijack vào container
WORKDIR /workspace
COPY . /workspace/

# 3. Kích hoạt tự động sitecustomize
ENV PYTHONPATH="/workspace:${PYTHONPATH}"
