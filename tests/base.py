# tests/base.py
import unittest
from app import create_app
from extensions import db
from models import Customer
from werkzeug.security import generate_password_hash
from auth import encode_token   # <-- add this

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            RATELIMIT_ENABLED=False,
            CACHE_TYPE="NullCache",
            SECRET_KEY="test-secret",
            JWT_ALGORITHM="HS256",
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            c = Customer(
                email="test@example.com",
                password_hash=generate_password_hash("password123"),
            )
            db.session.add(c)
            db.session.commit()
            self.customer_id = c.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # NEW: centralized auth header that runs encode_token inside app context
    def bearer(self, user_id=None):
        with self.app.app_context():
            token = encode_token(user_id or self.customer_id)
        return {"Authorization": f"Bearer {token}"}
