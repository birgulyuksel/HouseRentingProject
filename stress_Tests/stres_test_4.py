import requests
import threading

URL = "http://localhost:5001/reserve"
house_ids = [1, 2, 3]

def try_reserve(email, house_id):
    response = requests.post(URL, json={
        "house_id": house_id,
        "user_email": email,
        "start_date": "2025-11-01",
        "end_date": "2025-11-05"
    })
    msg = response.json().get("message", response.text)
    print(f"[{email}] tried house {house_id}: {msg}")

threads = []

for hid in house_ids:
    t1 = threading.Thread(target=try_reserve, args=("client1@example.com", hid))
    t2 = threading.Thread(target=try_reserve, args=("client2@example.com", hid))
    threads.extend([t1, t2])

for t in threads:
    t.start()
for t in threads:
    t.join()
