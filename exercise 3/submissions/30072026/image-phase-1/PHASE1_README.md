# Hướng dẫn build Image Phase 1 (CUDA Graph Optimization)

Teammate cần tạo một `Dockerfile` mới base trên image kỷ lục `sha256:2f1c` và chạy script patch trước khi đóng image.

## Bước 1: Tạo `Dockerfile.phase1`

```dockerfile
# Sử dụng base image là kỷ lục Humming W4
FROM docker.io/taze05/lfm25-h200-ers@sha256:2f1c6a6e529508932a7db35994f605696fabb6500af3019a49dea9fa148553e9

# Copy script patch vào container
COPY phase1_patch.py /tmp/phase1_patch.py

# Chạy script để patch vLLM source code
RUN python3 /tmp/phase1_patch.py
```

## Bước 2: Build và push image

```bash
docker build -t taze05/lfm25-h200-ers:phase1 -f Dockerfile.phase1 .
docker push taze05/lfm25-h200-ers:phase1
```

## Bước 3: Cấu hình Docker Compose (Config P1)

Khi có image, chúng ta sẽ nộp bằng cấu hình này:

```yaml
services:
  model:
    image: docker.io/taze05/lfm25-h200-ers:phase1
    entrypoint: ["python3", "-m", "vllm.entrypoints.openai.api_server"]
    command:
      - --model=/model
      - --served-model-name=LFM2.5-1.2B-Instruct
      - --host=0.0.0.0
      - --port=8000
      # Giữ nguyên 32768 như kỷ lục 0851 (vì slot 1238 đã chứng minh 8192 không giúp ích mà còn gây nhiễu)
      - --max-model-len=32768
      - --tensor-parallel-size=1
      - --gpu-memory-utilization=0.95
      - --dtype=bfloat16
      - --quantization=online_int4
      - --kv-cache-dtype=fp8
      - --mamba-cache-dtype=bfloat16
      - --enable-prefix-caching
      - --mamba-cache-mode=align
      - --block-size=16
      - --mamba-block-size=16
      - --prefix-match-unit=16
      - --prefix-caching-hash-algo=xxhash
      - --no-disable-cascade-attn
      - --enable-chunked-prefill
      - --max-num-batched-tokens=1024
      - --max-num-seqs=256
      - --async-scheduling
      - --optimization-level=3
      - --performance-mode=interactivity
      - --disable-log-stats
      - --disable-uvicorn-access-log
    environment:
      BTS_ONLINE_HUMMING_BLOCKS: "1"
      VLLM_HUMMING_ONLINE_QUANT_CONFIG: '{"dtype":"int4","group_size":0}'
      BTS_ONLINE_INT4_BACKEND: marlin
      BTS_ONLINE_INT4_GROUP_SIZE: "128"
      BTS_ONLINE_INT4_LM_HEAD: "1"
      BTS_ONLINE_INT4_LM_HEAD_BACKEND: auto
      VLLM_USE_V2_MODEL_RUNNER: "1"
      VLLM_USE_FASTOKENS: "1"
      HF_HUB_OFFLINE: "1"
      TRANSFORMERS_OFFLINE: "1"
      HF_DATASETS_OFFLINE: "1"
      TOKENIZERS_PARALLELISM: "false"
      OMP_NUM_THREADS: "1"
      MKL_NUM_THREADS: "1"
      OPENBLAS_NUM_THREADS: "1"
    ports:
      - "8000:8000"
    shm_size: "2g"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```
