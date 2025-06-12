import requests
import threading
import random
import time

# Stress Test 3: Immediate occupancy of all seats/reservations on 2 clients.

URL = "http://localhost:5001"
house_ids = [1, 2, 3, 4, 5, 6]
emails = ["user1@example.com", "user2@example.com"]

def reserve(email, house_id):
    # ufak gecikme ile adil yarış simülasyonu
    time.sleep(random.uniform(0, 0.05))
    try:
        response = requests.post(f"{URL}/reserve", json={
            "house_id": house_id,
            "user_email": email,
            "start_date": "2025-08-01",
            "end_date": "2025-08-05"
        })
        try:
            msg = response.json().get("message", response.text)
        except:
            msg = f"(Non-JSON Response) {response.status_code} | {response.text}"
        print(f"[{email}] house {house_id} → {msg}")
    except Exception as e:
        print(f"[{email}] ERROR: {e}")

# thread'leri karıştırarak adil dağılım simülasyonu
threads = []

for house_id in house_ids:
    t1 = threading.Thread(target=reserve, args=("user1@example.com", house_id))
    t2 = threading.Thread(target=reserve, args=("user2@example.com", house_id))
    threads.extend([t1, t2])

random.shuffle(threads)  # aynı anda farklı sırada başlasınlar

for t in threads:
    t.start()

for t in threads:
    t.join()
