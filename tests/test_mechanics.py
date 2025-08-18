import unittest
from tests.base import BaseTestCase

class TestMechanics(BaseTestCase):
    def test_leaderboard_empty(self):
        res = self.client.get("/mechanics/leaderboard")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_leaderboard_with_limit(self):
        res = self.client.get("/mechanics/leaderboard?limit=1")
        self.assertEqual(res.status_code, 200)
        self.assertLessEqual(len(res.get_json()), 1)

    def test_leaderboard_returns_list(self):
        res = self.client.get("/mechanics/leaderboard")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

if __name__ == "__main__":
    unittest.main()
