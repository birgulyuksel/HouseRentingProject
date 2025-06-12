import requests
import threading

# Stress Test 1: "Same client sends rapid-fire reservation requests"

URL = "http://localhost:5001/reserve"
house_id = 5
email = "speedy@example.com"

def reserve_rapidly():
    for i in range(10):
        start_date = f"2025-08-{10 + i*2:02d}"
        end_date = f"2025-08-{11 + i*2 :02d}"
        try:
            response = requests.post(URL, json={
                "house_id": house_id,
                "user_email": email,
                "start_date": start_date,
                "end_date": end_date
            })
            try:
                msg = response.json().get("message", response.text)
            except Exception:
                msg = f"(Non-JSON Response) Status: {response.status_code} | Content: {response.text}"
        except Exception as e:
            msg = f"ERROR: {e}"
        
        print(f"[{i+1}] {start_date} → {end_date} : {msg}")

thread = threading.Thread(target=reserve_rapidly)
thread.start()
thread.join()