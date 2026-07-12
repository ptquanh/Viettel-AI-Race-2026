cd "phase2_fp8_warmup"

echo "Building ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2..."
docker build -t ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2 .

echo "Pushing ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2..."
docker push ptquanh/sandbox-runtime:vllm-phase2-fp8-warmup-v2

cd ..

echo "Done! Warmup v2 image built and pushed successfully."
