import sqlite3

connection = sqlite3.connect("data/sales.db")
cursor = connection.cursor()

# 1. Total Revenue
cursor.execute("SELECT SUM(Revenue) FROM sales")
print("Total Revenue:", cursor.fetchone()[0])

# 2. Product with Highest Revenue
cursor.execute("""
    SELECT Product, SUM(Revenue) AS total_revenue
    FROM sales
    GROUP BY Product
    ORDER BY total_revenue DESC
    LIMIT 1
""")
print("\nTop Product:", cursor.fetchone())

# 3. Monthly Revenue Trend
cursor.execute("""
    SELECT strftime('%Y-%m', Order_date), SUM(Revenue)
    FROM sales
    GROUP BY strftime('%Y-%m', Order_date)
    ORDER BY strftime('%Y-%m', Order_date)
""")
print("\nMonthly Revenue:")
for row in cursor.fetchall():
    print(row)

# 4. Region with Highest Revenue
cursor.execute("""
    SELECT Region, SUM(Revenue) AS total_revenue
    FROM sales
    GROUP BY Region
    ORDER BY total_revenue DESC
    LIMIT 1
""")
print("\nTop Region:", cursor.fetchone())

# 5. Compare revenue between two months

month1 = "2026-01"
month2 = "2026-02"

cursor.execute("""
    SELECT SUM(Revenue)
    FROM sales
    WHERE strftime('%Y-%m', Order_date) = ?
""", (month1,))
revenue1 = cursor.fetchone()[0] or 0

cursor.execute("""
    SELECT SUM(Revenue)
    FROM sales
    WHERE strftime('%Y-%m', Order_date) = ?
""", (month2,))
revenue2 = cursor.fetchone()[0] or 0

difference = revenue2 - revenue1

print("\nMONTH COMPARISON:")
print(month1, ":", revenue1)
print(month2, ":", revenue2)
print("Revenue change:", difference)

if difference > 0:
    print("Revenue increased.")
elif difference < 0:
    print("Revenue decreased.")
else:
    print("Revenue remained the same.")

connection.close()