from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(title="AI-Powered E-Commerce Intelligence Platform")

BASE_PATH = "data/processed"

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def home():
    return {
        "project": "AI-Powered E-Commerce Intelligence Platform",
        "description": "This system provides revenue forecasting and personalized product recommendations using AI.",
        "available_endpoints": {
            "Forecast": "/forecast",
            "Recommendation": "/recommend/{customer_id}",
            "API Docs": "/docs"
        },
        "status": "Running"
    }


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