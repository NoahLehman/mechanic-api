from extensions import db

# --- Junction Tables ---
service_mechanic = db.Table(
    "service_mechanic",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_ticket.id"), primary_key=True),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanic.id"), primary_key=True),
)

service_ticket_parts = db.Table(
    "service_ticket_parts",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_ticket.id"), primary_key=True),
    db.Column("inventory_id", db.Integer, db.ForeignKey("inventory.id"), primary_key=True),
)

# --- Models ---
class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    tickets = db.relationship("ServiceTicket", back_populates="customer", lazy="dynamic")


class Mechanic(db.Model):
    __tablename__ = "mechanic"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    tickets = db.relationship(
        "ServiceTicket",
        secondary=service_mechanic,
        back_populates="mechanics",
        lazy="dynamic",
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))

    customer = db.relationship("Customer", back_populates="tickets")
    mechanics = db.relationship("Mechanic", secondary=service_mechanic, back_populates="tickets", lazy="dynamic")
    parts = db.relationship("Inventory", secondary=service_ticket_parts, back_populates="tickets", lazy="dynamic")


class Inventory(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)

    tickets = db.relationship("ServiceTicket", secondary=service_ticket_parts, back_populates="parts", lazy="dynamic")
