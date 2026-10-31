# AI Development Notes

## 1. Tools and Technologies Used

- Python 3.12
- PyCharm IDE
- Pandas for data cleaning and processing
- SQLite for database storage
- FastAPI for backend API development
- Streamlit for the user interface
- Google Gemini API for AI-assisted question interpretation
- Pytest for automated testing
- ChatGPT for development guidance and debugging support

## 2. How AI Was Used

Google Gemini was integrated to assist with interpreting natural-language questions.

The application uses a rule-based interpreter first for the five supported analytics questions. This provides faster and more predictable responses.

When the rule-based interpreter cannot recognize a question, Gemini is used as a fallback. Its response is parsed and checked against the application's allowed intent list.

The application does not allow the LLM to generate or execute SQL queries. Instead, it uses predefined SQL queries for the supported analytics operations.

ChatGPT was also used as a development assistant to understand concepts, troubleshoot errors, and improve the implementation.

## 3. Challenges and Debugging

- Faced temporary Gemini API availability errors during testing.
- Changed the model configuration and successfully tested the Gemini integration.
- Experienced slow responses when the Gemini API was called for every question.
- Improved response time by checking supported questions with the rule-based interpreter first.
- Tested API endpoints through FastAPI Swagger documentation.
- Verified the frontend and backend integration.
- Used automated tests to identify and verify application behavior.

## 4. Data Cleaning

The original dataset contained 51 records. Data validation identified returned transactions, an invalid quantity, and a missing unit price.

After applying the cleaning rules, 48 valid completed transactions were retained for analysis.

## 5. Testing

Seven automated tests were executed successfully.

The tests covered:
- Home endpoint
- Health endpoint
- Total revenue
- Highest revenue product
- Highest sales region
- Monthly revenue comparison
- Unsupported questions

Result: **7 tests passed.**

## 6. Future Improvements

- Add interactive charts for monthly sales trends.
- Improve natural-language understanding for more question formats.
- Support custom date ranges and additional analytics questions.
- Add more edge-case and integration tests.
- Improve error handling and user interface design.
- Add caching for AI interpretation where appropriate.
- Support deployment using Docker and a cloud platform.
