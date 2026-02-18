import pandas as pd
from prophet import Prophet

# Load data
df = pd.read_csv("data/processed/cleaned_data.csv")

# Monthly aggregation
monthly = (
    df.groupby(["Year", "Month"])["Revenue"]
    .sum()
    .reset_index()
)

# Create proper datetime column
monthly["ds"] = pd.to_datetime(
    monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str)
)

monthly = monthly.sort_values("ds")

# Prophet requires columns: ds (date), y (value)
prophet_df = monthly[["ds", "Revenue"]].rename(columns={"Revenue": "y"})

# Train model
model = Prophet()
model.fit(prophet_df)

# Create future dataframe (predict next 3 months)
future = model.make_future_dataframe(periods=3, freq="M")

forecast = model.predict(future)

# Show last predictions
# Show only future predictions
future_forecast = forecast.tail(3)

print("\n📈 Next 3 Months Revenue Forecast:")
print(future_forecast[["ds", "yhat"]])

# Save forecast to CSV
forecast[['ds', 'yhat']].tail(6).to_csv("data/processed/future_forecast.csv", index=False)

print("Forecast saved successfully!")
