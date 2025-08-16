# Mechanic Service API

A Flask-based REST API for managing **customers, mechanics, service tickets, and inventory**.  
This project demonstrates **JWT authentication, rate limiting, caching, and advanced database relationships**.

---

## Features

-  **Authentication**
  - Customer login with JWT
  - Protected routes requiring token
-  **Rate Limiting & Caching**
  - Login route rate-limited
  - Cached customer lists & tickets
-  **Mechanics**
  - Ranked by tickets completed
-  **Service Tickets**
  - Create, list, update (assign/remove mechanics)
  - Attach parts from inventory
-  **Inventory**
  - Full CRUD operations
  - Many-to-many relationship with tickets

---

## Tech Stack

- [Flask](https://flask.palletsprojects.com/)  
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)  
- [Flask-Limiter](https://flask-limiter.readthedocs.io/)  
- [Flask-Caching](https://flask-caching.readthedocs.io/)  
- [Marshmallow](https://marshmallow.readthedocs.io/)  
- [Python-Jose](https://python-jose.readthedocs.io/)  
- SQLite (default) – easily swappable for Postgres/MySQL  

---

## Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd Mechanic_service_api
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Initialize Database
```bash
python init_db.py
```

### 7. Run the Server
```bash
python run.py
```
## Server

Runs at **http://127.0.0.1:5001**

---

## Endpoints

### Customers
- **POST** `/customers/login` → Login & receive JWT  

  ```json
  { "email": "test@example.com", "password": "password123" }


* **GET** `/customers/my-tickets` → Requires `Authorization: Bearer <token>`

---

### Mechanics

* **GET** `/mechanics/top` → Mechanics ranked by tickets worked

---

### Service Tickets

* **GET** `/service_tickets/` → List tickets
* **PUT** `/service_tickets/<ticket_id>/edit` → Add/remove mechanics

  ```json
  {
    "add_ids": [1],
    "remove_ids": [2]
  }
  ```
* **POST** `/service_tickets/<ticket_id>/add-part/<part_id>` → Attach inventory item

---

### Inventory

* **POST** `/inventory/` → Create

  ```json
  { "name": "Oil Filter", "price": 14.99 }
  ```
* **GET** `/inventory/` → List all
* **PUT** `/inventory/<id>` → Update part
* **DELETE** `/inventory/<id>` → Remove part

---

## Testing with Postman

1. Import the provided **`new_mechanic_app.postman_collection.json`**
2. Run requests in order:

   * Login (get JWT)
   * Use token in `Authorization: Bearer <token>` header
   * Test mechanics, tickets, and inventory CRUD

---

## Assignment Coverage

*  Rate Limiting & Caching
*  JWT Token Authentication
*  Customer Login + My Tickets
*  Mechanic Ranking Query
*  Service Ticket Update (add/remove mechanics)
*  Inventory Model + CRUD + Relation to Tickets
*  Postman Collection Export
