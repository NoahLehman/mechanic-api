from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from .schemas import ServiceTicketSchema

service_ticket_bp = Blueprint('service_ticket_bp', __name__)

schema = ServiceTicketSchema()
schema_many = ServiceTicketSchema(many=True)

@service_ticket_bp.route('/', methods=['POST'])
def create_ticket():
    """
    summary: Create a new service ticket
    description: Creates a new service ticket in the system
    tags:
      - ServiceTickets
    parameters:
      - in: body
        name: ticket
        schema: ServiceTicketPayload
    responses:
      201:
        description: Ticket created successfully
        schema: ServiceTicketResponse
      400:
        description: Invalid input
    """
    data = request.json
    new_ticket = schema.load(data, session=db.session)
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify(schema.dump(new_ticket)), 201


@service_ticket_bp.route('/', methods=['GET'])
def list_tickets():
    """
    summary: List service tickets
    description: Returns a list of all service tickets
    tags:
      - ServiceTickets
    responses:
      200:
        description: List of service tickets
        schema:
          type: array
          items: ServiceTicketResponse
    """
    tickets = ServiceTicket.query.all()
    return jsonify(schema_many.dump(tickets)), 200


@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    """
    summary: Assign mechanic to ticket
    description: Assigns a mechanic to a specific service ticket
    tags:
      - ServiceTickets
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
        description: ID of the service ticket
      - in: path
        name: mechanic_id
        required: true
        type: integer
        description: ID of the mechanic
    responses:
      200:
        description: Updated service ticket
        schema: ServiceTicketResponse
      404:
        description: Ticket or mechanic not found
    """
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
    return jsonify(schema.dump(ticket)), 200


@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    """
    summary: Remove mechanic from ticket
    description: Removes a mechanic assignment from a specific service ticket
    tags:
      - ServiceTickets
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
        description: ID of the service ticket
      - in: path
        name: mechanic_id
        required: true
        type: integer
        description: ID of the mechanic
    responses:
      200:
        description: Updated service ticket
        schema: ServiceTicketResponse
      404:
        description: Ticket or mechanic not found
    """
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
    return jsonify(schema.dump(ticket)), 200
