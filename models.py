from extensions import db

# simple junction (no quantity)
service_ticket_parts = db.Table(
    "service_ticket_parts",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_ticket.id"), primary_key=True),
    db.Column("inventory_id", db.Integer, db.ForeignKey("inventory.id"), primary_key=True),
)

class Inventory(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)

    tickets = db.relationship(
        "ServiceTicket",
        secondary=service_ticket_parts,
        back_populates="parts",
        lazy="dynamic",
    )

# In your existing ServiceTicket model, add:
# parts = db.relationship("Inventory", secondary=service_ticket_parts, back_populates="tickets", lazy="dynamic")
