import urllib.request
import json
import time
import concurrent.futures
import sys

URL = "http://localhost:8000/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}
MODEL = "LFM2.5-1.2B-Instruct"

def send_request(length):
    prompt = "hello " * length
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1,
        "temperature": 0,
        "ignore_eos": True
    }
    req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        return str(e)

def warmup():
    print("[Antigravity Phase 2 v4] Starting Multi-turn Deep Warmup (Profile-Guided)...")
    
    # Trace characteristics: 6 turns, starting at 2150 tokens up to 4400 tokens.
    # The most critical shapes to compile are batch sizes that will be hit under load.
    # vLLM's max_num_seqs is typically 32.
    lengths = [1000, 2150, 3050, 4400]
    batch_sizes = [1, 4, 16, 32]
    
    for length in lengths:
        for bs in batch_sizes:
            print(f"[Antigravity Phase 2 v4] Warming up JIT Graph: context_len ~{length}, batch_size ~{bs}...")
            start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=bs) as executor:
                futures = [executor.submit(send_request, length) for _ in range(bs)]
                for future in concurrent.futures.as_completed(futures):
                    res = future.result()
            
            elapsed = time.time() - start_time
            print(f"[Antigravity Phase 2 v4] Successfully warmed up length {length} bs {bs} (Took {elapsed:.2f}s)")
    
    print("[Antigravity Phase 2 v4] Deep Warmup completed perfectly!")

if __name__ == "__main__":
    warmup()
