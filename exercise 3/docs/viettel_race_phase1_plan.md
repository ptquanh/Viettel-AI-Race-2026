# Viettel AI Race 2026 — Phase 1 Optimization Plan
## LLM Inference Optimization Challenge (Online Qualifier)
**Target:** Qwen/Qwen3.5-2B Dense Transformer (BF16)  
**Hardware:** MiG H200 @ 18 GB VRAM / 3 CPU cores / 8 GB RAM  
**Deadline:** July 30, 2026  
**Today:** July 3, 2026 (27 engineering days + 1 submission day)

---

## Executive Verdict (Read This First)

For a **2B dense model on an H200-class GPU**, you are **not** memory-bound or FLOPS-bound. A BF16 checkpoint is only ~4 GB; with KV cache it still fits comfortably inside the 18 GB MiG slice. The real enemy is **framework and CPU overhead**: only 3 CPU cores must drive a Python inference server, the scheduler, tokenizers, HTTP I/O, and CUDA launches.

**Highest-ROI strategy:**
- Use **vLLM** as the engine (best balance of speed, features, and Docker stability for a backend engineer).
- Start from a **BF16 baseline**. Test **FP8 (W8A8 or weight-only)** because H200 has native FP8 Tensor Cores and the accuracy risk on a 2B model is usually < 1–2 % on GPQA.
- Avoid INT4/AWQ/GPTQ unless BF16/FP8 miss the latency floors — the accuracy gate is wide (≥ 30 %), but 2B models are fragile and a 10-point drop is easy to hit with aggressive 4-bit schemes.
- Avoid custom CUDA kernels and speculative decoding unless the baseline is far from the floors; they add complexity and CPU overhead.
- Optimize the **serving runtime** (CUDA graphs, chunked prefill, prefix caching, CPU thread limits, small Docker image) more than the model math.

---

## 1. Architecture & Stack Proposal

### 1.1 Inference Engine: vLLM

| Option | Verdict | Why |
|--------|---------|-----|
| **vLLM** | **Primary** | Mature PagedAttention, FP8/INT8 support, prefix caching, chunked prefill, multi-step scheduling, CUDA graphs, OpenAI-compatible API, easy Dockerization. |
| SGLang | Backup | Can be faster on small models, but less stable; only if vLLM cannot hit floors after tuning. |
| TensorRT-LLM | Avoid | Fastest theoretical throughput, but engine building and Docker packaging are high-risk for a 27-day window without CUDA expertise. |
| llama.cpp | Avoid | Optimized for CPU/Apple, not for a single H200 MiG slice. |

### 1.2 Quantization Strategy

| Method | Expected Accuracy Drop on GPQA | Expected Latency Impact | Recommendation |
|--------|-------------------------------|------------------------|----------------|
| **BF16 baseline** | 0 % (reference) | Fast | Always run first; likely sufficient for H200. |
| **FP8 W8A8 / weight-only** | 0–2 % | 1.2–1.5× faster decode on H200 | **Main experiment.** Native H200 support. |
| INT8 SmoothQuant | 0.5–2 % | 1.1–1.3× faster | Fallback if FP8 is unsupported or unstable. |
| INT4 (AWQ/GPTQ) | 3–10+ % | 1.3–1.6× faster | **Avoid** unless desperate; too risky for 2B. |

**Decision rule:**
- If BF16 already gives **TTFT < 100 ms and TPOT < 20 ms** for the full trace, skip quantization entirely to maximize accuracy margin.
- If not, try FP8 first. Keep it only if GPQA accuracy stays ≥ 35 % (giving you a 5-point buffer under the 30 % gate).

### 1.3 KV Cache Strategy

- **PagedAttention** (vLLM default): mandatory.
- **FP8 KV cache** (`--kv-cache-dtype fp8`): test it. On H200 it reduces memory bandwidth with negligible accuracy impact on short-context tasks like GPQA.
- **Prefix caching** (`--enable-prefix-caching`): enable only if the trace shows shared system prompts or repeated instruction prefixes. If every prompt is unique, it adds minor CPU overhead with no gain — disable it.
- **Chunked prefill** (`--enable-chunked-prefill`): usually helps mix prefill and decode phases; test with/without.

### 1.4 Serving / Runtime Optimizations

