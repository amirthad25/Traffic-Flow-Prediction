import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

def train_model():
    # Paths
    data_path = os.path.join("data", "raw", "traffic.csv")
    model_dir = "model"
    model_path = os.path.join(model_dir, "model.joblib")

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)

    # Features and Target
    features = ["hour", "weekday", "month", "latitude", "longitude"]
    target = "traffic_volume"

    X = df[features]
    y = df[target]

    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    print(f"Saving model to {model_path}...")
    joblib.dump(model, model_path)
    print("Training complete!")

if __name__ == "__main__":
    train_model()
