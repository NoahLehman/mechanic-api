# blueprints/admin/routes.py
from flask import Blueprint, current_app, jsonify, request, abort
from extensions import db
# Import models so SQLAlchemy knows about all tables before create_all()
from models import *  # noqa: F401,F403
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def _authorized():
    """Simple shared-secret check."""
    expected = os.getenv("ADMIN_INIT_TOKEN")
    supplied = request.headers.get("X-Admin-Init") or request.args.get("token")
    return bool(expected and supplied and supplied == expected)

@admin_bp.post("/init-db")
def init_db_endpoint():
    if not _authorized():
        abort(403, description="Forbidden")
    # Ensure an app context and run table creation (idempotent)
    with current_app.app_context():
        db.create_all()
    return jsonify({"ok": True, "message": "Schema initialized (idempotent)."})