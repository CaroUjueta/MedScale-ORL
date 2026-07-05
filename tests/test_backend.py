import unittest


class TestBackend(unittest.TestCase):
    def test_root_endpoint(self):
        from backend.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "MedScale-ORL API"})


if __name__ == "__main__":
    unittest.main()
