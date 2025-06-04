import requests
import time

URL_RESERVE = "http://localhost:5001/reserve"
URL_CANCEL = "http://localhost:5001/cancel"

email = "loopuser@example.com"
house_id = 3
start_date = "2025-08-01"
end_date = "2025-08-05"
attempts = 10  # kaç kez tekrar etsin?

def reserve():
    return requests.post(URL_RESERVE, json={
        "house_id": house_id,
        "user_email": email,
        "start_date": start_date,
        "end_date": end_date
    })

def cancel():
    return requests.post(URL_CANCEL, json={
        "house_id": house_id,
        "user_email": email,
        "start_date": start_date,
        "end_date": end_date
    })

for i in range(1, attempts + 1):
    print(f"\n🔁 Loop {i}: Reserving...")
    r1 = reserve()
    print("→", r1.json().get("message", r1.text))

    print("🔁 Cancelling...")
    r2 = cancel()
    print("→", r2.json().get("message", r2.text))

    time.sleep(0.5)  # çok hızlı olmaması için küçük bir bekleme
