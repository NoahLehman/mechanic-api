from app import create_app
from extensions import db
from models import Customer, Mechanic, ServiceTicket, Inventory
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # 1. Create tables
    db.create_all()

    # --- Seed Customer ---
    if not Customer.query.filter_by(email="test@example.com").first():
        test_customer = Customer(
            email="test@example.com",
            password_hash=generate_password_hash("password123")
        )
        db.session.add(test_customer)
        print("Seeded customer: test@example.com / password123")
    else:
        test_customer = Customer.query.filter_by(email="test@example.com").first()
        print("Customer already exists.")

    # --- Seed Mechanic ---
    if not Mechanic.query.filter_by(name="Bob Builder").first():
        test_mechanic = Mechanic(name="Bob Builder")
        db.session.add(test_mechanic)
        print("Seeded mechanic: Bob Builder")
    else:
        test_mechanic = Mechanic.query.filter_by(name="Bob Builder").first()
        print(" Mechanic already exists.")

    # --- Seed Service Ticket ---
    if not ServiceTicket.query.first():
        test_ticket = ServiceTicket(
            description="Brake squeaking issue",
            customer_id=test_customer.id
        )
        test_ticket.mechanics.append(test_mechanic)
        db.session.add(test_ticket)
        print("Seeded service ticket assigned to test customer and mechanic.")
    else:
        test_ticket = ServiceTicket.query.first()
        print("Service ticket already exists.")

    # --- Seed Inventory Item ---
    if not Inventory.query.filter_by(name="Brake Pad").first():
        test_part = Inventory(name="Brake Pad", price=39.99)
        db.session.add(test_part)
        print("Seeded inventory part: Brake Pad")
    else:
        test_part = Inventory.query.filter_by(name="Brake Pad").first()
        print("Inventory item already exists.")

    # Commit all changes
    db.session.commit()
    print("Database seeding complete!")
