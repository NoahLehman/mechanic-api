from flask import Blueprint, request
from sqlalchemy import func
from extensions import db, cache
from models import Mechanic, ServiceTicket, service_mechanic
from schemas import MechanicSchema

mechanics_bp = Blueprint("mechanics", __name__)

# GET /mechanics/leaderboard : mechanics ordered by most tickets worked
@mechanics_bp.get("/leaderboard")
@cache.cached(timeout=60, query_string=True)
def leaderboard():
    limit = request.args.get("limit", default=50, type=int)

    q = (
        db.session.query(
            Mechanic,
            func.count(ServiceTicket.id).label("ticket_count")
        )
        .join(service_mechanic, Mechanic.id == service_mechanic.c.mechanic_id)
        .join(ServiceTicket, ServiceTicket.id == service_mechanic.c.service_ticket_id)
        .group_by(Mechanic.id)
        .order_by(func.count(ServiceTicket.id).desc())
        .limit(limit)
    )
    rows = q.all()
    return [
        {
            "mechanic": MechanicSchema().dump(m),
            "ticket_count": int(cnt)
        }
        for m, cnt in rows
    ], 200
