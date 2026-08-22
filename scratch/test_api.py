import requests
import json

def test_api():
    url = "http://127.0.0.1:5000/predict"
    
    # Test Chennai (Urban + Peak)
    print("Testing Chennai (Urban, Peak 9 AM)...")
    payload = {"area": "Chennai Center", "lat": 13.0827, "lon": 80.2707, "hour": 9}
    r = requests.post(url, json=payload)
    print(f"Response: {r.json()['congestion_level']} ({r.json()['traffic_volume']} v/h)")
    
    # Test Rural (10, 77 at 2 PM)
    print("\nTesting Rural Area (10, 77 at 2 PM)...")
    payload = {"area": "Rural Village", "lat": 10.0, "lon": 77.0, "hour": 14}
    r = requests.post(url, json=payload)
    print(f"Response: {r.json()['congestion_level']} ({r.json()['traffic_volume']} v/h)")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"Error: {e}")
