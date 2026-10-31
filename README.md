
# AI Business Intelligence Assistant

## 1. Project Overview

The AI Business Intelligence Assistant is a mini application that answers business questions using sales data.

It allows users to ask questions in natural language and receive answers with supporting figures. The application uses Python, SQLite, FastAPI, Streamlit, and Google Gemini.

## 2. Features

- Load and clean sales data from a CSV file.
- Store cleaned data in an SQLite database.
- Calculate total revenue.
- Identify the highest-revenue product.
- Display monthly revenue trends.
- Identify the highest-sales region.
- Compare revenue between two months.
- Accept natural-language questions through a web interface.
- Use Gemini as a fallback for interpreting unsupported question formats.
- Validate interpreted intents before executing analytics.

## 3. Technologies Used

- Python
- Pandas
- SQLite
- FastAPI
- Streamlit
- Google Gemini API
- Pytest

## 4. Architecture

```text
User
  |
  v
Streamlit User Interface
  |
  v
FastAPI Backend
  |
  v
Question Interpreter
  |
  +---- Rule-based interpretation
  |
  +---- Gemini fallback
  |
  v
Validated Analytics Intent
  |
  v
Predefined SQL Queries
  |
  v
SQLite Database
  |
  v
Structured Answer
```

## 5. Project Structure

```text
AI_Business_Intelligence_Assistant/
|
|-- data/
|   |-- sales_data.csv
|   |-- cleaned_sales_data.csv
|
|-- inspect_data.py
|-- clean_data.py
|-- create_database.py
|-- analytics.py
|-- interpreter.py
|-- main.py
|-- streamlit_app.py
|-- test_gemini.py
|-- test_app.py
|-- requirements.txt
|-- README.md
|-- AI_DEVELOPMENT_NOTES.md
|-- .gitignore
```

The SQLite database `sales.db` is generated locally by the database creation script.

## 6. Installation and Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## 7. Prepare the Database

Run the following commands:

```bash
python clean_data.py
python create_database.py
```

These scripts clean the original sales data and create the SQLite database.

## 8. Configure Gemini API

Set your Gemini API key as an environment variable in PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Do not store your actual API key in the source code or GitHub repository.

## 9. Run the Application

Start the FastAPI backend:

```bash
uvicorn main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

Open another terminal and start the Streamlit frontend:

```bash
streamlit run streamlit_app.py
```

Open:

http://localhost:8501

## 10. Example Questions

- What is the total revenue?
- Which product generated the highest revenue?
- Show monthly revenue trends.
- Which region has the highest sales?
- Compare January and February revenue.

## 11. Sample Results

| Analysis | Result |
|---|---:|
| Total revenue | ₹14,39,200 |
| Highest revenue product | Monitor |
| Monitor revenue | ₹4,73,000 |
| Highest-sales region | South |
| South region revenue | ₹4,11,200 |
| January revenue | ₹2,10,250 |
| February revenue | ₹2,34,600 |
| Revenue increase (Jan to Feb) | ₹24,350 |

## 12. Data Cleaning

The original dataset contained 51 records.

After data validation and cleaning, 48 records were retained. Three records were excluded because of invalid or missing values and transaction status.

The cleaned records were stored in an SQLite database.

## 13. AI and Query Safety

The application uses rule-based question interpretation for supported analytics questions and Gemini as a fallback interpreter.

The interpreted intent is checked against an allowed list. Analytics are executed using predefined SQL queries rather than allowing the AI model to generate and execute arbitrary SQL.

This helps prevent unsupported requests and destructive database operations.

## 14. Testing

Run automated tests using:

```bash
pytest -v test_app.py
```

The project includes tests for API endpoints, analytics questions, month comparisons, and unsupported questions.

## 15. Known Limitations

- The application supports a limited set of predefined analytics questions.
- More complex natural-language questions may not be recognized.
- Gemini fallback interpretation depends on API availability and network connectivity.
- The application currently runs locally and is not deployed to a cloud platform.
- The user interface provides basic question-and-answer functionality.

## 16. Future Enhancements

- Add interactive charts and visualizations.
- Support more business questions.
- Improve natural-language understanding.
- Add additional datasets and analytics.
- Deploy the application to a cloud platform.

## 17. Author

Developed as part of the AI-Assisted Development Challenge for GET Selection.
