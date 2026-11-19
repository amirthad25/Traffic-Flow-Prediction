import os
import unittest


class FrontendContractTests(unittest.TestCase):
    def setUp(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.frontend_path = os.path.join(project_root, "frontend", "index.html")

    def test_frontend_file_exists(self):
        self.assertTrue(os.path.exists(self.frontend_path))

    def test_original_frontend_contract_is_supported(self):
        with open(self.frontend_path, encoding="utf-8") as fh:
            html = fh.read()
        self.assertIn("data.predicted_traffic_volume", html)
        self.assertIn("http://127.0.0.1:5000/predict", html)

    def test_frontend_targets_backend_api(self):
        with open(self.frontend_path, encoding="utf-8") as fh:
            html = fh.read()
        self.assertIn("http://127.0.0.1:5000", html)
        self.assertIn("/predict", html)


if __name__ == "__main__":
    unittest.main()
