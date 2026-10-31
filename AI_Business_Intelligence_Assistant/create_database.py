import pandas as pd
import sqlite3

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales_data.csv")

# Connect to SQLite database
connection = sqlite3.connect("data/sales.db")

# Store data in a database table
df.to_sql("sales", connection, if_exists="replace", index=False)

# Check total records stored
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM sales")
count = cursor.fetchone()[0]

print("Database created successfully!")
print("Records stored:", count)

# Display first 5 records
cursor.execute("SELECT * FROM sales LIMIT 5")

for row in cursor.fetchall():
    print(row)

connection.close()