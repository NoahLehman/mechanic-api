from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from .schemas import ServiceTicketSchema

service_ticket_bp = Blueprint('service_ticket_bp', __name__)

schema = ServiceTicketSchema()
schema_many = ServiceTicketSchema(many=True)

@service_ticket_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.json
    new_ticket = schema.load(data, session=db.session)
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify(schema.dump(new_ticket)), 201

@service_ticket_bp.route('/', methods=['GET'])
def list_tickets():
    tickets = ServiceTicket.query.all()
    return jsonify(schema_many.dump(tickets)), 200

@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
    return jsonify(schema.dump(ticket)), 200

@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
    return jsonify(schema.dump(ticket)), 200
