from flask import Blueprint, request, jsonify
from app.extensions import db
from .schemas import MechanicSchema
from app.models import Mechanic

mechanic_bp = Blueprint('mechanic_bp', __name__)

schema = MechanicSchema()
schema_many = MechanicSchema(many=True)

@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    """
    summary: Create a new mechanic
    description: Adds a mechanic to the database
    tags:
      - Mechanics
    parameters:
      - in: body
        name: mechanic
        schema: MechanicPayload
    responses:
      201:
        description: Mechanic created successfully
        schema: MechanicResponse
      400:
        description: Invalid input
    """
    data = request.json
    new_mechanic = schema.load(data, session=db.session)
    db.session.add(new_mechanic)
    db.session.commit()
    return jsonify(schema.dump(new_mechanic)), 201


@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    """
    summary: Get all mechanics
    description: Returns a list of all mechanics
    tags:
      - Mechanics
    responses:
      200:
        description: List of mechanics
        schema:
          type: array
          items: MechanicResponse
    """
    mechanics = Mechanic.query.all()
    return jsonify(schema_many.dump(mechanics))


@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    """
    summary: Update mechanic
    description: Updates fields of a mechanic by ID
    tags:
      - Mechanics
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: Mechanic ID
      - in: body
        name: mechanic
        schema: MechanicPayload
    responses:
      200:
        description: Mechanic updated successfully
        schema: MechanicResponse
      404:
        description: Mechanic not found
    """
    mechanic = Mechanic.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return jsonify(schema.dump(mechanic))


@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    """
    summary: Delete mechanic
    description: Removes a mechanic from the database
    tags:
      - Mechanics
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: Mechanic ID
    responses:
      204:
        description: Mechanic deleted
      404:
        description: Mechanic not found
    """
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 204