| Knob | Rationale | Suggested Starting Value |
|------|-----------|--------------------------|
| Continuous batching | vLLM default; tune scheduler params. | — |
| `--max-num-seqs` | Higher = better GPU utilization, but more CPU scheduling. | 64–128 |
| `--max-num-batched-tokens` | Limit prefill batch size to keep TTFT low. | 512–2048 |
| `--num-scheduler-steps` | Batches decode steps, reduces CPU overhead. | 5–10 (test) |
| CUDA graphs | Avoid CPU launch overhead; critical for TPOT floor. | Enable (do not use `--enforce-eager`) |
| `--gpu-memory-utilization` | 18 GB is plenty; leave headroom for graphs. | 0.90–0.93 |
| `--swap-space` | CPU RAM is only 8 GB; keep low. | 0–1 GB |
| CPU thread limits | Prevent CPU thrashing across only 3 cores. | `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, etc. |

### 1.5 Docker Image Strategy

- **Base:** `nvidia/cuda:12.4.1-runtime-ubuntu22.04` (matches CUDA 12.x constraint).
- **Install vLLM + transformers via pip.** Pin versions to avoid last-minute breakage.
- **Embed model weights in the image** (`/app/model/`) because the benchmark environment has no external network. Use safetensors to keep CPU load peaks low.
- **Multi-stage build:** compile nothing; just copy wheels/weights to a runtime stage.
- **Target image size:** ~6–8 GB uncompressed, ~3–4 GB compressed.
- **Do not** include Ray, monitoring agents, or unnecessary Python packages — they consume the 8 GB RAM and 3 cores.

### 1.6 Concrete vLLM Launch Command (Template)

```bash
# Inside container entrypoint
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VLLM_WORKER_MULTIPROC_METHOD=spawn

python -m vllm.entrypoints.openai.api_server \
  --model /app/model/Qwen3.5-2B \
  --dtype bfloat16 \
  --quantization fp8 \
  --kv-cache-dtype fp8 \
  --gpu-memory-utilization 0.93 \
  --max-model-len 32768 \
  --max-num-seqs 96 \
  --max-num-batched-tokens 1024 \
  --enable-chunked-prefill \
  --enable-prefix-caching \
  --num-scheduler-steps 8 \
  --swap-space 0 \
  --uvicorn-log-level warning \
  --port 8000
```

*Validate exact flag names against the vLLM version you pin. Do not cargo-cult this command; the grid search in Week 3 will change these values.*

### 1.7 `docker-compose.yml` Snippet

```yaml
version: '3.8'
services:
  vllm:
    image: your-dockerhub-user/viettel-race-qwen35-2b:latest
    runtime: nvidia
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - OMP_NUM_THREADS=1
      - MKL_NUM_THREADS=1
    deploy:
      resources:
        limits:
          cpus: '3.0'
          memory: 8G
    ports:
      - "8000:8000"
```

---

## 2. Local Benchmarking Protocol

You cannot fully reproduce an H200 MiG slice on a desktop GPU, but you can measure **relative improvements** locally and run **final validation** on a rented H200/H100.

### 2.1 Benchmarking Environment

1. **Primary bench machine:** rent an H200 or H100 instance (1× GPU is enough; you only need to test the 18 GB MiG behavior). Vietnamese clouds / Vultr / Lambda / CoreWeave are options.
2. **Local sanity machine:** any CUDA GPU with ≥ 24 GB VRAM (e.g., RTX 4090) for quick iteration, but do **not** trust absolute latency numbers from it.
3. **Resource constraints:** always run the container with `--cpus=3 --memory=8g` to match the qualifier environment.

### 2.2 Trace Replay Script Requirements

Write a Python script (`trace_benchmark.py`) that:

1. Reads `trace-round1.jsonl` and extracts per request:
   - prompt text
   - `max_tokens` / expected output length
   - arrival timestamp or inter-arrival delay
   - sampling parameters (temperature, top_p, etc.)
2. Opens an async SSE connection to `http://localhost:8000/v1/completions`.
3. Replays requests respecting inter-arrival times (asynchronous, not serialized).
4. Records:
   - `t_sent`: HTTP request sent time
   - `t_first`: first SSE chunk received time
   - `t_last`: final SSE chunk received time
   - `n_out`: number of generated tokens
5. Computes:
   - `TTFT = t_first - t_sent`
   - `TPOT = (t_last - t_first) / max(1, n_out - 1)`
   - Gamma-2 score for each metric
   - Per-request and average ERS

### 2.3 Scoring Formula to Reproduce

