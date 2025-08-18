from app.extensions import ma
from app.models import Mechanic
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class MechanicSchema(SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, example="John Doe")
    specialty = fields.Str(required=True, example="Engine Repair")

    class Meta:
        model = Mechanic
        load_instance = True