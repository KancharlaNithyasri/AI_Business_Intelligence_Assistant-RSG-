import os
from google import genai

# Get API key from Windows environment variable
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found!")
else:
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="""
        Identify the business question intent.

        Question: Which product generated the highest revenue?

        Return only JSON:
        {"intent": "top_product"}
        """
    )

    print("Gemini response:")
    print(response.text)