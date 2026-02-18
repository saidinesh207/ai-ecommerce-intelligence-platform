import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

print("🔄 Loading cleaned dataset...")
df = pd.read_csv("data/processed/cleaned_data.csv")

# Convert Customer ID to int
df["Customer ID"] = df["Customer ID"].astype(int)

print("🔄 Creating user-product matrix...")
user_product_matrix = df.pivot_table(
    index="Customer ID",
    columns="Description",
    values="Quantity",
    aggfunc="sum",
    fill_value=0
)

print("🔄 Calculating user similarity...")
user_similarity = cosine_similarity(user_product_matrix)

user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_product_matrix.index,
    columns=user_product_matrix.index
)

print("🔄 Generating recommendations for all customers...")

recommendations_list = []

for customer_id in user_product_matrix.index:

    similarity_scores = user_similarity_df.loc[customer_id]
    similarity_scores = similarity_scores.sort_values(ascending=False)

    # Top 5 similar users (excluding itself)
    similar_users = similarity_scores.iloc[1:6]
    similar_user_ids = similar_users.index

    similar_user_products = user_product_matrix.loc[similar_user_ids]
    product_scores = similar_user_products.sum().sort_values(ascending=False)

    customer_products = user_product_matrix.loc[customer_id]
    already_bought = customer_products[customer_products > 0].index

    recommended_products = product_scores.drop(already_bought).head(5)

    for product in recommended_products.index:
        recommendations_list.append({
            "Customer ID": customer_id,
            "Recommended Product": product
        })

recommendations_df = pd.DataFrame(recommendations_list)

# Save file for API use
recommendations_df.to_csv("data/processed/recommendations.csv", index=False)

print("✅ recommendations.csv created successfully!")
