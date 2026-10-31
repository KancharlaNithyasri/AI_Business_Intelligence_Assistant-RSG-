import os
import json
import re
from google import genai

MONTHS = {
    "january": "2026-01",
    "february": "2026-02",
    "march": "2026-03",
    "april": "2026-04",
    "may": "2026-05",
    "june": "2026-06"
}

ALLOWED_INTENTS = {
    "total_revenue",
    "top_product",
    "monthly_trend",
    "top_region",
    "compare_months",
    "unsupported"
}


def rule_based_interpreter(question):
    q = question.lower()

    if any(word in q for word in ["compare", "difference", "change"]):
        months = re.findall(
            r"january|february|march|april|may|june", q
        )
        if len(months) >= 2:
            return {
                "intent": "compare_months",
                "months": [MONTHS[m] for m in months[:2]]
            }

    if any(word in q for word in ["total revenue", "overall revenue", "total sales"]):
        return {"intent": "total_revenue"}

    if any(word in q for word in [
        "top product",
        "best product",
        "highest product",
        "which product",
        "generated the highest",
        "highest revenue"
    ]):
        return {"intent": "top_product"}

    if any(word in q for word in ["monthly", "month-wise", "trend"]):
        return {"intent": "monthly_trend"}

    if any(word in q for word in ["region", "area", "location"]):
        return {"intent": "top_region"}

    return {"intent": "unsupported"}


def interpret_question(question):
    fallback = rule_based_interpreter(question)

    # Use the fast rule-based result for recognized questions
    if fallback["intent"] != "unsupported":
        return fallback
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return rule_based_interpreter(question)

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"""
            Identify the intent of this business analytics question.

            Allowed intents:
            total_revenue, top_product, monthly_trend,
            top_region, compare_months, unsupported.

            If comparing months, return their names in a months list.
            Return only valid JSON.

            Question: {question}

            Example:
            {{"intent": "top_product"}}
            """
        )

        result = json.loads(response.text)

        if result["intent"] == "unsupported":
            return rule_based_interpreter(question)


        if result["intent"] == "compare_months":
            months = result.get("months", [])
            if len(months) < 2:
                return rule_based_interpreter(question)

            normalized = []
            for month in months[:2]:
                month = str(month).lower()
                if month not in MONTHS:
                    return rule_based_interpreter(question)
                normalized.append(MONTHS[month])

            result["months"] = normalized

        return result

    except Exception:
        return rule_based_interpreter(question)

if __name__ == "__main__":
    questions = [
        "What is the total revenue?",
        "Which product generated the highest revenue?",
        "Show monthly revenue trend",
        "Which region has highest sales?",
        "Compare January and February revenue"
    ]

    for question in questions:
        print(question)
        print(interpret_question(question))
        print()