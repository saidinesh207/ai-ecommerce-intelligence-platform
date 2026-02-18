from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="AI E-Commerce Backend")

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
    forecast_df = pd.read_csv("data/processed/future_forecast.csv")
    return {
        "future_forecast": forecast_df.to_dict(orient="records")
    }


# -----------------------------
# Recommendation Endpoint
# -----------------------------
@app.get("/recommend/{customer_id}")
def recommend(customer_id: int):

    # Load precomputed recommendation file
    try:
        rec_df = pd.read_csv("data/processed/recommendations.csv")
    except:
        return {"error": "Recommendation file not found"}

    customer_data = rec_df[rec_df["Customer ID"] == customer_id]

    if customer_data.empty:
        return {"error": "Customer ID not found"}

    products = customer_data["Recommended Product"].tolist()

    return {
        "customer_id": customer_id,
        "recommended_products": products
    }
