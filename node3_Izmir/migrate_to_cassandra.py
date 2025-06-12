from cassandra.cluster import Cluster
import json

# Connection
cluster = Cluster(['127.0.0.1'])
session = cluster.connect("houserental")

# Şehir bilgisi ve JSON yolu 
city = "Izmir"
json_path = "data.json"

# JSON dosyasını oku
with open(json_path, "r") as f:
    houses = json.load(f)

# Her ev için hem houses tablosuna hem de varsa reservations tablosuna veri ekle
for house in houses:
    session.execute("""
        INSERT INTO houses (city, house_id, title, price, description)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        city,
        house["house_id"],
        house["title"],
        house["price"],
        house["description"]
    ))

    for res in house.get("reservations", []):
        session.execute("""
            INSERT INTO reservations (city, house_id, user_email, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            city,
            house["house_id"],
            res["user_email"],
            res["start_date"],
            res["end_date"]
        ))

print(f"{city} verileri başarıyla Cassandra'ya aktarıldı.")