```python
import numpy as np

def gamma_score(actual, floor, ceiling, gamma=2.0):
    if actual <= floor:
        return 1.0
    if actual >= ceiling:
        return 0.0
    return ((ceiling - actual) / (ceiling - floor)) ** gamma

def request_score(ttft, tpot):
    s_ttft = gamma_score(ttft, floor=100, ceiling=1500)
    s_tpot = gamma_score(tpot, floor=20, ceiling=45)
    return 0.5 * s_ttft + 0.5 * s_tpot

effective_request_score = np.mean([request_score(r.ttft, r.tpot) for r in results])
```

**Critical:** gamma=2 is brutal. A TTFT of 800 ms scores only **0.25**; a TPOT of 32.5 ms also scores **0.25**. You need to be *near the floors*, not near the ceilings. Outliers matter quadratically.

### 2.4 Accuracy Evaluation

Use `lm-eval-harness` with the vLLM backend:

```bash
lm_eval \
  --model vllm \
  --model_args pretrained=/app/model/Qwen3.5-2B,dtype=bfloat16,gpu_memory_utilization=0.93 \
  --tasks gpqa_diamond \
  --batch_size auto \
  --num_fewshot 0
```

Run this **inside the same Docker container** so the score reflects your exact runtime/quantization.

**Accuracy gate:** baseline ≈ 40 %. You are safe if accuracy ≥ 30 %. Target ≥ 35 % to leave margin.

### 2.5 Profiling Checklist

| Tool | What it tells you |
|------|-------------------|
| Your trace replay script | ERS breakdown; which requests are slow. |
| vLLM metrics (`--prometheus-port`) | Batch size over time, KV cache hit rate, prefill/decode split. |
| `htop` / `py-spy` | CPU bottlenecks in scheduler or API server. |
| `nsys` / `nvidia-smi dmon` | GPU utilization, memory bandwidth, idle gaps. |

**Hypothesis to validate first:** If GPU utilization is low and TPOT is > 20 ms, the bottleneck is CPU launch/scheduler overhead, not FLOPS.

---

## 3. 27-Day Execution Plan

### Week 1 — Foundation & Baseline (July 3 – 9)

| Day | Date | Task | Success Criteria |
|-----|------|------|------------------|
| 1 | Jul 3 | Secure H200/H100 bench instance; install CUDA 12.x, Docker, nvidia-container-toolkit. | `docker run --gpus all nvidia/cuda:12.x-base nvidia-smi` works. |
| 2 | Jul 4 | Build base Dockerfile with pinned vLLM + transformers; push v0.1 tag. | Container starts and imports vLLM without errors. |
| 3 | Jul 5 | Download Qwen3.5-2B weights into the Docker build context; verify checksums and tokenizer. | Model loads in BF16 inside container. |
| 4 | Jul 6 | **BF16 baseline run:** single-request TTFT/TPOT on short/medium/long prompts. | Stable server, generation correct. |
| 5 | Jul 7 | **Full trace replay BF16:** measure ERS and identify slow-request percentiles. | You have a ranked list of bottleneck requests. |
| 6 | Jul 8 | **GPQA Diamond BF16 baseline:** establish accuracy (target ~40 %). | Baseline accuracy documented. |
| 7 | Jul 9 | Analyze trace: input/output length distribution, shared prefixes, arrival burstiness. Decide which optimizations are likely to matter. | Written trace profile + hypothesis list. |

### Week 2 — Quantization & Memory (July 10 – 16)

| Day | Date | Task | Success Criteria |
|-----|------|------|------------------|
| 8 | Jul 10 | Implement **FP8 W8A8** checkpoint (use vLLM / AutoFP8 or pre-converted HF checkpoint). | Server starts with `--quantization fp8`. |
| 9 | Jul 11 | Measure FP8 latency vs BF16 on full trace; measure GPQA accuracy. | Accuracy drop ≤ 2 % and latency improves → keep. |
| 10 | Jul 12 | Implement **FP8 KV cache** (`--kv-cache-dtype fp8`) with BF16 and FP8 weights. | No crashes, measure combined impact. |
| 11 | Jul 13 | If FP8 accuracy drop > 3 %, test **INT8 SmoothQuant** as fallback. | Choose best quant config by ERS × accuracy. |
| 12 | Jul 14 | Tune **CUDA graphs** and `--max-seq-len-to-capture`; compare with `--enforce-eager`. | Confirm graphs improve TPOT. |
| 13 | Jul 15 | Test **prefix caching** on/off; test **chunked prefill** on/off. | Keep only if ERS improves. |
| 14 | Jul 16 | **Week 2 review:** freeze quantization + KV-cache config. Document go/no-go for FP8 vs BF16. | Decision memo written. |

