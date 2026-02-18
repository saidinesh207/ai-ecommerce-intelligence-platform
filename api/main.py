from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(title="AI E-Commerce Backend")

BASE_PATH = "data/processed"

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def home():
    return {"message": "AI E-Commerce Backend Running 🚀"}


# -----------------------------
# Forecast Endpoint
# -----------------------------
@app.get("/forecast")
def get_forecast():

    forecast_path = os.path.join(BASE_PATH, "future_forecast.csv")

    if not os.path.exists(forecast_path):
        return {"error": "Forecast file not found"}

    forecast_df = pd.read_csv(forecast_path)

    return {
        "future_forecast": forecast_df.to_dict(orient="records")
    }


# -----------------------------
# Recommendation Endpoint
# -----------------------------
@app.get("/recommend/{customer_id}")
def recommend(customer_id: int):

    rec_path = os.path.join(BASE_PATH, "recommendations.csv")

    if not os.path.exists(rec_path):
        return {"error": "Recommendation file not found"}

    rec_df = pd.read_csv(rec_path)

    customer_data = rec_df[rec_df["Customer ID"] == customer_id]

    if customer_data.empty:
        return {"error": "Customer ID not found"}

    return {
        "customer_id": customer_id,
        "recommended_products": list(customer_data["Recommended Product"])
    }
