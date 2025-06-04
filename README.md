
# Distributed House Rental System

This project is a **distributed house reservation system** developed as part of a Distributed Databases course project.  
It simulates a multi-node environment, where each node (city) manages its own house listings and supports full reservation functionality using date ranges.

---

## Features

- **Date-based reservation system** (check-in/check-out style)
- **Distributed structure** with 3 independent nodes:
  - Istanbul (`localhost:5001`)
  - Ankara (`localhost:5002`)
  - Izmir (`localhost:5003`)
- Search for houses by keyword and/or price
- View, update, and cancel your reservations
- View statistics (total/reserved/available houses per city)
- Built-in stress tests for concurrent reservation attempts

---

## Project Structure

```
HouseRentingProject/
├── node1_Istanbul/
│   ├── server.py
│   └── data.json
├── node2_Ankara/
│   ├── server.py
│   └── data.json
├── node3_Izmir/
│   ├── server.py
│   └── data.json
├── client/
│   └── client.py
├── stress_Tests/
│   ├── stres_test_1.py
│   ├── stres_test_2.py
│   └── stres_test_3.py
├── schema.png             # ER diagram
├── report.pdf             # Project report
└── README.md
```

---

## Technologies

- **Python 3.10+**
- **Flask** for REST APIs (per node)
- **requests** and **threading** for client and stress testing
- **JSON files** simulate each node’s local database

---

## How to Run the Project

### 1. Install dependencies

```bash
pip install flask requests
```

### 2. Run all three nodes in separate terminals

```bash
# Terminal 1
cd node1_istanbul
python server.py

# Terminal 2
cd node2_ankara
python server.py

# Terminal 3
cd node3_izmir
python server.py
```

Each node runs on its own port:
- Istanbul: `http://localhost:5001`
- Ankara: `http://localhost:5002`
- Izmir: `http://localhost:5003`

### 3. Launch the client

```bash
cd client
python client.py
```

You'll see a menu to:
- List or search houses
- Make a reservation
- Update or cancel an existing reservation
- View your reservations by email
- View city statistics

---

## Stress Testing

Stress tests simulate edge cases like:
- Concurrent booking of the same house
- Repeated reservation/ cancellation
- High-frequency booking attempts

To run a test:
```bash
cd stress_tests
python stres_test_1.py
```

---

## Deliverables

- `README.md` → This file
- `report.pdf` → Description, design, schema, test results
- `schema.png` → ER diagram
- `client.py` → User interface
- `server.py` (x3) → One per city (Istanbul, Ankara, Izmir)

---

## Author

- **Student Name:** Birgül Yüksel - ER1922
- **Course:** Big Data and Distributed Processing
- **Instructor:** Adam Godzinski
