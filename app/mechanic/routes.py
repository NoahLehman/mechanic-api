from flask import Blueprint, request, jsonify
from app.extensions import db
from .schemas import MechanicSchema
from app.models import Mechanic

mechanic_bp = Blueprint('mechanic_bp', __name__)

schema = MechanicSchema()
schema_many = MechanicSchema(many=True)

@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.json
    new_mechanic = schema.load(data, session=db.session)
    db.session.add(new_mechanic)
    db.session.commit()
    return jsonify(schema.dump(new_mechanic)), 201

@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify(schema_many.dump(mechanics))

@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return jsonify(schema.dump(mechanic))

@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 204