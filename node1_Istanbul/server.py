from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"

from datetime import datetime

def is_available(existing_reservations, new_start, new_end):
    new_start = datetime.strptime(new_start, "%Y-%m-%d")
    new_end = datetime.strptime(new_end, "%Y-%m-%d")
    
    for res in existing_reservations:
        existing_start = datetime.strptime(res["start_date"], "%Y-%m-%d")
        existing_end = datetime.strptime(res["end_date"], "%Y-%m-%d")

        # Çakışma varsa False döndür
        if new_start <= existing_end and new_end >= existing_start:
            return False
    return True


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

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

    data = load_data()
    for house in data:
        if house["house_id"] == house_id:
            reservations = house.get("reservations", [])
            # Rezervasyonu bul
            target_res = None
            for res in reservations:
                if res["user_email"] == user_email and res["start_date"] == old_start and res["end_date"] == old_end:
                    target_res = res
                    break

            if not target_res:
                return jsonify({"message": "Reservation not found"}), 404

            # Geçici olarak rezervasyonu kaldır
            reservations.remove(target_res)
            # Yeni tarih uygun mu?
            if not is_available(reservations, new_start, new_end):
                reservations.append(target_res)  # Eski haline geri koy
                return jsonify({"message": "New dates are not available"}), 409

            # Güncelle
            target_res["start_date"] = new_start
            target_res["end_date"] = new_end
            reservations.append(target_res)
            house["reservations"] = reservations
            save_data(data)
            return jsonify({"message": "Reservation updated successfully"})

    return jsonify({"message": "House not found"}), 404

# GET /stats
@app.route("/stats", methods=["GET"])
def get_statistics():
    try:
        data = load_data()
        total = len(data)
        reserved = sum(len(h.get("reservations", [])) > 0 for h in data)
        available = total - reserved

        return jsonify({
            "total_houses": total,
            "reserved": reserved,
            "available": available
        })
    except Exception as e:
        print("Error in /stats:", e)
        return jsonify({"message": "Internal server error"}), 500

@app.route("/reservations", methods=["GET"])
def get_user_reservations():
    email = request.args.get("email", "").lower()
    if not email:
        return jsonify({"message": "Email parameter is required."}), 400

    data = load_data()
    user_reservations = []

    for house in data:
        for res in house.get("reservations", []):
            if res["user_email"].lower() == email:
                user_reservations.append({
                    "house_id": house["house_id"],
                    "title": house["title"],
                    "location": house["location"],
                    "price": house["price"],
                    "start_date": res["start_date"],
                    "end_date": res["end_date"]
                })

    return jsonify(user_reservations)


@app.route("/search", methods=["GET"])
def search_houses():
    title_query = request.args.get("title", "").lower()
    max_price = request.args.get("max_price", None)

    data = load_data()
    filtered = []

    for house in data:
        matches_title = title_query in house["title"].lower()
        matches_price = True if not max_price else house["price"] <= int(max_price)

        if matches_title and matches_price:
            filtered.append(house)

    return jsonify(filtered)

@app.route("/houses", methods=["GET"])
def get_all_houses():
    data = load_data()
    return jsonify(data)

@app.route("/houses/available", methods=["GET"])
def get_available_houses():
    data = load_data()
    available = [h for h in data if not h.get("reservations")]
    return jsonify(available)

@app.route("/reserve", methods=["POST"])
def reserve_house():
    body = request.json
    house_id = body.get("house_id")
    user_email = body.get("user_email")
    start_date = body.get("start_date")
    end_date = body.get("end_date")

    if not all([house_id, user_email, start_date, end_date]):
        return jsonify({"message": "Missing required fields."}), 400

    data = load_data()

    for house in data:
        if house["house_id"] == house_id:
            reservations = house.get("reservations", [])
            if is_available(reservations, start_date, end_date):
                reservations.append({
                    "user_email": user_email,
                    "start_date": start_date,
                    "end_date": end_date
                })
                house["reservations"] = reservations
                save_data(data)
                return jsonify({"message": "Reservation successful!"})
            else:
                return jsonify({"message": "House is already booked for selected dates."}), 409

    return jsonify({"message": "House not found."}), 404


# POST /cancel
@app.route("/cancel", methods=["POST"])
def cancel_reservation():
    body = request.json
    house_id = body.get("house_id")
    user_email = body.get("user_email")
    start_date = body.get("start_date")
    end_date = body.get("end_date")

    if not all([house_id, user_email, start_date, end_date]):
        return jsonify({"message": "Missing required fields."}), 400

    data = load_data()
    for house in data:
        if house["house_id"] == house_id:
            original_res = house.get("reservations", [])
            new_res = [r for r in original_res if not (
                r["user_email"] == user_email and
                r["start_date"] == start_date and
                r["end_date"] == end_date
            )]
            if len(original_res) == len(new_res):
                return jsonify({"message": "No matching reservation found."}), 404
            house["reservations"] = new_res
            save_data(data)
            return jsonify({"message": "Reservation cancelled."})

    return jsonify({"message": "House not found."}), 404

if __name__ == "__main__":
    app.run(port=5001)
