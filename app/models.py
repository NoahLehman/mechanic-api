from app.extensions import db

mechanic_service = db.Table('mechanic_service',
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
    mechanics = db.relationship('Mechanic', secondary=mechanic_service, backref='service_tickets')