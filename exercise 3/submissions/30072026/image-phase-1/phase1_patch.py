import os
import site
import sys

def patch_vllm_cudagraph_sizes():
    """
    Tìm và patch file định nghĩa kích thước CUDA Graph trong vLLM.
    Mục đích: Giảm số lượng graph capture từ 76 xuống còn 15 sizes,
    chỉ cover tối đa batch_size=70 (giới hạn workload của cuộc thi).
    Giúp giảm VRAM tiêu thụ và tăng tốc độ warmup.
    """
    # Tìm đường dẫn cài đặt vllm
    site_packages = site.getsitepackages()
    vllm_path = None
    for sp in site_packages:
        if os.path.exists(os.path.join(sp, 'vllm')):
            vllm_path = os.path.join(sp, 'vllm')
            break
            
    if not vllm_path:
        print("❌ Không tìm thấy vllm trong site-packages")
        sys.exit(1)
        
    print(f"✅ Tìm thấy vllm tại: {vllm_path}")
    
    # Cấu trúc file vLLM có thể khác nhau tùy version.
    # Thông thường _BATCH_SIZES_TO_CAPTURE nằm trong model_runner.py hoặc gpu_model_runner.py hoặc utils.py
    target_files = [
        os.path.join(vllm_path, 'worker', 'model_runner.py'),
        os.path.join(vllm_path, 'worker', 'gpu_model_runner.py'),
        os.path.join(vllm_path, 'engine', 'async_llm_engine.py')
    ]
    
    patched = False
    for filepath in target_files:
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Dấu hiệu nhận biết mảng CUDA Graph sizes
        if '_BATCH_SIZES_TO_CAPTURE' in content or 'batch_sizes = [' in content:
            print(f"🔄 Đang patch file: {filepath}")
            
            # Ghi đè mảng _BATCH_SIZES_TO_CAPTURE
            import re
            # Regex tìm mảng bắt đầu bằng [1, 2, 4 ... và kết thúc bằng ]
            pattern1 = r'_BATCH_SIZES_TO_CAPTURE\s*=\s*\[.*?\]'
            replacement1 = '_BATCH_SIZES_TO_CAPTURE = [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 70]'
            
            new_content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
            
            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"✅ Đã patch thành công mảng _BATCH_SIZES_TO_CAPTURE trong {filepath}!")
                patched = True
                
    if not patched:
        print("⚠️ Không tìm thấy biến _BATCH_SIZES_TO_CAPTURE để patch. Có thể vLLM version này dùng logic khác.")
        print("Hãy kiểm tra thủ công trong source vLLM.")
    else:
        print("🎉 Phase 1 Patch hoàn tất. Build image ngay!")

if __name__ == "__main__":
    patch_vllm_cudagraph_sizes()
