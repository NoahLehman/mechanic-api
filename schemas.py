from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from models import Customer, Mechanic, ServiceTicket, Inventory

# Login schema (email + password)
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

login_schema = LoginSchema()

# --- Customer ---
class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# --- Mechanic ---
class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

# --- ServiceTicket ---
class ServiceTicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

# --- Inventory ---
class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
