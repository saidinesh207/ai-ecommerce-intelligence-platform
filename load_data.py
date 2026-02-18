import pandas as pd

file_path = "data/raw/online_retail_II.xlsx"
df = pd.read_excel(file_path)

print("Original Shape:", df.shape)

# 1️⃣ Remove rows with missing Customer ID
df = df.dropna(subset=["Customer ID"])

# 2️⃣ Remove negative or zero Quantity
df = df[df["Quantity"] > 0]

# 3️⃣ Remove negative or zero Price
df = df[df["Price"] > 0]

print("Cleaned Shape:", df.shape)

print("\nMin Quantity:", df["Quantity"].min())
print("Min Price:", df["Price"].min())
# 4️⃣ Create Revenue column
df["Revenue"] = df["Quantity"] * df["Price"]

print("\nRevenue Column Created")
print("Min Revenue:", df["Revenue"].min())
print("Max Revenue:", df["Revenue"].max())
# 5️⃣ Extract Date Features
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Day"] = df["InvoiceDate"].dt.day
df["Hour"] = df["InvoiceDate"].dt.hour

print("\nDate Features Added")
print(df[["InvoiceDate", "Year", "Month", "Day", "Hour"]].head())
# Save cleaned dataset
df.to_csv("data/processed/cleaned_data.csv", index=False)

print("\n✅ Cleaned dataset saved successfully!")
