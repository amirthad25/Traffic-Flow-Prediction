import unittest

from api.app import MODEL, app


class TrafficApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_model_is_loaded(self):
        self.assertIsNotNone(MODEL)

    def test_dashboard_preserves_map_and_charts(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.data
        self.assertIn(b'id="map"', html)
        self.assertIn(b"leaflet", html)
        self.assertIn(b"World_Dark_Gray_Base", html)
        self.assertIn(b"new Chart", html)
        self.assertIn(b"setMapTheme", html)
        self.assertIn(b"speechSynthesis", html)

    def test_index_page_is_served(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Traffic Intelligence Hub", response.data)
        self.assertIn(b'id="map"', response.data)

    def test_analytics_returns_chart_data(self):
        response = self.client.get("/analytics")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["labels_hour"]), 24)
        self.assertEqual(len(data["hourly_data"]), 24)
        self.assertEqual(len(data["dist_labels"]), 3)
        self.assertEqual(sum(data["congestion_distribution"]), 100)

    def test_predict_urban_peak_is_heavy(self):
        response = self.client.post(
            "/predict",
            json={
                "area": "Chennai Center",
                "lat": 13.0827,
                "lon": 80.2707,
                "hour": 9,
                "type": "suburb",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(data["traffic_volume"], 5000)
        self.assertEqual(data["predicted_traffic_volume"], data["traffic_volume"])
        self.assertEqual(data["congestion_level"], "Heavy")
        self.assertEqual(data["color"], "Red")
        self.assertIn("what_if", data)
        self.assertIn("new_time", data["what_if"])

    def test_predict_rural_offpeak_is_light(self):
        response = self.client.post(
            "/predict",
            json={
                "area": "Rural Village",
                "lat": 10.0,
                "lon": 77.0,
                "hour": 14,
                "type": "village",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertLess(data["traffic_volume"], 2000)
        self.assertEqual(data["congestion_level"], "Light")
        self.assertEqual(data["color"], "Green")

    def test_predict_non_road_location_is_not_applicable(self):
        response = self.client.post(
            "/predict",
            json={
                "area": "Local Lake",
                "lat": 13.0827,
                "lon": 80.2707,
                "hour": 9,
                "type": "lake",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["traffic"], "Not Applicable")
        self.assertEqual(data["status"], "Not Applicable")
        self.assertNotIn("traffic_volume", data)

    def test_predict_invalid_coordinates_returns_400(self):
        response = self.client.post(
            "/predict",
            json={"lat": "not-a-number", "lon": 80.2707},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_cors_allows_frontend_origin(self):
        response = self.client.get(
            "/analytics",
            headers={"Origin": "http://localhost:3000"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Access-Control-Allow-Origin", response.headers)


if __name__ == "__main__":
    unittest.main()