### Week 3 — Serving Optimization (July 17 – 23)

| Day | Date | Task | Success Criteria |
|-----|------|------|------------------|
| 15 | Jul 17 | Grid-search continuous batching params: `--max-num-seqs` (32, 64, 96, 128) and `--max-num-batched-tokens` (512, 1024, 2048). | Best combo selected by ERS. |
| 16 | Jul 18 | Tune `--num-scheduler-steps` (1, 4, 8, 12) for decode overhead reduction. | Higher scheduler steps improve TPOT without hurting TTFT. |
| 17 | Jul 19 | **CPU/RAM hardening:** set thread limits, remove unnecessary packages, test with `--cpus=3 --memory=8g`. | Container stable under load; no OOM. |
| 18 | Jul 20 | Optimize API server: uvicorn settings, keep-alive, HTTP client pooling in benchmark script. | Lower overhead on small/fast requests. |
| 19 | Jul 21 | Evaluate **speculative decoding / prompt-lookup decoding** only if floors are not yet met. | Go/no-go: keep only if clear ERS gain and stable. |
| 20 | Jul 22 | Profile with `py-spy` and `nsys`; identify final bottlenecks. | At least one concrete bottleneck documented. |
| 21 | Jul 23 | **Week 3 review:** freeze serving config; run full end-to-end trace + accuracy. | ERS target: ≥ 0.90; accuracy ≥ 35 %. |

### Week 4 — Finalization & Submission (July 24 – 30)

| Day | Date | Task | Success Criteria |
|-----|------|------|------------------|
| 22 | Jul 24 | Final accuracy sweep across the frozen config; run GPQA 3× to confirm variance. | Accuracy ≥ 30 %, ideally ≥ 35 %. |
| 23 | Jul 25 | Robustness tests: cold-start latency, concurrent burst, max-length prompts, empty/edge-case inputs. | No crashes; TTFT/TPOT remain near floors. |
| 24 | Jul 26 | Build final optimized Docker image; optimize layers; push `latest` and a dated tag to Docker Hub. | `docker pull` from a clean VM succeeds. |
| 25 | Jul 27 | Write final `docker-compose.yml`; validate full pull → up → benchmark cycle on a second machine. | Reproducible ERS within 2 % of dev bench. |
| 26 | Jul 28 | Final ERS run + accuracy run on the *exact* submission container. | Numbers meet targets. |
| 27 | Jul 29 | **Buffer day:** fix any last issue, re-push image, re-validate. | No open bugs. |
| 28 | Jul 30 | **Submit** the `docker-compose.yml` before deadline. | Confirmation received. |

---

## 4. Risk Register & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **CPU (3 cores) becomes bottleneck** | High | High | Limit CPU threads, enable CUDA graphs, tune scheduler steps, keep API server lean. |
| **8 GB RAM OOM during model load** | Medium | High | Use safetensors, pre-load to GPU, set `--swap-space 0`, strip Docker image. |
| **FP8 quantization drops accuracy > 10 pts** | Low-Medium | High | Keep BF16 fallback ready; validate GPQA before keeping FP8. |
| **vLLM version bug or model incompatibility** | Medium | High | Pin versions immediately; do not upgrade after Week 2. |
| **Large Docker image / slow pull** | Low | Medium | Multi-stage build; target < 8 GB uncompressed; test pull time. |
| **Trace has unique prompts → prefix caching useless** | Unknown | Low | Make prefix caching a toggle; decide after trace analysis. |
| **Speculative decoding adds CPU overhead** | Medium | Medium | Benchmark carefully; discard if no clear ERS win. |

---

## 5. Decision Framework

Use this at every milestone to avoid rabbit holes:

1. **Latency first:** Can BF16 hit TTFT < 100 ms and TPOT < 20 ms for the full trace? If yes, prefer BF16 for maximum accuracy headroom.
2. **Quantize only if needed:** Try FP8 next. Keep it only if (a) latency improves and (b) GPQA ≥ 35 %.
3. **No exotic techniques unless baseline fails:** Custom CUDA, speculative decoding, and INT4 are last resorts.
4. **Measure end-to-end ERS, not micro-benchmarks:** A 10 % speedup in decode means nothing if a few requests time out and score 0 under gamma=2.
5. **Container parity:** Every accuracy and ERS number that matters must come from the Docker container with the same resource limits as the qualifier.
