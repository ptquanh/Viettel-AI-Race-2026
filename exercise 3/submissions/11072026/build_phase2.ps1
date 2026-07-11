cd "phase2_custom_kernel"

echo "Building ptquanh/sandbox-runtime:vllm-phase2-int8..."
docker build -t ptquanh/sandbox-runtime:vllm-phase2-int8 .

echo "Building ptquanh/sandbox-runtime:vllm-phase2-fp8..."
docker build -t ptquanh/sandbox-runtime:vllm-phase2-fp8 .

echo "Pushing ptquanh/sandbox-runtime:vllm-phase2-int8..."
docker push ptquanh/sandbox-runtime:vllm-phase2-int8

echo "Pushing ptquanh/sandbox-runtime:vllm-phase2-fp8..."
docker push ptquanh/sandbox-runtime:vllm-phase2-fp8

cd "../phase2_fp8_warmup"

echo "Building ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup..."
docker build -t ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup .

echo "Pushing ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup..."
docker push ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup

cd ..

echo "Done! All images built and pushed successfully."
