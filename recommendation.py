import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load cleaned data
df = pd.read_csv("data/processed/cleaned_data.csv")

# Convert Customer ID to int (cleaner indexing)
df["Customer ID"] = df["Customer ID"].astype(int)

# Create user-product matrix
user_product_matrix = df.pivot_table(
    index="Customer ID",
    columns="Description",
    values="Quantity",
    aggfunc="sum",
    fill_value=0
)

# Compute similarity between users
user_similarity = cosine_similarity(user_product_matrix)

# Convert similarity matrix to DataFrame
user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_product_matrix.index,
    columns=user_product_matrix.index
)

# Recommendation function
def recommend_products(customer_id, top_n=5):

    # Get similarity scores for this customer
    similarity_scores = user_similarity_df.loc[customer_id]

    # Sort by similarity (descending)
    similarity_scores = similarity_scores.sort_values(ascending=False)

    # Remove the customer itself (first entry)
    similar_users = similarity_scores.iloc[1:6]

    similar_user_ids = similar_users.index

    # Get products bought by similar users
    similar_user_products = user_product_matrix.loc[similar_user_ids]

    product_scores = similar_user_products.sum().sort_values(ascending=False)

    # Remove already purchased products
    customer_products = user_product_matrix.loc[customer_id]
    already_bought = customer_products[customer_products > 0].index

    recommendations = product_scores.drop(already_bought).head(top_n)

    return recommendations

# Test with first customer
test_customer = user_product_matrix.index[0]

print(f"\nRecommendations for Customer {test_customer}:")
print(recommend_products(test_customer))
