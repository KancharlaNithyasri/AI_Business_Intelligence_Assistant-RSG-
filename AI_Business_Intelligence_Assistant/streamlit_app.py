import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 AI Business Intelligence Assistant")
st.write("Ask questions about your sales data using natural language.")

# Backend API
API_URL = "http://127.0.0.1:8000/ask"

# Question input
question = st.text_input(
    "Ask your business question:",
    placeholder="Example: What is the total revenue?"
)

# Ask button
if st.button("Get Answer"):
    if question.strip():

        with st.spinner("Analyzing your question..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()

                    st.subheader("Answer")
                    st.write(data["result"])

                    st.subheader("Question Interpretation")
                    st.json(data["interpretation"])

                else:
                    st.error(f"API Error: {response.status_code}")

            except requests.exceptions.RequestException as error:
                st.error(f"Could not connect to backend: {error}")

    else:
        st.warning("Please enter a question.")

# Example questions
st.divider()
st.subheader("Example Questions")

examples = [
    "What is the total revenue?",
    "Which product generated the highest revenue?",
    "Show monthly revenue trend",
    "Which region has the highest sales?",
    "Compare January and February revenue"
]

for example in examples:
    st.write("• " + example)