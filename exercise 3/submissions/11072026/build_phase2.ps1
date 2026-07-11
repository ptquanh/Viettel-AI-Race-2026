cd "phase2_custom_kernel"

echo "Building ptquanh/sandbox-runtime:vllm-phase2-int8..."
docker build -t ptquanh/sandbox-runtime:vllm-phase2-int8 .

echo "Building ptquanh/sandbox-runtime:vllm-phase2-fp8..."
docker build -t ptquanh/sandbox-runtime:vllm-phase2-fp8 .

echo "Pushing ptquanh/sandbox-runtime:vllm-phase2-int8..."
docker push ptquanh/sandbox-runtime:vllm-phase2-int8

echo "Pushing ptquanh/sandbox-runtime:vllm-phase2-fp8..."
docker push ptquanh/sandbox-runtime:vllm-phase2-fp8

echo "Done! You can now submit 1203-docker-compose.yml and 1235-docker-compose.yml in parallel."
