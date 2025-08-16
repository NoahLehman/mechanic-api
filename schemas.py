from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Inventory, Customer, ServiceTicket, Mechanic

# Login schema (email + password only)
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

login_schema = LoginSchema()

class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

# Assume you already have CustomerSchema, ServiceTicketSchema, MechanicSchema, plus plural forms
