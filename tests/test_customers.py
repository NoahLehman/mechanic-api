# tests/test_customers.py
from tests.base import BaseTestCase
from extensions import db
from models import ServiceTicket

class TestCustomers(BaseTestCase):
    def test_login_failure(self):
        res = self.client.post("/customers/login", json={
            "email": "wrong@example.com",
            "password": "wrong"
        })
        self.assertEqual(res.status_code, 401)

    def test_login_success(self):
        res = self.client.post("/customers/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.get_json())

    def test_list_customers(self):
        res = self.client.get("/customers/")  # trailing slash matches route
        self.assertEqual(res.status_code, 200)
        body = res.get_json()
        self.assertIn("items", body)

    def test_my_tickets_unauthorized(self):
        res = self.client.get("/customers/my-tickets")
        self.assertEqual(res.status_code, 401)

    def test_my_tickets_authorized(self):
        with self.app.app_context():
            t = ServiceTicket(description="Brake squeak", customer_id=self.customer_id)
            db.session.add(t); db.session.commit()

        res = self.client.get("/customers/my-tickets", headers=self.bearer())
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)
