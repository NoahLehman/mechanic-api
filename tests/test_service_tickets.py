# tests/test_service_tickets.py
from tests.base import BaseTestCase
from extensions import db
from models import ServiceTicket, Mechanic, Inventory

class TestServiceTickets(BaseTestCase):
    def setUp(self):
        super().setUp()
        with self.app.app_context():
            self.ticket = ServiceTicket(description="Oil change", customer_id=self.customer_id)
            self.mechanic = Mechanic(name="Bob Builder")
            self.part = Inventory(name="Oil Filter", price=14.99)
            db.session.add_all([self.ticket, self.mechanic, self.part])
            db.session.commit()
            self.ticket_id = self.ticket.id
            self.mechanic_id = self.mechanic.id
            self.part_id = self.part.id
        self.auth = self.bearer()  # token generated within app context

    def test_edit_ticket_add_mechanic(self):
        r = self.client.put(f"/service_tickets/{self.ticket_id}/edit",
                            json={"add_ids": [self.mechanic_id]}, headers=self.auth)
        self.assertEqual(r.status_code, 200)

    def test_edit_ticket_remove_mechanic(self):
        self.client.put(f"/service_tickets/{self.ticket_id}/edit",
                        json={"add_ids": [self.mechanic_id]}, headers=self.auth)
        r = self.client.put(f"/service_tickets/{self.ticket_id}/edit",
                            json={"remove_ids": [self.mechanic_id]}, headers=self.auth)
        self.assertEqual(r.status_code, 200)

    def test_add_part_success(self):
        r = self.client.post(f"/service_tickets/{self.ticket_id}/parts",
                             json={"inventory_id": self.part_id}, headers=self.auth)
        self.assertEqual(r.status_code, 201)

    def test_add_part_missing_inventory_id(self):
        r = self.client.post(f"/service_tickets/{self.ticket_id}/parts",
                             json={}, headers=self.auth)
        self.assertEqual(r.status_code, 400)

    def test_add_part_ticket_not_found(self):
        r = self.client.post("/service_tickets/999999/parts",
                             json={"inventory_id": self.part_id}, headers=self.auth)
        self.assertEqual(r.status_code, 404)
