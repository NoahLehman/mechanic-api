# Mechanic Service API

A Flask-based REST API for managing mechanics and service tickets, built with SQLAlchemy and Marshmallow.  
Implements full CRUD for mechanics, ticket creation, and assignment/removal of mechanics from tickets.

## Features

### Mechanics (`/mechanics`)
- **POST `/`** – Create a new mechanic.
- **GET `/`** – Retrieve all mechanics.
- **PUT `/<id>`** – Update a mechanic by ID.
- **DELETE `/<id>`** – Delete a mechanic by ID.

### Service Tickets (`/service-tickets`)
- **POST `/`** – Create a new service ticket.
- **GET `/`** – Retrieve all service tickets.
- **PUT `/<ticket_id>/assign-mechanic/<mechanic_id>`** – Assign a mechanic to a ticket.
- **PUT `/<ticket_id>/remove-mechanic/<mechanic_id>`** – Remove a mechanic from a ticket.

## Tech Stack
- **Flask** – Web framework
- **Flask-SQLAlchemy** – ORM for database operations
- **Flask-Marshmallow / Marshmallow-SQLAlchemy** – Serialization/deserialization
- **SQLite** – Default database (configurable)

## Project Structure
Mechanic_service_api/
│
├── app/
│ ├── init.py # App factory, blueprint registration
│ ├── extensions.py # DB & Marshmallow initialization
│ ├── models.py # SQLAlchemy models and relationships
│ │
│ ├── mechanic/
│ │ ├── init.py
│ │ ├── routes.py # CRUD routes for mechanics
│ │ └── schemas.py # Mechanic schema
│ │
│ └── service_ticket/
│ ├── init.py
│ ├── routes.py # Ticket CRUD + assign/remove mechanic
│ └── schemas.py # Ticket schema
│
├── config.py # Config class (DB URI, etc.)
├── init_db.py # Script to create DB tables
├── mechanic-postman.json # Postman collection for testing
└── requirements.txt

## Setup Instructions

1. **Clone the repository**
```bash
git clone <repo_url>
cd Mechanic_service_api
```

2. **Create & activate a virtual environment**
```bash
**python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**

```bash
python init_db.py
```
5. **Run the app**
```bash
flask --app app run --debug
```

Test with Postman

Import mechanic-postman.json into Postman.

Set the base_url variable to http://localhost:5001.
