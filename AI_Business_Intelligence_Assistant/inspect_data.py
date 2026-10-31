import pandas as pd

df = pd.read_csv("data/sales_data.csv")

print("DUPLICATE TRANSACTIONS:")
print(df["Transaction_Id"].duplicated().sum())

print("\nORDER STATUS:")
print(df["Status"].value_counts())

print("\nINVALID QUANTITIES:")
print(df[df["Quantity"] <= 0])

print("\nMISSING UNIT PRICES:")
print(df[df["Unit_price"].isnull()])

print("\nINVALID UNIT PRICES:")
print(df[df["Unit_price"] <= 0])

print("\nINVALID DISCOUNTS:")
print(df[df["Discount_amount"] < 0])

print("\nINVALID DATES:")
dates = pd.to_datetime(
    df["Order_date"],
    format="%d-%m-%Y",
    errors="coerce"
)
print(df[dates.isnull()])