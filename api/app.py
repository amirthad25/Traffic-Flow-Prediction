from flask import Flask, jsonify, request, render_template
import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__, template_folder="templates")

# Global variable for model
MODEL = None

def load_model():
    global MODEL
    model_path = os.path.join("model", "model.joblib")
    if os.path.exists(model_path):
        MODEL = joblib.load(model_path)
        print("Model loaded successfully from joblib.")
    else:
        print("Model file not found. Prediction will use fallback logic.")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        area = data.get('area', 'Selected Location')
        lat = float(data.get('lat', 13.0827))
        lon = float(data.get('lon', 80.2707))
        location_type = data.get('type', '').lower()

        # --- Part 3: Fix Lake / Non-Road Issue ---
        water_types = ['water', 'lake', 'river', 'reservoir', 'basin', 'canal', 'nature_reserve', 'forest']
        if location_type in water_types:
            return jsonify({
                "traffic": "Not Applicable",
                "message": "No traffic data available for this location (non-road area)",
                "error": "No traffic data (non-road area)", # Keep for compatibility
                "status": "Not Applicable"
            })
        
        # Get current time features
        now = datetime.now()
        hour = int(data.get('hour', now.hour))
        weekday = now.weekday()
        month = now.month

        # --- Base Prediction ---
        if MODEL:
            # Prepare features for model
            features = np.array([[hour, weekday, month, lat, lon]])
            raw_prediction = MODEL.predict(features)
            base_volume = float(raw_prediction[0])
            
            # --- Part 1: Debug the Model Output (MANDATORY) ---
            print("--- DEBUG LOG START ---")
            print("Input Features:", features)
            print("Raw Prediction:", raw_prediction)
            if hasattr(MODEL, 'predict_proba'):
                print("Prediction Probabilities:", MODEL.predict_proba(features))
            else:
                print("Prediction Probabilities: N/A (Regressor Model)")
            print("--- DEBUG LOG END ---")
        else:
            # Fallback simulation (Dynamic based on time/location)
            base_volume = 1500 + np.random.randint(-200, 200)

        # --- Intelligence Layer (Manual Adjustments) ---
        
        # 1. Peak Hour Adjustment (Rush Hour)
        is_peak = (7 <= hour <= 10) or (17 <= hour <= 20)
        peak_adjustment = 2000 if is_peak else 0
        
        # 2. Location-Based Variation (Urban vs Rural)
        # Chennai center approx: 13.08, 80.27
        dist_to_chennai = np.sqrt((lat - 13.08)**2 + (lon - 80.27)**2)
        
        location_adjustment = 0
        area_type = "Rural"
        if dist_to_chennai < 0.2: # Near city center
            location_adjustment = 1500
            area_type = "Urban (Chennai Core)"
        elif dist_to_chennai < 0.5: # Suburban
            location_adjustment = 700
            area_type = "Semi-Urban"
        else:
            location_adjustment = -300 # Rural/Outside
            area_type = "Rural / Small Town"

        # Final Volume Calculation
        traffic_volume = int(base_volume + peak_adjustment + location_adjustment)
        
        # --- Part 1: Fix Traffic Always Heavy (Balancing Logic) ---
        if not is_peak:
            traffic_volume = int(traffic_volume * 0.6) # Deeper reduction for variety
        
        # Add controlled noise for variety (+/- 5%)
        noise = np.random.randint(-int(traffic_volume * 0.05), int(traffic_volume * 0.05))
        traffic_volume += noise
            
        traffic_volume = max(500, traffic_volume) # Minimum floor

        print(f"LOG: Area: {area} | Lat: {lat:.4f}, Lon: {lon:.4f} | Type: {area_type} | Hour: {hour} | Volume: {traffic_volume}")

        # --- Part 2: Force Balanced Traffic Classification (CRITICAL FIX) ---
        # vehicle_density is represented by our final traffic_volume
        if traffic_volume < 2000:
            level = "Light"
            color = "Green"
            explanation = f"Traffic is light. Clear roads in this {area_type} location."
            suggestion = "Optimal travel conditions. Enjoy your ride!"
        elif 2000 <= traffic_volume < 5000:
            level = "Moderate"
            color = "Yellow"
            explanation = f"Traffic is moderate. Standard {area_type} flow observed."
            suggestion = "Alternative routes might save a few minutes."
        else: # >= 5000
            level = "Heavy"
            color = "Red"
            explanation = f"Traffic is heavy in {area} due to high vehicle density in this {area_type} area."
            suggestion = f"Expect delays. Consider traveling after { (hour + 2) % 24 }:00."

        # Confidence & Risk
        confidence = 85 if MODEL else 60
        risk = "High" if is_peak and traffic_volume > 4000 else "Low"
        
        factors = [f"Location: {area_type}"]
        if is_peak: factors.append("Peak Hour Surge")
        if dist_to_chennai < 0.3: factors.append("High Population Density")

        # What-If (Simplified)
        future_hour = (hour + 2) % 24
        future_is_peak = (7 <= future_hour <= 10) or (17 <= future_hour <= 20)
        future_vol = base_volume + (2000 if future_is_peak else 0) + location_adjustment
        change_pct = int(((future_vol - traffic_volume) / traffic_volume) * 100)

        return jsonify({
            "area": area,
            "traffic_volume": traffic_volume,
            "congestion_level": level,
            "color": color,
            "explanation": explanation,
            "suggestion": suggestion,
            "confidence": confidence,
            "risk": risk,
            "factors": factors,
            "what_if": {
                "new_time": f"{future_hour % 12 or 12} {'PM' if future_hour >= 12 else 'AM'}",
                "traffic": int(future_vol),
                "change_percent": change_pct
            }
        })

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route("/analytics", methods=["GET"])
def analytics():
    hours = list(range(24))
    volumes = []
    for h in hours:
        vol = 800
        if 7 <= h <= 10: vol = 3500 + (h * 50)
        elif 16 <= h <= 20: vol = 4200 - (h * 20)
        volumes.append(vol)

    return jsonify({
        "labels_hour": hours,
        "hourly_data": volumes,
        "congestion_distribution": [20, 40, 40],
        "dist_labels": ["Low", "Moderate", "Heavy"]
    })

load_model()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
