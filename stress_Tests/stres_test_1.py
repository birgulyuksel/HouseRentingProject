import requests
import threading

URL = "http://localhost:5001/reserve"
house_id = 1

def make_reservation(email, start, end):
    response = requests.post(URL, json={
        "house_id": house_id,
        "user_email": email,
        "start_date": start,
        "end_date": end
    })
    try:
        print(f"[{email}] → {response.json()['message']}")
    except Exception as e:
        print(f"[{email}] → Error: {response.text}")

# Kullanıcılar aynı anda başlasın
user1 = threading.Thread(target=make_reservation, args=("user1@example.com", "2025-06-10", "2025-06-15"))
user2 = threading.Thread(target=make_reservation, args=("user2@example.com", "2025-06-10", "2025-06-15"))

user1.start()
user2.start()

user1.join()
user2.join()
