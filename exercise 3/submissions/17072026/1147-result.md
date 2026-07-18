# Kết quả Benchmark - 11:47 17/07/2026 (STT 21 - Slot 6 - Seqs=32 + FP8 Base + OMP=2 + swap=0)

- **Trạng thái**: **Chấm điểm thất bại (FAILED)**

## Nguyên nhân lỗi
* Grader log: `spawn contestant container: wait for pod ready: contestant pod failed: container "inference" exited 2 (Error): ashinfer_trtllm,humming,marlin,triton,triton_unfused}]
                     [--linear-backend {aiter,auto,conch,cutlass,deep_gemm,emulation,exllama,fbgemm,flashinfer_cudnn,flashinfer_cutlass,flashinfer_trtllm,machete,marlin,torch,triton}]
                     [--speculative-config SPECULATIVE_CONFIG]
                     [--spec-method {custom_class,deepseek_mtp,dflash,draft_model,eagle,eagle3,ernie_mtp,exaone4_5_mtp,exaone_moe_mtp,extract_hidden_states,gemma4_mtp,glm4_moe_lite_mtp,gl
... [truncated] ...
el_tag]
api_server.py: error: unrecognized arguments: --swap-space=0

--- last container logs ---
                     [--kv-transfer-config KV_TRANSFER_CONFIG]
                     [--kv-events-config KV_EVENTS_CONFIG]
                     [--ec-transfer-config EC_TRANSFER_CONFIG]
                     [--compilation-config COMPILATION_CONFIG]
                     [--attention-config ATTENTION_CONFIG]
                     [--reasoning-config REASONING_CONFIG]
                     [--kernel-config KERNEL_CONFIG]
                     [--additional-config ADDITIONAL_CONFIG]
                     [--structured-outputs-config STRUCTURED_OUTPUTS_CONFIG]
                     [--profiler-config PROFILER_CONFIG]
                     [--optimization-level OPTIMIZATION_LEVEL]
                     [--performance-mode {balanced,interactivity,throughput}]
                     [--weight-transfer-config WEIGHT_TRANSFER_CONFIG]
                     [--disable-log-stats] [--aggregate-engine-logging]
                     [--fail-on-environ-validation | --no-fail-on-environ-validation]
                     [--shutdown-timeout SHUTDOWN_TIMEOUT]
                     [--gdn-prefill-backend {flashinfer,triton,cutedsl}]
                     [--enable-log-requests | --no-enable-log-requests]
                     [model_tag]
api_server.py: error: unrecognized arguments: --swap-space=0`
