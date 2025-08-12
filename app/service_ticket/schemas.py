from app.extensions import ma
from app.models import ServiceTicket
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ServiceTicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_relationships = True