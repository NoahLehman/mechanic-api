from flask import Blueprint, request
from werkzeug.security import check_password_hash
from sqlalchemy.exc import SQLAlchemyError

from extensions import db, limiter, cache
from auth import encode_token, token_required
from models import Customer, ServiceTicket
from schemas import login_schema, Customer, ServiceTicketSchema  # adjust imports for your setup

customers_bp = Blueprint("customers", __name__)

# Pagination on GET Customers
@customers_bp.get("/")
@limiter.limit("30 per minute")
@cache.cached(timeout=30, query_string=True)
def list_customers():
    page = request.args.get("page", type=int, default=1)
    per_page = request.args.get("per_page", type=int, default=20)
    pagination = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
    items = [c.to_dict() for c in pagination.items] if hasattr(Customer, "to_dict") else [ {"id": c.id, "email": c.email} for c in pagination.items ]  # adjust to your schema
    return {
        "items": items,
        "page": page,
        "per_page": per_page,
        "total": pagination.total,
        "pages": pagination.pages,
    }

# POST /login (rate-limited)
@customers_bp.post("/login")
@limiter.limit("5 per minute")
def login():
    data = login_schema.load(request.get_json() or {})
    customer = Customer.query.filter_by(email=data["email"]).first()
    if not customer or not check_password_hash(customer.password_hash, data["password"]):
        return {"message": "Invalid credentials"}, 401
    token = encode_token(customer.id, role="customer")
    return {"token": token}, 200

# GET /my-tickets (requires token)
@customers_bp.get("/my-tickets")
@token_required
@cache.cached(timeout=30)  # short cache window
def my_tickets():
    tickets = ServiceTicket.query.filter_by(customer_id=g.customer_id).all()
    return ServiceTicketSchema(many=True).dump(tickets), 200
