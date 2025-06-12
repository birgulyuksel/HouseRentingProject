# Distributed House Rental System (Cassandra Edition)

This project is a **distributed house reservation system** developed as part of a Distributed Databases course project.
It simulates a multi-node environment, where each node (city) manages its own house listings and supports full reservation functionality using date ranges.

All data is now stored in a **centralized Apache Cassandra** database instead of local JSON files, enabling a realistic and scalable distributed data architecture.

---

## Features

* **Date-based reservation system** (check-in/check-out style)
* **Distributed structure** with 3 independent nodes:

  * Istanbul (`localhost:5001`)
  * Ankara (`localhost:5002`)
  * Izmir (`localhost:5003`)
* Backend powered by **Apache Cassandra** (city-based partitioning)
* RESTful API for all CRUD operations
* Search for houses by keyword and/or price
* View, update, and cancel reservations
* View statistics (total/reserved/available houses per city)
* Built-in stress tests for concurrent reservation attempts

---

## Project Structure

```
HouseRentingProject/
├── node1_Istanbul/
│   └── server.py
├── node2_Ankara/
│   └── server.py
├── node3_Izmir/
│   └── server.py
├── client/
│   └── client.py
├── stress_tests/
│   ├── stress_test_1_cassandra.py
│   ├── stress_test_2_cassandra.py
│   └── stress_test_3_cassandra.py
├── schema.png             # ER diagram
├── report.pdf             # Project report
└── README.md
```

---

## Technologies

* **Python 3.10+**
* **Flask** for REST APIs (per node)
* **Apache Cassandra** as distributed database
* **requests** and **threading** for client and stress testing

---

## How to Run the Project

### 1. Install dependencies

```bash
pip install flask requests cassandra-driver
```

### 2. Ensure Cassandra is running (Docker recommended)

```bash
docker run --name cassandra -p 9042:9042 -d cassandra
```

Wait \~20 seconds for it to initialize, then you can optionally enter `cqlsh`:

```bash
docker exec -it cassandra cqlsh
```

### 3. Run all three nodes in separate terminals

```bash
# Terminal 1
cd node1_istanbul
py -3.10 server.py

# Terminal 2
cd node2_ankara
py -3.10 server.py

# Terminal 3
cd node3_izmir
py -3.10 server.py
```

### 4. Launch the client

```bash
cd client
python client.py
```

---

## Stress Testing (Cassandra-Based)

Stress tests simulate scenarios like:

* ✅ High-frequency reservations from one client
* ✅ Randomized heavy access from multiple clients
* ✅ Competitive reservation attempts with fair distribution

To run tests:

```bash
cd stress_tests
python stress_test_1_cassandra.py
python stress_test_2_cassandra.py
python stress_test_3_cassandra.py
```

---

## Deliverables

* `README.md` → This file
* `report.pdf` → Updated project report (Cassandra edition)
* `schema.png` → ER diagram (updated for Cassandra)
* `client.py` → Terminal interface
* `server.py` (x3) → One per city, Cassandra-powered
* `stress_tests/` → Realistic concurrency and load test scripts

---

## Author

* **Student Name:** Birgül Yüksel - ER1922
* **Course:** Big Data and Distributed Processing
* **Instructor:** Adam Godzinski
