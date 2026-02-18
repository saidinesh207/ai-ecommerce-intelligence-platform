import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_data.csv")

print("Dataset Shape:", df.shape)

# Total Revenue
total_revenue = df["Revenue"].sum()
print("\nTotal Revenue:", round(total_revenue, 2))

# Revenue by Year
revenue_by_year = df.groupby("Year")["Revenue"].sum()
print("\nRevenue by Year:")
print(revenue_by_year)

# Top 5 Products by Revenue
top_products = df.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(5)

print("\nTop 5 Products by Revenue:")
print(top_products)
# Monthly Revenue Trend
monthly_revenue = df.groupby(["Year", "Month"])["Revenue"].sum().reset_index()

print("\nMonthly Revenue Sample:")
print(monthly_revenue.head())

# Top 5 Customers by Revenue
top_customers = df.groupby("Customer ID")["Revenue"].sum().sort_values(ascending=False).head(5)

print("\nTop 5 Customers by Revenue:")
print(top_customers)
