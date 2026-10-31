import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from interpreter import interpret_question

app = FastAPI(title="AI Business Intelligence Assistant")

DATABASE = "data/sales.db"


class QuestionRequest(BaseModel):
    question: str


def execute_analytics(intent, months=None):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        if intent == "total_revenue":
            cursor.execute("""
                SELECT SUM(Revenue) FROM sales
            """)
            result = cursor.fetchone()[0]

            return {
                "answer": "Total revenue",
                "value": result,
                "unit": "INR"
            }

        elif intent == "top_product":
            cursor.execute("""
                SELECT Product, SUM(Revenue) AS revenue
                FROM sales
                GROUP BY Product
                ORDER BY revenue DESC
                LIMIT 1
            """)
            result = cursor.fetchone()

            return {
                "answer": "Product with highest revenue",
                "product": result[0],
                "revenue": result[1],
                "unit": "INR"
            }

        elif intent == "monthly_trend":
            cursor.execute("""
                SELECT strftime('%Y-%m', Order_date),
                       SUM(Revenue)
                FROM sales
                GROUP BY strftime('%Y-%m', Order_date)
                ORDER BY strftime('%Y-%m', Order_date)
            """)
            rows = cursor.fetchall()

            return {
                "answer": "Monthly revenue trend",
                "data": [
                    {"month": row[0], "revenue": row[1]}
                    for row in rows
                ]
            }

        elif intent == "top_region":
            cursor.execute("""
                SELECT Region, SUM(Revenue) AS revenue
                FROM sales
                GROUP BY Region
                ORDER BY revenue DESC
                LIMIT 1
            """)
            result = cursor.fetchone()

            return {
                "answer": "Region with highest sales",
                "region": result[0],
                "revenue": result[1],
                "unit": "INR"
            }

        elif intent == "compare_months":
            if not months or len(months) != 2:
                return {"error": "Please provide two valid months."}

            values = []

            for month in months:
                cursor.execute("""
                    SELECT SUM(Revenue)
                    FROM sales
                    WHERE strftime('%Y-%m', Order_date) = ?
                """, (month,))
                values.append(cursor.fetchone()[0] or 0)

            difference = values[1] - values[0]

            return {
                "answer": "Revenue comparison",
                "month_1": months[0],
                "revenue_1": values[0],
                "month_2": months[1],
                "revenue_2": values[1],
                "difference": difference,
                "trend": "Increased" if difference > 0
                         else "Decreased" if difference < 0
                         else "No change"
            }

        return {"error": "Unsupported business question."}

    finally:
        connection.close()


@app.get("/")
def home():
    return {
        "message": "AI Business Intelligence Assistant is running!"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    interpretation = interpret_question(request.question)

    result = execute_analytics(
        interpretation["intent"],
        interpretation.get("months")
    )

    return {
        "question": request.question,
        "interpretation": interpretation,
        "result": result
    }