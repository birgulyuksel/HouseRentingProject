from cassandra.cluster import Cluster

# Cassandra bağlantısı
cluster = Cluster(['127.0.0.1'])
session = cluster.connect("houserental")

# Hangi şehirlerde işlem yapılacak
cities = ["Istanbul", "Ankara", "Izmir"]

deleted_count = 0

for city in cities:
    print(f"🔍 {city} içindeki rezervasyonlar alınıyor...")
    rows = session.execute("""
        SELECT city, house_id, start_date, user_email
        FROM reservations WHERE city = %s ALLOW FILTERING
    """, [city])

    for row in rows:
        session.execute("""
            DELETE FROM reservations
            WHERE city = %s AND house_id = %s AND start_date = %s AND user_email = %s
        """, (row.city, row.house_id, row.start_date, row.user_email))
        deleted_count += 1

print(f"\n✅ Toplam {deleted_count} rezervasyon silindi.")
