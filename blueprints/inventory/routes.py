from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from extensions import db, cache
from auth import token_required
from models import Inventory
from schemas import inventory_schema, inventories_schema

inventory_bp = Blueprint("inventory", __name__)

# CREATE
@inventory_bp.post("/")
@token_required
def create_part():
    """
    summary: Create inventory part
    description: Adds a new inventory item to the database
    tags:
      - Inventory
    security:
      - Bearer: []
    parameters:
      - in: body
        name: part
        schema: InventoryPayload
    responses:
      201:
        description: Created part
        schema: InventoryResponse
      400:
        description: Part name must be unique
    """
    data = request.get_json() or {}
    part = Inventory(name=data.get("name"), price=data.get("price"))
    db.session.add(part)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"message": "Part name must be unique"}, 400
    return inventory_schema.dump(part), 201

# READ (list)
@inventory_bp.get("/")
@cache.cached(timeout=60, query_string=True)
def list_parts():
    """
    summary: List inventory parts
    description: Returns all parts in the inventory
    tags:
      - Inventory
    responses:
      200:
        description: List of inventory items
        schema:
          type: array
          items: InventoryResponse
    """
    parts = Inventory.query.order_by(Inventory.name.asc()).all()
    return inventories_schema.dump(parts), 200

# READ one
@inventory_bp.get("/<int:part_id>")
def get_part(part_id: int):
    """
    summary: Get part
    description: Returns details for a specific inventory part
    tags:
      - Inventory
    parameters:
      - in: path
        name: part_id
        required: true
        type: integer
        description: Inventory part ID
    responses:
      200:
        description: Inventory part details
        schema: InventoryResponse
      404:
        description: Part not found
    """
    part = Inventory.query.get_or_404(part_id)
    return inventory_schema.dump(part), 200

# UPDATE
@inventory_bp.put("/<int:part_id>")
@token_required
def update_part(part_id: int):
    """
    summary: Update part
    description: Updates an inventory item
    tags:
      - Inventory
    security:
      - Bearer: []
    parameters:
      - in: path
        name: part_id
        required: true
        type: integer
      - in: body
        name: part
        schema: InventoryPayload
    responses:
      200:
        description: Updated part
        schema: InventoryResponse
      400:
        description: Part name must be unique
      404:
        description: Part not found
    """
    part = Inventory.query.get_or_404(part_id)
    data = request.get_json() or {}
    if "name" in data:
        part.name = data["name"]
    if "price" in data:
        part.price = data["price"]
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"message": "Part name must be unique"}, 400
    return inventory_schema.dump(part), 200

# DELETE
@inventory_bp.delete("/<int:part_id>")
@token_required
def delete_part(part_id: int):
    """
    summary: Delete part
    description: Deletes a part from the inventory
    tags:
      - Inventory
    security:
      - Bearer: []
    parameters:
      - in: path
        name: part_id
        required: true
        type: integer
        description: Inventory part ID
    responses:
      200:
        description: Part deleted
      404:
        description: Part not found
    """
    part = Inventory.query.get_or_404(part_id)
    db.session.delete(part)
    db.session.commit()
    return {"message": "deleted"}, 200
