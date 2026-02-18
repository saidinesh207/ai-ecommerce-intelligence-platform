from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from prophet import Prophet

app = FastAPI(title="AI E-Commerce Backend")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/processed/cleaned_data.csv")
df["Customer ID"] = df["Customer ID"].astype(int)

# -----------------------------
# Build Recommendation System
# -----------------------------
user_product_matrix = df.pivot_table(
    index="Customer ID",
    columns="Description",
    values="Quantity",
    aggfunc="sum",
    fill_value=0
)

user_similarity = cosine_similarity(user_product_matrix)
user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_product_matrix.index,
    columns=user_product_matrix.index
)

# -----------------------------
# Forecast Model Setup
# -----------------------------
monthly = (
    df.groupby(["Year", "Month"])["Revenue"]
    .sum()
    .reset_index()
)

monthly["ds"] = pd.to_datetime(
    monthly["Year"].astype(str) + "-" +
    monthly["Month"].astype(str)
)

prophet_df = monthly[["ds", "Revenue"]].rename(columns={"Revenue": "y"})

forecast_model = Prophet()
forecast_model.fit(prophet_df)


# -----------------------------
# API Endpoints
# -----------------------------

@app.get("/")
def home():
    return {"message": "AI E-Commerce Backend Running 🚀"}


@app.get("/recommend/{customer_id}")
def recommend(customer_id: int):

    if customer_id not in user_product_matrix.index:
        return {"error": "Customer ID not found"}

    similarity_scores = user_similarity_df.loc[customer_id]
    similarity_scores = similarity_scores.sort_values(ascending=False)

    similar_users = similarity_scores.iloc[1:6]
    similar_user_ids = similar_users.index

    similar_user_products = user_product_matrix.loc[similar_user_ids]
    product_scores = similar_user_products.sum().sort_values(ascending=False)

    customer_products = user_product_matrix.loc[customer_id]
    already_bought = customer_products[customer_products > 0].index

    recommendations = product_scores.drop(already_bought).head(5)

    return {
        "customer_id": customer_id,
        "recommended_products": list(recommendations.index)
    }


@app.get("/forecast")
def get_forecast():
    forecast_df = pd.read_csv("data/processed/future_forecast.csv")
    return {
        "future_forecast": forecast_df.to_dict(orient="records")
    }
