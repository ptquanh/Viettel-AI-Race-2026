import asyncio
import aiohttp
import json
import time
from statistics import mean

# ==========================================
# 1. CẤU HÌNH THAM SỐ CHẤM ĐIỂM TỪ BTC
# ==========================================
F_TTFT = 100.0   # ms
C_TTFT = 1500.0  # ms
F_TPOT = 20.0    # ms
C_TPOT = 45.0    # ms
GAMMA = 2
W = 0.5

# Cấu hình Server
API_URL = "http://localhost:8000/v1/completions"
MODEL_NAME = "Qwen3.5-2B"

# ==========================================
# 2. HÀM TÍNH ĐIỂM TOÁN HỌC
# ==========================================
def clamp(val, min_val, max_val):
    """Giới hạn giá trị trong khoảng [min_val, max_val]"""
    return max(min_val, min(val, max_val))

def calculate_request_score(ttft_ms, tpot_ms):
    """Tính ERS cho 1 request dựa trên công thức BTC"""
    # Tính s_ttft
    ttft_ratio = (C_TTFT - ttft_ms) / (C_TTFT - F_TTFT)
    s_ttft = clamp(ttft_ratio, 0.0, 1.0) ** GAMMA
    
    # Tính s_tpot
    tpot_ratio = (C_TPOT - tpot_ms) / (C_TPOT - F_TPOT)
    s_tpot = clamp(tpot_ratio, 0.0, 1.0) ** GAMMA
    
    return W * s_ttft + (1 - W) * s_tpot

# ==========================================
# 3. XỬ LÝ GỌI API & ĐO LƯỜNG (ASYNC)
# ==========================================
async def send_request(session, req_id, prompt, max_tokens, delay_s):
    """Mô phỏng 1 request có độ trễ (arrival time) và đọc luồng Stream"""
    if delay_s > 0:
        await asyncio.sleep(delay_s)
        
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "stream": True,  # Bắt buộc True để đo TTFT/TPOT
        "temperature": 0.1
    }
    
    t_sent = time.perf_counter()
    t_first = None
    t_last = None
    tokens_received = 0

    try:
        async with session.post(API_URL, json=payload) as response:
            if response.status != 200:
                print(f"[Req {req_id}] Failed with status {response.status}")
                return 0.0, 0.0, 0.0

            # Đọc trực tiếp luồng bytes để xử lý SSE
            async for line in response.content:
                line = line.decode('utf-8').strip()
                if line.startswith("data: ") and line != "data: [DONE]":
                    now = time.perf_counter()
                    
                    if t_first is None:
                        t_first = now  # Ghi nhận Token đầu tiên
                        
                    t_last = now       # Cập nhật liên tục Token cuối cùng
                    tokens_received += 1
                    
        # Kiểm tra tính hợp lệ
        if tokens_received == 0 or t_first is None:
            print(f"[Req {req_id}] 0 tokens received.")
            return 0.0, 0.0, 0.0

        # Đổi giây sang mili-giây
        ttft_ms = (t_first - t_sent) * 1000
        
        if tokens_received > 1:
            tpot_ms = ((t_last - t_first) / (tokens_received - 1)) * 1000
        else:
            tpot_ms = 0.0

        score = calculate_request_score(ttft_ms, tpot_ms)
        print(f"[Req {req_id}] TTFT: {ttft_ms:.1f}ms | TPOT: {tpot_ms:.1f}ms | Score: {score:.3f}")
        return ttft_ms, tpot_ms, score

    except Exception as e:
        print(f"[Req {req_id}] Error: {e}")
        return 0.0, 0.0, 0.0

# ==========================================
# 4. CHẠY TRACE FILE & TỔNG HỢP ERS
# ==========================================
async def main():
    # Mô phỏng đọc file trace-round1.jsonl
    # Trong thực tế, bạn đổi hàm này thành logic đọc file local
    mock_trace = [
        {"id": 1, "prompt": "Giải thích về Docker:", "max_tokens": 100, "delay": 0.0},
        {"id": 2, "prompt": "Viết code Python tính Fibonacci:", "max_tokens": 50, "delay": 0.2},
        {"id": 3, "prompt": "Tóm tắt chiến tranh thế giới thứ 2:", "max_tokens": 200, "delay": 0.5},
        # Bạn sẽ load 120 requests thật vào đây...
    ]
    
    print(f"🚀 Bắt đầu bắn {len(mock_trace)} requests vào {API_URL}...")
    start_time = time.time()
    
    # Dùng tcp_connector để không giới hạn connection
    connector = aiohttp.TCPConnector(limit=0)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for req in mock_trace:
            task = send_request(
                session, 
                req["id"], 
                req["prompt"], 
                req["max_tokens"], 
                req["delay"]
            )
            tasks.append(task)
            
        # Chờ toàn bộ 120 requests chạy xong
        results = await asyncio.gather(*tasks)

    # Phân tích kết quả
    total_time = time.time() - start_time
    valid_scores = [res[2] for res in results]
    
    final_ers = mean(valid_scores) if valid_scores else 0.0
    
    print("-" * 50)
    print("📊 BÁO CÁO KẾT QUẢ BENCHMARK LOCAL")
    print("-" * 50)
    print(f"Thời gian test tổng: {total_time:.2f} giây")
    print(f"Số lượng requests:   {len(valid_scores)}")
    print(f"Điểm ERS trung bình: {final_ers:.4f} (Max: 1.0)")
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())