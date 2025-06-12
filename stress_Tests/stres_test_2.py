import requests
import threading
import random
from datetime import datetime, timedelta

# Stress Test 2: "Two clients make random requests"

NODES = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]
emails = ["clientA@example.com", "clientB@example.com"]
house_ids = [1, 2, 3, 4, 5, 6]

def random_reserve(email):
    for i in range(15):
        node = random.choice(NODES)
        house_id = random.choice(house_ids)
        day_offset = random.randint(1, 30)
        start_date = (datetime(2025, 7, 1) + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        end_date = (datetime(2025, 7, 1) + timedelta(days=day_offset+1)).strftime("%Y-%m-%d")
        try:
            response = requests.post(f"{node}/reserve", json={
                "house_id": house_id,
                "user_email": email,
                "start_date": start_date,
                "end_date": end_date
            })
            print(f"[{email}] {node}/house_{house_id} {start_date}-{end_date} →", response.json().get("message", response.text))
        except Exception as e:
            print(f"[{email}] Error contacting {node}: {e}")

threads = []
for email in emails:
    t = threading.Thread(target=random_reserve, args=(email,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
