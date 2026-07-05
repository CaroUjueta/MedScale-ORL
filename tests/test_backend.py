import unittest
from fastapi.testclient import TestClient


class TestBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from backend.database.db import Base, engine
        Base.metadata.create_all(bind=engine)

    def test_root_endpoint(self):
        from backend.main import app
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "MedScale-ORL API"})

    def test_register_and_login(self):
        from backend.main import app
        client = TestClient(app)
        response = client.post("/auth/register", json={
            "email": "test@test.com",
            "nombre": "Test",
            "password": "123456",
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

        response = client.post("/auth/login", json={
            "email": "test@test.com",
            "password": "123456",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())


if __name__ == "__main__":
    unittest.main()
