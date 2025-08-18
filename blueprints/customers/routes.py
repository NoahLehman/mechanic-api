from flask import Blueprint, request, g
from werkzeug.security import check_password_hash
from extensions import db, limiter, cache
from auth import encode_token, token_required
from models import Customer, ServiceTicket
from schemas import login_schema, CustomerSchema, ServiceTicketSchema

customers_bp = Blueprint("customers", __name__)

# Pagination on GET Customers
@customers_bp.get("/")
@limiter.limit("30 per minute")
@cache.cached(timeout=30, query_string=True)
def list_customers():
    """
    summary: List customers
    description: Returns a paginated list of customers
    tags:
      - Customers
    parameters:
      - in: query
        name: page
        type: integer
        description: Page number
      - in: query
        name: per_page
        type: integer
        description: Number of results per page
    responses:
      200:
        description: Paginated customers list
        schema:
          type: object
          properties:
            items:
              type: array
              items: CustomerResponse
            page:
              type: integer
            per_page:
              type: integer
            total:
              type: integer
            pages:
              type: integer
    """
    page = request.args.get("page", type=int, default=1)
    per_page = request.args.get("per_page", type=int, default=20)
    pagination = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
    items = [ {"id": c.id, "email": c.email} for c in pagination.items ]
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
    """
    summary: Customer login
    description: Authenticates a customer and returns a JWT token
    tags:
      - Customers
    parameters:
      - in: body
        name: credentials
        schema: LoginPayload
    responses:
      200:
        description: Successful login
        schema: LoginResponse
      401:
        description: Invalid credentials
    """
    data = login_schema.load(request.get_json() or {})
    customer = Customer.query.filter_by(email=data["email"]).first()
    if not customer or not check_password_hash(customer.password_hash, data["password"]):
        return {"message": "Invalid credentials"}, 401
    token = encode_token(customer.id, role="customer")
    return {"token": token}, 200

# GET /my-tickets (requires token)
@customers_bp.get("/my-tickets")
@token_required
@cache.cached(timeout=30)
def my_tickets():
    """
    summary: Get my tickets
    description: Returns service tickets belonging to the authenticated customer
    tags:
      - Customers
    security:
      - Bearer: []
    responses:
      200:
        description: List of tickets for the authenticated customer
        schema:
          type: array
          items: ServiceTicketResponse
      401:
        description: Missing or invalid token
    """
    tickets = ServiceTicket.query.filter_by(customer_id=g.customer_id).all()
    return ServiceTicketSchema(many=True).dump(tickets), 200
