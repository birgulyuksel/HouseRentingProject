import requests

NODES = {
    "Istanbul": "http://localhost:5001",
    "Ankara": "http://localhost:5002",
    "Izmir": "http://localhost:5003"
}

def choose_city():
    print("\nAvailable Cities:")
    for i, city in enumerate(NODES.keys(), start=1):
        print(f"{i}. {city}")
    choice = input("Choose a city: ")
    city_list = list(NODES.keys())
    if choice.isdigit() and 1 <= int(choice) <= len(city_list):
        return city_list[int(choice) - 1]
    else:
        print("Invalid choice.")
        return None

def list_all_houses():
    city = choose_city()
    if not city:
        return
    response = requests.get(f"{NODES[city]}/houses")
    houses = response.json()
    print(f"\n🏠 Houses in {city}:")
    for house in houses:
        status = "Available" if not house.get("reservations") else "Reserved"
        print(f"ID: {house['house_id']} | {house['title']} | {house['price']}₺ | Status: {status}")
        print(f"    {house['description']}")
        if house.get("reservations"):
            for res in house["reservations"]:
                print(f"    🔒 {res['start_date']} → {res['end_date']} (by {res['user_email']})")
        print("-" * 60)

def list_available_houses():
    city = choose_city()
    if not city:
        return
    response = requests.get(f"{NODES[city]}/houses/available")
    houses = response.json()
    print(f"\n🟢 Available Houses in {city}:")
    for house in houses:
        print(f"ID: {house['house_id']} | {house['title']} | {house['price']}₺")
        print(f"    {house['description']}")
        print("-" * 60)

def reserve_house():
    city = choose_city()
    if not city:
        return
    house_id = input("Enter the house ID to reserve: ")
    email = input("Enter your email: ")
    start_date = input("Start date (YYYY-MM-DD): ")
    end_date = input("End date (YYYY-MM-DD): ")

    response = requests.post(
        f"{NODES[city]}/reserve",
        json={
            "house_id": int(house_id),
            "user_email": email,
            "start_date": start_date,
            "end_date": end_date
        }
    )

    try:
        print(response.json()["message"])
    except Exception as e:
        print("An error occurred:", e)
        print("Server response:", response.text)

def cancel_reservation():
    city = choose_city()
    if not city:
        return
    house_id = input("Enter the house ID to cancel reservation: ")
    email = input("Enter your email: ")
    start_date = input("Start date of the reservation (YYYY-MM-DD): ")
    end_date = input("End date of the reservation (YYYY-MM-DD): ")

    response = requests.post(
        f"{NODES[city]}/cancel",
        json={
            "house_id": int(house_id),
            "user_email": email,
            "start_date": start_date,
            "end_date": end_date
        }
    )

    try:
        print(response.json()["message"])
    except Exception as e:
        print("An error occurred:", e)
        print("Server response:", response.text)

def search_houses():
    city = choose_city()
    if not city:
        return
    title = input("Enter keyword (e.g., 'studio', 'villa'): ").strip()
    max_price = input("Max price (or leave empty): ").strip()

    params = {"title": title}
    if max_price:
        params["max_price"] = max_price

    response = requests.get(f"{NODES[city]}/search", params=params)
    houses = response.json()

    print(f"\n🔍 Search Results in {city}:")
    if not houses:
        print("No matching houses found.")
    for house in houses:
        status = "Available" if not house.get("reservations") else "Reserved"
        print(f"ID: {house['house_id']} | {house['title']} | {house['price']}₺ | Status: {status}")
        print(f"    {house['description']}")
        print("-" * 60)

def view_my_reservations():
    city = choose_city()
    if not city:
        return
    email = input("Enter your email: ").strip()

    response = requests.get(f"{NODES[city]}/reservations", params={"email": email})
    if response.status_code != 200:
        print(response.json().get("message", "An error occurred."))
        return

    reservations = response.json()
    if not reservations:
        print("You have no reservations in this city.")
        return

    print(f"\n📋 Reservations for {email} in {city}:")
    for res in reservations:
        print(f"House ID: {res['house_id']} | {res['title']} | {res['price']}₺")
        print(f"From {res['start_date']} to {res['end_date']}")
        print("-" * 60)

def view_city_stats():
    city = choose_city()
    if not city:
        return

    response = requests.get(f"{NODES[city]}/stats")
    if response.status_code != 200:
        print("Failed to fetch statistics.")
        return

    stats = response.json()
    print(f"\n📈 Statistics for {city}:")
    print(f"Total houses: {stats['total_houses']}")
    print(f"Reserved: {stats['reserved']}")
    print(f"Available: {stats['available']}")

def main():
    while True:
        print("\n====== Distributed House Rental System ======")
        print("1. List all houses")
        print("2. List available houses")
        print("3. Make a reservation")
        print("4. Cancel a reservation")
        print("5. Search for a house")
        print("6. View my reservations")
        print("7. View city statistics")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            list_all_houses()
        elif choice == "2":
            list_available_houses()
        elif choice == "3":
            reserve_house()
        elif choice == "4":
            cancel_reservation()
        elif choice == "5":
            search_houses()
        elif choice == "6":
            view_my_reservations()
        elif choice == "7":
            view_city_stats()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
