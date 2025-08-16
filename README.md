Mechanic Service API

A Flask-based REST API for managing mechanics, customers, service tickets, and inventory.
This project demonstrates authentication with JWT, rate limiting, caching, and advanced database relationships.

Features

Authentication

Customer login with JWT token

Protected routes requiring valid token

Rate Limiting & Caching

Rate-limited login route

Cached customer list & tickets

Customer

Login

View their own service tickets

Mechanics

View mechanics ordered by number of tickets worked

Service Tickets

Create, list, update (assign/remove mechanics)

Attach inventory parts

Inventory

Full CRUD: create, read, update, delete

Link parts to service tickets

Tech Stack

Flask

Flask-SQLAlchemy

Flask-Limiter

Flask-Caching

Marshmallow

Python-Jose (JWT)

SQLite (default, easily swapped with Postgres/MySQL)

Setup
1. Clone Repository
git clone <your-repo-url>
cd Mechanic_service_api

2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Initialize Database
python init_db.py

5. Run Server
python run.py


App runs at http://127.0.0.1:5001

Endpoints
Customers

POST /customers/login → Get JWT token

{ "email": "test@example.com", "password": "password123" }


GET /customers/my-tickets → Requires Authorization: Bearer <token>

Mechanics

GET /mechanics/top → Returns mechanics ordered by tickets worked

Service Tickets

GET /service_tickets/ → List all tickets

PUT /service_tickets/<ticket_id>/edit → Add/remove mechanics

{
  "add_ids": [1],
  "remove_ids": [2]
}


POST /service_tickets/<ticket_id>/add-part/<part_id> → Attach inventory item

Inventory

POST /inventory/ → Create

{ "name": "Oil Filter", "price": 14.99 }


GET /inventory/ → List

PUT /inventory/<id> → Update

DELETE /inventory/<id> → Delete

Testing with Postman

Import the provided new_mechanic_app.postman_collection.json

Run requests in order:

Login → Copy JWT token

Access protected endpoints using Authorization: Bearer <token>

Test mechanics, service tickets, and inventory CRUD

Assignment Coverage

✔️ Rate Limiting & Caching
✔️ JWT Token Authentication
✔️ Customer Login + My Tickets
✔️ Mechanic Ranking Query
✔️ Service Ticket Update (add/remove mechanics)
✔️ Inventory Model + CRUD + Relation to Tickets
✔️ Postman Collection Export

✅ Meets all required project requirements