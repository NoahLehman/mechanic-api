from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Optional

from flask import current_app, request, g
from jose import jwt, JWTError

def encode_token(customer_id: int, *, role: str = "customer", expires_in: int = 3600) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(customer_id),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in)).timestamp()),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm=current_app.config["JWT_ALGORITHM"])

def _decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        current_app.config["SECRET_KEY"],
        algorithms=[current_app.config["JWT_ALGORITHM"]],
        options={"require_exp": True},
    )

def _extract_bearer() -> Optional[str]:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    return auth.split(" ", 1)[1].strip()

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _extract_bearer()
        if not token:
            return {"message": "Missing Bearer token"}, 401
        try:
            data = _decode_token(token)
        except JWTError:
            return {"message": "Invalid or expired token"}, 401
        g.customer_id = int(data.get("sub"))
        g.role = data.get("role", "customer")
        return fn(*args, **kwargs)
    return wrapper

def role_required(required_role: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if getattr(g, "role", None) != required_role:
                return {"message": f"{required_role.capitalize()} access required"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
 