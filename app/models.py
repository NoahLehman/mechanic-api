from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for many-to-many between mechanics and tickets
mechanic_service = db.Table(
    'mechanic_service',
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanic.id')),
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_ticket.id'))
)

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skill_level = db.Column(db.String(50))

class ServiceTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    # Relationships
    mechanics = db.relationship('Mechanic', secondary=mechanic_service, backref='service_tickets')
    customer = db.relationship('Customer', backref='tickets')

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)