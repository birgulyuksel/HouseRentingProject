import requests
import threading

URL = "http://localhost:5001/reserve"
house_id = 2

def rapid_reservation_attempt(email, n):
    for i in range(n):
        start_date = f"2025-07-{10 + i*2:02d}"
        end_date = f"2025-07-{11 + i*2:02d}"
        response = requests.post(URL, json={
            "house_id": house_id,
            "user_email": email,
            "start_date": start_date,
            "end_date": end_date
        })
        print(f"Attempt {i+1}: {response.json().get('message', response.text)}")

thread = threading.Thread(target=rapid_reservation_attempt, args=("fastuser@example.com", 5))
thread.start()
thread.join()
