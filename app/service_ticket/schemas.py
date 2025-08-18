from app.extensions import ma
from app.models import ServiceTicket
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class ServiceTicketSchema(SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True, example="Brake inspection")
    status = fields.Str(required=True, example="open")
    customer_id = fields.Int(required=True, example=1)
    mechanics = fields.List(fields.Nested("MechanicSchema"), dump_only=True)

    class Meta:
        model = ServiceTicket
        load_instance = True
        include_relationships = True