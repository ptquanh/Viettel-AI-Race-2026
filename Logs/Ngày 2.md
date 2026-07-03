```bash
# Cài đặt huggingface-cli nếu chưa có
pip install -U "huggingface_hub[cli]"

# Tải đúng phiên bản commit hash về thư mục local ./Qwen3.5-2B-BTC
huggingface-cli download Qwen/Qwen3.5-2B \
  --revision <MÃ_HASH_BTC> \
  --local-dir ./Qwen3.5-2B-BTC \
  --local-dir-use-symlinks False
```
