Chấm điểm thất bại

out of memory: container "inference" exceeded its 8Gi memory limit and was OOM-killed (exit 137). This is the container's host RAM limit, not GPU memory — reduce CPU-side memory (runtime kernel JIT/compile parallelism, tokenizer/dataloader workers, CUDA graph capture) or pre-build kernels into the image so nothing compiles at inference time
--- container logs ---
(APIServer pid=1) INFO 07-30 07:06:32 [api_utils.py:345] 
(APIServer pid=1) INFO 07-30 07:06:32 [api_utils.py:345]        █     █     █▄   ▄█
(APIServer pid=1) INFO 07-30 07:06:32 [api_utils.py:345]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.26.0
(APIServer pid=1) INFO 07-30 07:06:32 [api_utils.py:345]   █▄█▀ █     █     █     █  model   /model
(APIServer pid=1) INFO 07-30 07:06:32 [api_utils.py:345]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
(APIServer pid=1) INFO 07-30 07:06:32 [api_utils.py:345] 
(APIServer pid=1) INFO 07-30 07:06:33 [api_utils.py:273] non-default args: {'host': '0.0.0.0', 'disable_uvicorn_access_log': True, 'model': '/model', 'trust_remote_code': True, 'dtype': 'float16', 'max_model_len': 32768, 'quantization': 'online_int4', 'disable_cascade_attn': False, 'served_model_name': ['LFM2.5-1.2B-Instruct'], 'attention_backend': 'FLASHINFER', 'block_size': 16, 'gpu_memory_utilization': 0.95, 'kv_cache_dtype': 'fp8', 'enable_prefix_caching': True, 'prefix_caching_hash_algo': 'xxhash', 'mamba_cache_dtype': 'float16', 'mamba_block_size': 16, 'prefix_match_unit': 16, 'mamba_cache_mode': 'align', 'max_num_batched_tokens': 1024, 'max_num_seqs': 256, 'enable_chunked_prefill': True, 'async_scheduling': True, 'optimization_level': '3', 'performance_mode': 'interactivity', 'disable_log_stats': True}
(APIServer pid=1) INFO 07-30 07:06:49 [model.py:623] Resolved architecture: Lfm2ForCausalLM
(APIServer pid=1) WARNING 07-30 07:06:49 [model.py:2123] Casting torch.bfloat16 to torch.float16.
(APIServer pid=1) INFO 07-30 07:06:49 [model.py:1788] Using max model len 32768
(APIServer pid=1) INFO 07-30 07:06:49 [cache.py:285] Using fp8 data type to store kv cache. It reduces the GPU memory footprint and boosts the performance. Meanwhile, it may cause accuracy drop without a proper scaling factor
(APIServer pid=1) INFO 07-30 07:06:49 [scheduler.py:252] Chunked prefill is enabled with max_num_batched_tokens=1024.
(APIServer pid=1) INFO 07-30 07:06:49 [vllm.py:943] Performance mode set to 'interactivity'.
(APIServer pid=1) INFO 07-30 07:06:49 [config.py:583] Warning: Prefix caching in Mamba cache 'align' mode is currently enabled. Its support for Mamba layers is experimental. Please report any issues you may observe.
(APIServer pid=1) INFO 07-30 07:06:49 [vllm.py:1109] Asynchronous scheduling is enabled.
(APIServer pid=1) INFO 07-30 07:06:49 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native'])
(APIServer pid=1) [fastokens] patch_transformers: successfully patched transformers v5.14.1
(EngineCore pid=79) INFO 07-30 07:07:02 [core.py:116] Initializing a V1 LLM engine (v0.26.0) with config: model='/model', speculative_config=None, tokenizer='/model', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.float16, max_seq_len=32768, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=online_int4, quantization_config=None, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=fp8, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False, jit_monitor_mode='warn', jit_monitor_verbose=False), seed=0, served_model_name=LFM2.5-1.2B-Instruct, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none'], 'ir_enable_torch_wrap': True, 'splitting_ops': ['vllm::unified_attention_with_output', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::qwen_gdn_attention_core', 'vllm::gdn_attention_core_xpu', 'vllm::olmo_hybrid_gdn_full_forward', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer', 'vllm::deepseek_v4_attention', 'vllm::hpc_rope_norm_forward', 'vllm::unified_kv_cache_update', 'vllm::unified_mla_kv_cache_update'], 'compile_mm_encoder': False, 'cudagraph_mm_encoder': False, 'encoder_cudagraph_token_budgets': [], 'encoder_cudagraph_max_vision_items_per_batch': 0, 'encoder_cudagraph_max_frames_per_batch': None, 'compile_sizes': [], 'compile_ranges_endpoints': [1024], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'size_asserts': False, 'alignment_asserts': False, 'scalar_asserts': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496, 512], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False, 'enable_qk_norm_rope_fusion': False, 'fuse_rope_kvcache_cat_mla': False, 'fuse_act_padding': False, 'fuse_qk_norm_rope_kvcache': False}, 'max_cudagraph_capture_size': 512, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': False, 'static_all_moe_layers': []}, kernel_config=KernelConfig(ir_op_priority=IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native']), enable_flashinfer_autotune=True, enable_cutedsl_warmup=True, enable_bf16x3_router_gemm=False, moe_backend='auto', linear_backend='auto')
(EngineCore pid=79) INFO 07-30 07:07:03 [parallel_state.py:1615] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://10.0.0.226:53689 backend=nccl
(EngineCore pid=79) INFO 07-30 07:07:03 [parallel_state.py:1946] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
(EngineCore pid=79) INFO 07-30 07:07:03 [topk_topp_sampler.py:55] Using FlashInfer for top-p & top-k sampling.
(EngineCore pid=79) INFO 07-30 07:07:03 [gpu_model_runner.py:5250] Starting to load model /model...
(EngineCore pid=79) INFO 07-30 07:07:04 [cuda.py:422] Using AttentionBackendEnum.FLASHINFER backend.
(EngineCore pid=79) INFO 07-30 07:07:04 [weight_utils.py:869] Filesystem type for checkpoints: EXT4. Checkpoint size: 2.18 GiB. Available RAM: 210.20 GiB.
(EngineCore pid=79) INFO 07-30 07:07:04 [weight_utils.py:892] Auto-prefetch is disabled because the filesystem (EXT4) is not a recognized network FS (NFS/Lustre). If you want to force prefetching, start vLLM with --safetensors-load-strategy=prefetch.
(EngineCore pid=79) 
Loading safetensors checkpoint shards:   0% Completed | 0/1 [00:00<?, ?it/s]
(EngineCore pid=79) 
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:04<00:00,  4.00s/it]
(EngineCore pid=79) 
Loading safetensors checkpoint shards: 100% Completed | 1/1 [00:04<00:00,  4.00s/it]
(EngineCore pid=79) 
(EngineCore pid=79) INFO 07-30 07:07:08 [default_loader.py:430] Loading weights took 4.13 seconds
(EngineCore pid=79) INFO 07-30 07:07:11 [online_int4.py:632] Online INT4 lm_head uses Humming W4A16
(EngineCore pid=79) INFO 07-30 07:07:11 [gpu_model_runner.py:5347] Model loading took 0.88 GiB memory and 7.012805 seconds
(EngineCore pid=79) INFO 07-30 07:07:11 [interface.py:929] Padding mamba page size by 100.00% to ensure that mamba page size and attention page size are exactly equal.
(EngineCore pid=79) INFO 07-30 07:07:16 [backends.py:1094] Using cache directory: /root/.cache/vllm/torch_compile_cache/0b4005cc46/rank_0_0/backbone for vLLM's torch.compile
(EngineCore pid=79) INFO 07-30 07:07:16 [backends.py:1155] Dynamo bytecode transform time: 4.75 s
(EngineCore pid=79) INFO 07-30 07:07:19 [backends.py:378] Cache the graph of compile range (1, 1024) for later use
(EngineCore pid=79) INFO 07-30 07:07:27 [backends.py:393] Compiling a graph for compile range (1, 1024) takes 10.88 s
(EngineCore pid=79) INFO 07-30 07:07:29 [decorators.py:708] saved AOT compiled function to /root/.cache/vllm/torch_compile_cache/torch_aot_compile/246d253779277f957d6a2673435c81abe31cb5d6d154b82e0e53192b9ae9bd2e/rank_0_0/model
(EngineCore pid=79) INFO 07-30 07:07:29 [monitor.py:53] torch.compile took 17.57 s in total
(EngineCore pid=79) INFO 07-30 07:10:19 [monitor.py:81] Initial profiling/warmup run took 169.73 s
(EngineCore pid=79) WARNING 07-30 07:10:58 [kv_cache_utils.py:1237] Add 2 padding layers, may waste at most 20.00% KV cache memory
(EngineCore pid=79) INFO 07-30 07:10:58 [flashinfer.py:822] FlashInfer resolved query dtypes: prefill=torch.float8_e4m3fn, decode=torch.float16, decode_backend=xqa, kv_cache_dtype=torch.float8_e4m3fn, arch=sm90
(EngineCore pid=79) INFO 07-30 07:10:58 [gpu_model_runner.py:6612] Profiling CUDA graph memory: PIECEWISE=76 (largest=512), FULL=60 (largest=256)
(EngineCore pid=79) INFO 07-30 07:11:00 [gpu_model_runner.py:6737] Estimated CUDA graph memory: 0.58 GiB total
(EngineCore pid=79) INFO 07-30 07:11:00 [gpu_worker.py:560] Available KV cache memory: 13.33 GiB
(EngineCore pid=79) INFO 07-30 07:11:00 [gpu_worker.py:575] CUDA graph memory profiling is enabled (default since v0.21.0). The current --gpu-memory-utilization=0.9500 is equivalent to --gpu-memory-utilization=0.9139 without CUDA graph memory profiling. To maintain the same effective KV cache size as before, increase --gpu-memory-utilization to 0.9861. To disable, set VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=0.
(EngineCore pid=79) WARNING 07-30 07:11:00 [kv_cache_utils.py:1237] Add 2 padding layers, may waste at most 20.00% KV cache memory
(EngineCore pid=79) INFO 07-30 07:11:00 [kv_cache_utils.py:2177] GPU KV cache size: 2,324,244 tokens
(EngineCore pid=79) INFO 07-30 07:11:00 [kv_cache_utils.py:2178] Maximum concurrency for 32,768 tokens per request: 70.93x
(EngineCore pid=79) INFO 07-30 07:11:01 [kernel_warmup.py:227] Using FlashInfer autotune cache file: /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/90a/01abe2e90a48184c4b113e6fc81ef39629d7f3fcbd45b97879e84836de93371f/autotune_configs.json
(EngineCore pid=79) 2026-07-30 07:11:01,504 - INFO - autotuner.py:651 - flashinfer.jit: [Autotuner]: Autotuning process starts ...
(EngineCore pid=79) 2026-07-30 07:11:01,515 - INFO - autotuner.py:674 - flashinfer.jit: [Autotuner]: Autotuning process ends
(EngineCore pid=79) WARNING 07-30 07:11:01 [kernel_warmup.py:258] No FlashInfer autotune cache entries found.Falling back to default tactics.
(EngineCore pid=79) INFO 07-30 07:11:01 [kernel_warmup.py:65] Warming up ll_bf16 router GEMM kernels.
(EngineCore pid=79) INFO 07-30 07:11:15 [cutedsl_warmup.py:101] Skipping CuTeDSL warmup because no compile units were requested.
(EngineCore pid=79) INFO 07-30 07:11:15 [gpu_model_runner.py:6798] Rank 0: Torch profiler disabled for CUDA graph capture
(EngineCore pid=79) 
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):   0%|          | 0/76 [00:00<?, ?it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):   4%|▍         | 3/76 [00:00<00:02, 27.08it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):   8%|▊         | 6/76 [00:00<00:02, 27.93it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  12%|█▏        | 9/76 [00:00<00:02, 28.42it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  17%|█▋        | 13/76 [00:00<00:02, 29.25it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  22%|██▏       | 17/76 [00:00<00:01, 29.68it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  26%|██▋       | 20/76 [00:00<00:01, 29.27it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  30%|███       | 23/76 [00:00<00:01, 28.98it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  34%|███▍      | 26/76 [00:00<00:01, 28.76it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  38%|███▊      | 29/76 [00:01<00:01, 28.80it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  42%|████▏     | 32/76 [00:01<00:01, 29.03it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  46%|████▌     | 35/76 [00:01<00:01, 29.18it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  50%|█████     | 38/76 [00:01<00:01, 29.23it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  55%|█████▌    | 42/76 [00:01<00:01, 31.27it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  61%|██████    | 46/76 [00:01<00:00, 32.49it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  66%|██████▌   | 50/76 [00:01<00:00, 33.63it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  71%|███████   | 54/76 [00:01<00:00, 34.45it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  76%|███████▋  | 58/76 [00:01<00:00, 34.81it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  82%|████████▏ | 62/76 [00:01<00:00, 35.25it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  87%|████████▋ | 66/76 [00:02<00:00, 35.46it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  92%|█████████▏| 70/76 [00:02<00:00, 35.42it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  97%|█████████▋| 74/76 [00:02<00:00, 35.51it/s]
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE): 100%|██████████| 76/76 [00:02<00:00, 32.04it/s]
(EngineCore pid=79) 
Capturing CUDA graphs (decode, FULL):   0%|          | 0/60 [00:00<?, ?it/s]
Capturing CUDA graphs (decode, FULL):   7%|▋         | 4/60 [00:00<00:01, 33.87it/s]
Capturing CUDA graphs (decode, FULL):  13%|█▎        | 8/60 [00:00<00:01, 35.27it/s]
Capturing CUDA graphs (decode, FULL):  20%|██        | 12/60 [00:00<00:01, 35.75it/s]
Capturing CUDA graphs (decode, FULL):  27%|██▋       | 16/60 [00:00<00:01, 35.85it/s]
Capturing CUDA graphs (decode, FULL):  33%|███▎      | 20/60 [00:00<00:01, 35.97it/s]
Capturing CUDA graphs (decode, FULL):  40%|████      | 24/60 [00:00<00:00, 36.00it/s]
Capturing CUDA graphs (decode, FULL):  47%|████▋     | 28/60 [00:00<00:00, 36.32it/s]
Capturing CUDA graphs (decode, FULL):  53%|█████▎    | 32/60 [00:00<00:00, 36.71it/s]
Capturing CUDA graphs (decode, FULL):  60%|██████    | 36/60 [00:00<00:00, 37.08it/s]
Capturing CUDA graphs (decode, FULL):  67%|██████▋   | 40/60 [00:01<00:00, 37.34it/s]
Capturing CUDA graphs (decode, FULL):  73%|███████▎  | 44/60 [00:01<00:00, 37.41it/s]
Capturing CUDA graphs (decode, FULL):  80%|████████  | 48/60 [00:01<00:00, 37.61it/s]
Capturing CUDA graphs (decode, FULL):  87%|████████▋ | 52/60 [00:01<00:00, 37.78it/s]
Capturing CUDA graphs (decode, FULL):  93%|█████████▎| 56/60 [00:01<00:00, 37.94it/s]
Capturing CUDA graphs (decode, FULL): 100%|██████████| 60/60 [00:01<00:00, 37.93it/s]
Capturing CUDA graphs (decode, FULL): 100%|██████████| 60/60 [00:01<00:00, 36.97it/s]
(EngineCore pid=79) INFO 07-30 07:11:20 [gpu_model_runner.py:6844] Graph capturing finished in 5 secs, took 0.24 GiB
(EngineCore pid=79) INFO 07-30 07:11:20 [gpu_worker.py:793] CUDA graph pool memory: 0.24 GiB (actual), 0.58 GiB (estimated), difference: 0.34 GiB (142.2%).
(EngineCore pid=79) INFO 07-30 07:11:20 [gpu_worker.py:857] Free memory on device (15.89/16.0 GiB) on startup. Desired GPU memory utilization is (0.95, 15.2 GiB). Actual usage is 0.88 GiB for weight, 0.26 GiB for peak activation, 0.16 GiB for non-torch memory, and 0.24 GiB for CUDAGraph memory. Replace gpu_memory_utilization config with `--kv-cache-memory=14514713805` (13.52 GiB) to fit into requested memory, or `--kv-cache-memory=15258363904` (14.21 GiB) to fully utilize gpu memory. Current kv cache memory in use is 13.33 GiB.
(EngineCore pid=79) INFO 07-30 07:11:21 [jit_monitor.py:79] Kernel JIT monitor activated; monitored JIT compilations during inference will use mode=warn.
(EngineCore pid=79) INFO 07-30 07:11:22 [core.py:340] init engine (profile, create kv cache, warmup model) took 250.65 s (compilation: 17.57 s)
(EngineCore pid=79) [fastokens] patch_transformers: successfully patched transformers v5.14.1
(EngineCore pid=79) INFO 07-30 07:11:23 [vllm.py:943] Performance mode set to 'interactivity'.
(EngineCore pid=79) INFO 07-30 07:11:23 [vllm.py:1109] Asynchronous scheduling is enabled.
(EngineCore pid=79) INFO 07-30 07:11:23 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native'])
(APIServer pid=1) INFO 07-30 07:11:23 [api_server.py:673] Supported tasks: ['generate']
(APIServer pid=1) INFO 07-30 07:11:24 [hf.py:540] Detected the chat template content format to be 'string'. You can set `--chat-template-content-format` to override this.
(APIServer pid=1) INFO 07-30 07:11:24 [api_server.py:677] Starting vLLM server on http://0.0.0.0:8000
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:37] Available routes are:
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /openapi.json, Methods: GET, HEAD
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /docs, Methods: GET, HEAD
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /docs/oauth2-redirect, Methods: GET, HEAD
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /redoc, Methods: GET, HEAD
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /load, Methods: GET
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /version, Methods: GET
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /health, Methods: GET
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /metrics, Methods: GET
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /tokenize, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /detokenize, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/models, Methods: GET
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /ping, Methods: GET
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /ping, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /invocations, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/chat/completions, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/chat/completions/batch, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/responses, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/responses/{response_id}, Methods: GET
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/responses/{response_id}/cancel, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/completions, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/messages, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/messages/count_tokens, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /generative_scoring, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /scale_elastic_ep, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /is_scaling_elastic_ep, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/chat/completions/render, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/completions/render, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/chat/completions/derender, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /v1/completions/derender, Methods: POST
(APIServer pid=1) INFO 07-30 07:11:24 [launcher.py:46] Route: /inference/v1/generate, Methods: POST
(APIServer pid=1) INFO:     Started server process [1]
(APIServer pid=1) INFO:     Waiting for application startup.
(APIServer pid=1) INFO:     Application startup complete.
(EngineCore pid=79) WARNING 07-30 07:11:34 [jit_monitor.py:135] Triton kernel JIT compilation during inference: _zero_kv_blocks_kernel. This causes a latency spike; consider extending warmup to cover this shape/config.
(EngineCore pid=79) WARNING 07-30 07:11:34 [jit_monitor.py:135] Triton kernel JIT compilation during inference: _copy_page_indices_kernel. This causes a latency spike; consider extending warmup to cover this shape/config.