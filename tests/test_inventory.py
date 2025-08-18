from tests.base import BaseTestCase

class TestInventory(BaseTestCase):
    def test_list_parts(self):
        res = self.client.get("/inventory/")  # trailing slash to avoid 308
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_create_part_success(self):
        r = self.client.post("/inventory/", json={"name": "Brake Pad", "price": 39.99},
                             headers=self.bearer())
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["name"], "Brake Pad")

    def test_create_part_duplicate(self):
        self.client.post("/inventory/", json={"name": "Bulb", "price": 5.0},
                         headers=self.bearer())
        dup = self.client.post("/inventory/", json={"name": "Bulb", "price": 5.0},
                               headers=self.bearer())
        self.assertEqual(dup.status_code, 400)

    def test_get_part_success(self):
        created = self.client.post("/inventory/", json={"name": "Oil Filter", "price": 14.99},
                                   headers=self.bearer()).get_json()
        pid = created["id"]
        got = self.client.get(f"/inventory/{pid}")
        self.assertEqual(got.status_code, 200)
        self.assertEqual(got.get_json()["name"], "Oil Filter")

    def test_get_part_not_found(self):
        res = self.client.get("/inventory/999999")
        self.assertEqual(res.status_code, 404)

    def test_update_part_success(self):
        created = self.client.post("/inventory/", json={"name":"Cap","price":2.5},
                                   headers=self.bearer()).get_json()
        pid = created["id"]
        upd = self.client.put(f"/inventory/{pid}", json={"price": 3.0}, headers=self.bearer())
        self.assertEqual(upd.status_code, 200)
        self.assertEqual(upd.get_json()["price"], 3.0)

    def test_delete_part_success(self):
        created = self.client.post("/inventory/", json={"name":"Fuse","price":1.5},
                                   headers=self.bearer()).get_json()
        pid = created["id"]
        dele = self.client.delete(f"/inventory/{pid}", headers=self.bearer())
        self.assertEqual(dele.status_code, 200)

    def test_delete_part_not_found(self):
        dele = self.client.delete("/inventory/999999", headers=self.bearer())
        self.assertEqual(dele.status_code, 404)
