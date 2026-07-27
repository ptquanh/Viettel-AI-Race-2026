FROM ptquanh/sandbox-runtime:vllm-lfm25-fp8-kernels-v14

# Cài đặt build-essential để đảm bảo có gcc/g++ compile C++ extension
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy mã nguồn C++ custom kernel
COPY patch/lfm_fused_kernels.cu /patch_cpp/lfm_fused_kernels.cu
COPY patch/setup.py /patch_cpp/setup.py

# Biên dịch C++ CUDA kernel (AOT)
WORKDIR /patch_cpp
# Sử dụng python3_real vì python3 đã bị hijack
RUN /usr/bin/python3_real setup.py install

# Trở lại thư mục gốc
WORKDIR /

# Ghi đè sitecustomize.py (sử dụng C++ kernel thay vì Triton)
COPY sitecustomize.py /patch/sitecustomize.py

# Ghi đè python3_hijack để cập nhật version log
COPY python3_hijack /usr/bin/python3
RUN sed -i 's/\r$//' /usr/bin/python3 && chmod +x /usr/bin/python3
