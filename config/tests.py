from django.test import Client, SimpleTestCase


class CoreApiTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_health(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_info(self):
        response = self.client.get("/api/info/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "SBM-API")

    def test_api_root(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("health", response.json())
