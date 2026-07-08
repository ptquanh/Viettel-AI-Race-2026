import os
import sys
import torch

# Define patched smooth_layers function to support hybrid layers
def patched_smooth_layers(layers,
                          fc2fcs,
                          norm2fcs,
                          a_scales,
                          group_size=-1,
                          device='cuda'):
    """Apply weight smoothing based on input scales, gracefully handling hybrid layers."""
    from lmdeploy.lite.quantization.awq import smooth_ln_fcs, smooth_fc_fcs

    for l_name, layer in layers.items():
        layer.to(device)
        submodule_names = [name for name, _ in layer.named_modules()]
        
        for ln_name, fc_names in norm2fcs.items():
            # Check if ln_name exists in this layer
            if ln_name not in submodule_names:
                continue
            
            # Filter fc_names that actually exist in this layer
            existing_fc_names = [n for n in fc_names if n in submodule_names]
            if not existing_fc_names:
                continue
                
            a_name = f'{l_name}.{existing_fc_names[0]}'
            
            ln = layer.get_submodule(ln_name)
            fcs = [layer.get_submodule(n) for n in existing_fc_names]
            smooth_ln_fcs(ln, fcs, a_scales[a_name], group_size)

        for f_name, fc_names in fc2fcs.items():
            # Check if f_name exists in this layer
            if f_name not in submodule_names:
                continue
                
            # Filter fc_names that actually exist in this layer
            existing_fc_names = [n for n in fc_names if n in submodule_names]
            if not existing_fc_names:
                continue
                
            a_name = f'{l_name}.{existing_fc_names[0]}'

            fc = layer.get_submodule(f_name)
            fcs = [layer.get_submodule(n) for n in existing_fc_names]
            smooth_fc_fcs(fc, fcs, a_scales[a_name], group_size)

        layer.to('cpu')
        torch.cuda.empty_cache()
        max_memory = torch.cuda.max_memory_allocated() / 1024 / 1024 / 1024
        print(f'{l_name} smooth weight done.'
              f' max gpu memory: {max_memory:.2f} GB')

# Define patched save_vl_model to clean up memory before saving/sharding (prevents OOM SIGKILL)
def patched_save_vl_model(vl_model, model_path, dst_path):
    import gc
    import shutil
    import os
    import os.path as osp

    print("🧹 Patched save: Cleaning memory and VRAM before sharding...")
    vl_model.cpu()
    gc.collect()
    torch.cuda.empty_cache()

    print("💾 Patched save: Saving model weights to disk (max 2GB shards)...")
    safe_serialization = type(vl_model).__name__ == 'MGMLlamaForCausalLM'
    vl_model.save_pretrained(dst_path,
                             max_shard_size='2GB',
                             safe_serialization=safe_serialization)
    
    # Run gc again to free memory of saved tensors
    gc.collect()

    candidate = [
        'preprocessor_config.json', 'processor_config.json', 'vit',
        'generation_config.json', 'added_tokens.json'
    ]
    for name in candidate:
        tmp_path = osp.join(model_path, name)
        if osp.exists(tmp_path):
            if osp.isfile(tmp_path):
                shutil.copy(tmp_path, osp.join(dst_path, name))
            elif osp.isdir(tmp_path):
                shutil.copytree(tmp_path, osp.join(dst_path, name))
    # AutoProcessor files
    allfiles = os.listdir(model_path)
    for file in allfiles:
        if not file.endswith('.py'):
            continue
        copy_src = osp.join(model_path, file)
        copy_dst = osp.join(dst_path, file)
        if not osp.exists(copy_dst):
            shutil.copyfile(copy_src, copy_dst)
    print("✅ Patched save: Model saved successfully!")

# Monkey patch LMDeploy functions and layer mappings
print("🐒 Patching LMDeploy functions and mappings for hybrid Qwen3.5...")
try:
    import lmdeploy.lite.quantization.awq
    import lmdeploy.lite.apis.auto_awq
    from lmdeploy.lite.apis.auto_awq import FC_FCS_MAP, NORM_FCS_MAP
    
    # 1. Patch smooth_layers function
    lmdeploy.lite.quantization.awq.smooth_layers = patched_smooth_layers
    lmdeploy.lite.apis.auto_awq.smooth_layers = patched_smooth_layers
    print("✅ Monkey patched smooth_layers successfully!")

    # 2. Patch save_vl_model function to avoid OOM SIGKILL
    lmdeploy.lite.apis.auto_awq.save_vl_model = patched_save_vl_model
    print("✅ Monkey patched save_vl_model successfully!")

    # 3. Register Qwen3_5DecoderLayer mapping supporting both linear and standard attention layers
    FC_FCS_MAP['Qwen3_5DecoderLayer'] = {
        'self_attn.v_proj': ['self_attn.o_proj'],
        'linear_attn.in_proj_qkv': ['linear_attn.out_proj'],
        'mlp.up_proj': ['mlp.down_proj']
    }
    NORM_FCS_MAP['Qwen3_5DecoderLayer'] = {
        'input_layernorm': [
            'self_attn.q_proj', 'self_attn.k_proj', 'self_attn.v_proj',
            'linear_attn.in_proj_qkv', 'linear_attn.in_proj_z', 'linear_attn.in_proj_b', 'linear_attn.in_proj_a'
        ],
        'post_attention_layernorm': ['mlp.gate_proj', 'mlp.up_proj']
    }
    print("✅ Registered hybrid Qwen3_5DecoderLayer mappings successfully!")
except Exception as e:
    print(f"❌ Failed to patch LMDeploy: {e}")
    sys.exit(1)

# Import auto_awq and execute
from lmdeploy.lite.apis.auto_awq import auto_awq

model_path = "/workspace/exercise 3/Qwen3.5-2B-BTC"
work_dir = "/workspace/exercise 3/submissions/08072026/lmdeploy/qwen35-2b-awq"

print(f"🔥 Starting AWQ quantization using auto_awq...")
try:
    auto_awq(
        model=model_path,
        work_dir=work_dir,
        calib_dataset="wikitext2",
        calib_samples=32,
        calib_seqlen=512,
        w_bits=4,
        w_group_size=128
    )
    print("🎉 SUCCESS!!! AWQ quantization finished successfully!")
except Exception as e:
    print(f"❌ AWQ quantization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)