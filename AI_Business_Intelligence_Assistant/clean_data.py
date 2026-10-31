import pandas as pd

# Load original dataset
df = pd.read_csv("data/sales_data.csv")

# Convert order date into datetime
df["Order_date"] = pd.to_datetime(
    df["Order_date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# Remove invalid records
cleaned_df = df[
    (df["Status"] == "Completed") &
    (df["Quantity"] > 0) &
    (df["Unit_price"].notna()) &
    (df["Unit_price"] >= 0) &
    (df["Discount_amount"] >= 0) &
    (df["Order_date"].notna())
].copy()

# Calculate revenue
cleaned_df["Revenue"] = (
    cleaned_df["Quantity"] * cleaned_df["Unit_price"]
    - cleaned_df["Discount_amount"]
)

# Display results
print("Original records:", len(df))
print("Cleaned records:", len(cleaned_df))
print("Excluded records:", len(df) - len(cleaned_df))

print("\nTOTAL REVENUE:")
print(cleaned_df["Revenue"].sum())

print("\nCLEANED DATA:")
print(cleaned_df.head())

# Save cleaned dataset
cleaned_df.to_csv("data/cleaned_sales_data.csv", index=False)

print("\nCleaned dataset saved successfully!")