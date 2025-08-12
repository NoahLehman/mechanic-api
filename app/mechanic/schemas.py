from app.extensions import ma
from app.models import Mechanic
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True