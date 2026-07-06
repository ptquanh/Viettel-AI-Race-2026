import json

ts = []
ml = []
temps = []
seeds = []
msg_counts = []
input_lens = []
with open('input/trace-round1.jsonl', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line)
        ts.append(d['timestamp_ms'])
        b = d['body']
        ml.append(b['max_tokens'])
        temps.append(b['temperature'])
        seeds.append(b['seed'])
        msg_counts.append(len(b['messages']))
        total_chars = sum(len(m['content']) for m in b['messages'])
        input_lens.append(total_chars)

print(f'Total requests: {len(ts)}')
print(f'Timestamp range: {min(ts)} - {max(ts)} ms (span={max(ts)-min(ts)} ms = {(max(ts)-min(ts))/1000:.1f}s)')
print(f'Max tokens: min={min(ml)}, max={max(ml)}, unique={sorted(set(ml))}')
print(f'Temperature: unique={sorted(set(temps))}')
print(f'Seed: unique count={len(set(seeds))}')
print(f'Messages per request: min={min(msg_counts)}, max={max(msg_counts)}, unique={sorted(set(msg_counts))}')
print(f'Input char length: min={min(input_lens)}, max={max(input_lens)}, avg={sum(input_lens)/len(input_lens):.0f}')

# Check for shared system prompts
sys_prompts = set()
with open('input/trace-round1.jsonl', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line)
        for m in d['body']['messages']:
            if m['role'] == 'system':
                sys_prompts.add(m['content'][:100])

print(f'Unique system prompt prefixes (first 100 chars): {len(sys_prompts)}')
if len(sys_prompts) < len(ts):
    print('Shared system prompts? YES')
else:
    print('Shared system prompts? NO (all unique)')

# Arrival pattern analysis
import statistics
intervals = [ts[i+1] - ts[i] for i in range(len(ts)-1)]
print(f'\nArrival intervals (ms): min={min(intervals)}, max={max(intervals)}, median={statistics.median(intervals):.0f}, mean={statistics.mean(intervals):.0f}')

# Input token estimation (rough: 4 chars per token)
est_tokens = [c // 4 for c in input_lens]
print(f'Estimated input tokens: min={min(est_tokens)}, max={max(est_tokens)}, avg={sum(est_tokens)//len(est_tokens)}')

# Distribution of max_tokens
from collections import Counter
mt_dist = Counter(ml)
print(f'\nmax_tokens distribution:')
for k in sorted(mt_dist.keys()):
    print(f'  {k}: {mt_dist[k]} requests')
