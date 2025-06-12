from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
from datetime import datetime

# Cassandra bağlantısı
cluster = Cluster(['127.0.0.1'])
session = cluster.connect("houserental")

# Bu node'un ait olduğu şehir
CITY = "Ankara"  

app = Flask(__name__)


# Yardımcı fonksiyon: Tarih çakışması var mı?
def is_available(house_id, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    rows = session.execute("""
        SELECT start_date, end_date FROM reservations
        WHERE city=%s AND house_id=%s
    """, (CITY, house_id))

    for row in rows:
        existing_start = row.start_date
        existing_end = row.end_date
        if start <= existing_end and end >= existing_start:
            return False
    return True


@app.route("/houses", methods=["GET"])
def get_all_houses():
    rows = session.execute("SELECT * FROM houses WHERE city=%s", [CITY])
    houses = []

    for row in rows:
        house = {
            "house_id": row.house_id,
            "title": row.title,
            "price": row.price,
            "description": row.description,
            "reservations": []
        }

        res_rows = session.execute("""
            SELECT user_email, start_date, end_date FROM reservations
            WHERE city=%s AND house_id=%s
        """, (CITY, row.house_id))

        for r in res_rows:
            house["reservations"].append({
                "user_email": r.user_email,
                "start_date": str(r.start_date),
                "end_date": str(r.end_date)
            })

        houses.append(house)

    return jsonify(houses)


@app.route("/houses/available", methods=["GET"])
def get_available_houses():
    houses = []
    rows = session.execute("SELECT * FROM houses WHERE city=%s", [CITY])
    for row in rows:
        res = session.execute("""
            SELECT COUNT(*) FROM reservations WHERE city=%s AND house_id=%s
        """, (CITY, row.house_id)).one()
        if res.count == 0:
            houses.append({
                "house_id": row.house_id,
                "title": row.title,
                "price": row.price,
                "description": row.description
            })
    return jsonify(houses)


@app.route("/reserve", methods=["POST"])
def reserve_house():
    body = request.json
    house_id = body.get("house_id")
    user_email = body.get("user_email")
    start_date = body.get("start_date")
    end_date = body.get("end_date")

    if not all([house_id, user_email, start_date, end_date]):
        return jsonify({"message": "Missing required fields."}), 400

    if not is_available(house_id, start_date, end_date):
        return jsonify({"message": "House is already booked for selected dates."}), 409

    session.execute("""
        INSERT INTO reservations (city, house_id, user_email, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (CITY, house_id, user_email, start_date, end_date))

    return jsonify({"message": "Reservation successful!"})


@app.route("/cancel", methods=["POST"])
def cancel_reservation():
    body = request.json
    house_id = body.get("house_id")
    user_email = body.get("user_email")
    start_date = body.get("start_date")
    end_date = body.get("end_date")

    if not all([house_id, user_email, start_date, end_date]):
        return jsonify({"message": "Missing required fields."}), 400

    result = session.execute("""
        DELETE FROM reservations
        WHERE city=%s AND house_id=%s AND start_date=%s AND user_email=%s
    """, (CITY, house_id, start_date, user_email))

    return jsonify({"message": "Reservation cancelled."})


@app.route("/update", methods=["POST"])
def update_reservation():
    body = request.json
    house_id = body.get("house_id")
    user_email = body.get("user_email")
    old_start = body.get("old_start_date")
    old_end = body.get("old_end_date")
    new_start = body.get("new_start_date")
    new_end = body.get("new_end_date")

    if not all([house_id, user_email, old_start, old_end, new_start, new_end]):
        return jsonify({"message": "Missing fields"}), 400

    # Eski rezervasyonu sil
    session.execute("""
        DELETE FROM reservations
        WHERE city=%s AND house_id=%s AND start_date=%s AND user_email=%s
    """, (CITY, house_id, old_start, user_email))

    # Yeni tarih müsait mi kontrol et
    if not is_available(house_id, new_start, new_end):
        # Eskiyi geri yükle
        session.execute("""
            INSERT INTO reservations (city, house_id, user_email, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (CITY, house_id, user_email, old_start, old_end))
        return jsonify({"message": "New dates are not available"}), 409

    # Yeni rezervasyon ekle
    session.execute("""
        INSERT INTO reservations (city, house_id, user_email, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (CITY, house_id, user_email, new_start, new_end))

    return jsonify({"message": "Reservation updated successfully"})


@app.route("/reservations", methods=["GET"])
def get_user_reservations():
    email = request.args.get("email", "").lower()
    if not email:
        return jsonify({"message": "Email parameter is required."}), 400

    rows = session.execute("""
        SELECT * FROM reservations WHERE city=%s ALLOW FILTERING
    """, (CITY,))

    result = []
    for row in rows:
        if row.user_email.lower() == email:
            house = session.execute("""
                SELECT * FROM houses WHERE city=%s AND house_id=%s
            """, (CITY, row.house_id)).one()
            result.append({
                "house_id": row.house_id,
                "title": house.title,
                "price": house.price,
                "location": house.city,
                "start_date": str(row.start_date),
                "end_date": str(row.end_date)
            })

    return jsonify(result)


@app.route("/stats", methods=["GET"])
def get_statistics():
    all_houses = session.execute("SELECT * FROM houses WHERE city=%s", [CITY])
    total = 0
    reserved = 0

    for house in all_houses:
        total += 1
        res_count = session.execute("""
            SELECT COUNT(*) FROM reservations WHERE city=%s AND house_id=%s
        """, (CITY, house.house_id)).one().count
        if res_count > 0:
            reserved += 1

    available = total - reserved
    return jsonify({
        "total_houses": total,
        "reserved": reserved,
        "available": available
    })


@app.route("/search", methods=["GET"])
def search_houses():
    title_query = request.args.get("title", "").lower()
    max_price = request.args.get("max_price", None)

    houses = []
    rows = session.execute("SELECT * FROM houses WHERE city=%s", [CITY])

    for row in rows:
        matches_title = title_query in row.title.lower()
        matches_price = True if not max_price else row.price <= float(max_price)

        if matches_title and matches_price:
            houses.append({
                "house_id": row.house_id,
                "title": row.title,
                "price": row.price,
                "description": row.description
            })

    return jsonify(houses)


if __name__ == "__main__":
    app.run(port=5002)
