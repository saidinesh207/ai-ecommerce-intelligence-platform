import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="AI E-Commerce Platform", layout="wide")

st.title("🛍 AI-Powered E-Commerce Intelligence Platform")

API_BASE_URL = "http://127.0.0.1:8000"

# -----------------------------
# Load Data (only for KPIs)
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/cleaned_data.csv")

df = load_data()

# -----------------------------
# KPI Section
# -----------------------------
total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()
total_customers = df["Customer ID"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"£{total_revenue:,.2f}")
col2.metric("🧾 Total Orders", total_orders)
col3.metric("👥 Total Customers", total_customers)

st.divider()

# -----------------------------
# Forecast Section (API Call)
# -----------------------------
st.subheader("📈 Revenue Forecast (From Backend API)")

if st.button("Get Forecast"):

    response = requests.get(f"{API_BASE_URL}/forecast")

    if response.status_code == 200:
        forecast_data = response.json()["future_forecast"]

        forecast_df = pd.DataFrame(forecast_data)
        forecast_df["ds"] = pd.to_datetime(forecast_df["ds"])

        st.line_chart(
            forecast_df.set_index("ds")["yhat"]
        )
    else:
        st.error("Failed to fetch forecast from API")

st.divider()

# -----------------------------
# Recommendation Section (API Call)
# -----------------------------
st.subheader("🤖 AI Product Recommendation (From Backend API)")

customer_id_input = st.number_input("Enter Customer ID", step=1)

if st.button("Get Recommendations"):

    response = requests.get(
        f"{API_BASE_URL}/recommend/{customer_id_input}"
    )

    if response.status_code == 200:
        data = response.json()

        if "recommended_products" in data:
            st.success("Top 5 Recommended Products:")
            for product in data["recommended_products"]:
                st.write("•", product)
        else:
            st.error("Customer not found.")
    else:
        st.error("Failed to fetch recommendations from API")
