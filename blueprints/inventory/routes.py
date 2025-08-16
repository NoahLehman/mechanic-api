from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from extensions import db, cache
from auth import token_required, role_required
from models import Inventory
from schemas import inventory_schema, inventories_schema

inventory_bp = Blueprint("inventory", __name__)

# CREATE
@inventory_bp.post("/")
@token_required
def create_part():
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
    parts = Inventory.query.order_by(Inventory.name.asc()).all()
    return inventories_schema.dump(parts), 200

# READ one
@inventory_bp.get("/<int:part_id>")
def get_part(part_id: int):
    part = Inventory.query.get_or_404(part_id)
    return inventory_schema.dump(part), 200

# UPDATE
@inventory_bp.put("/<int:part_id>")
@token_required
def update_part(part_id: int):
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
    part = Inventory.query.get_or_404(part_id)
    db.session.delete(part)
    db.session.commit()
    return {"message": "deleted"}, 200
