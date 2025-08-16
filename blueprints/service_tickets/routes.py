from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError

from extensions import db
from auth import token_required, role_required
from models import ServiceTicket, Mechanic, Inventory
from schemas import ServiceTicketSchema

service_tickets_bp = Blueprint("service_tickets", __name__)

# PUT /service_tickets/<ticket_id>/edit : add/remove mechanics
@service_tickets_bp.put("/<int:ticket_id>/edit")
@token_required
@role_required("mechanic")  # restrict to mechanics (optional but recommended)
def edit_ticket_mechanics(ticket_id: int):
    st = ServiceTicket.query.get_or_404(ticket_id)
    payload = request.get_json() or {}
    add_ids = set(payload.get("add_ids", []))
    remove_ids = set(payload.get("remove_ids", []))

    # Add mechanics
    if add_ids:
        for mid in add_ids:
            m = Mechanic.query.get(mid)
            if m and m not in st.mechanics:
                st.mechanics.append(m)

    # Remove mechanics
    if remove_ids:
        st.mechanics = [m for m in st.mechanics if m.id not in remove_ids]

    db.session.commit()
    return ServiceTicketSchema().dump(st), 200

# POST /service_tickets/<ticket_id>/parts : add a single part to an existing ticket
@service_tickets_bp.post("/<int:ticket_id>/parts")
@token_required
@role_required("mechanic")
def add_part_to_ticket(ticket_id: int):
    st = ServiceTicket.query.get_or_404(ticket_id)
    body = request.get_json() or {}
    part_id = body.get("inventory_id")
    if not part_id:
        return {"message": "inventory_id is required"}, 400

    part = Inventory.query.get_or_404(part_id)
    if part not in st.parts:
        st.parts.append(part)
        db.session.commit()
    return ServiceTicketSchema().dump(st), 201
