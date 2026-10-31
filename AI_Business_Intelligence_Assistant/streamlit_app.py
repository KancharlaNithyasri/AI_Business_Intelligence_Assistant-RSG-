
import streamlit as st
import requests
import pandas as pd

# ======================================================
# CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Sales Intelligence | Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000/ask"

# Snapshot of the current project dataset
MONTHLY_DATA = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [210250, 234600, 223900, 240700, 318500, 211250]
}

TOTAL_REVENUE = 1439200
TOP_PRODUCT = "Monitor"
TOP_PRODUCT_REVENUE = 473000
TOP_REGION = "South"
TOP_REGION_REVENUE = 411200

# ======================================================
# SESSION STATE
# ======================================================

defaults = {
    "question_input": "",
    "answer_data": None,
    "api_error": None,
    "submit_question": False,
    "last_question": "",
    "history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def select_example(question):
    st.session_state.question_input = question
    st.session_state.submit_question = True
    st.session_state.api_error = None


def clear_results():
    st.session_state.question_input = ""
    st.session_state.answer_data = None
    st.session_state.api_error = None
    st.session_state.submit_question = False
    st.session_state.last_question = ""


# ======================================================
# ANSWER FORMATTING
# ======================================================

def money(value):
    try:
        return f"₹{float(value):,.0f}"
    except (ValueError, TypeError):
        return str(value)


def humanize(value):
    return str(value).replace("_", " ").replace("-", " ").strip().capitalize()


def natural_language_answer(result):

    if result is None:
        return "The analysis did not return a result. Please try again."

    if isinstance(result, str):
        return result

    if isinstance(result, (int, float)):
        return f"The calculated result is **{format(result, ',')}**."

    if isinstance(result, list):

        if not result:
            return "No matching records were found."

        lines = []

        for item in result:
            if isinstance(item, dict):
                lines.append(
                    " · ".join(
                        f"{humanize(k)}: {v}"
                        for k, v in item.items()
                    )
                )
            else:
                lines.append(str(item))

        return "\n\n".join(f"- {line}" for line in lines)

    if isinstance(result, dict):

        answer = result.get("answer")
        value = result.get("value")
        unit = result.get("unit", "")

        if answer is not None and value is not None:

            formatted = f"{unit} {value:,.0f}" if (
                isinstance(value, (int, float)) and unit
            ) else f"{unit} {value}" if unit else (
                f"{value:,.0f}" if isinstance(value, (int, float))
                else str(value)
            )

            if "total revenue" in str(answer).lower():
                return f"The total revenue generated is **{formatted}**."

            return f"{answer}: **{formatted}**."

        if "product" in result and "revenue" in result:
            return (
                f"**{result['product']}** is the highest-revenue product, "
                f"generating **{money(result['revenue'])}**."
            )

        if "region" in result and "revenue" in result:
            return (
                f"**{result['region']}** is the leading sales region, "
                f"with revenue of **{money(result['revenue'])}**."
            )

        if "difference" in result:
            difference = result["difference"]

            if isinstance(difference, (int, float)):
                direction = "increase" if difference >= 0 else "decrease"
                return (
                    f"The comparison shows a revenue **{direction} "
                    f"of {money(abs(difference))}**."
                )

        lines = []

        for key, value in result.items():

            if isinstance(value, list):
                lines.append(f"**{humanize(key)}**")
                for item in value:
                    if isinstance(item, dict):
                        details = ", ".join(
                            f"{humanize(k)}: {v}"
                            for k, v in item.items()
                        )
                        lines.append(f"- {details}")
                    else:
                        lines.append(f"- {item}")

            elif isinstance(value, dict):
                details = ", ".join(
                    f"{humanize(k)}: {v}"
                    for k, v in value.items()
                )
                lines.append(f"**{humanize(key)}:** {details}")

            else:
                lines.append(f"**{humanize(key)}:** {value}")

        return "\n\n".join(lines)

    return str(result)


def explain_intent(interpretation):

    if not isinstance(interpretation, dict):
        return "Your question was processed by the business analytics assistant."

    explanations = {
        "total_revenue": "Calculating the total revenue from the sales data.",
        "top_product": "Identifying the product with the highest revenue.",
        "monthly_trend": "Examining revenue performance across months.",
        "top_region": "Finding the region with the highest sales.",
        "compare_months": "Comparing revenue between the selected months.",
        "unsupported": "The question could not be matched to a supported analysis."
    }

    return explanations.get(
        interpretation.get("intent"),
        "Your question was interpreted and processed."
    )


# ======================================================
# PROFESSIONAL DESIGN SYSTEM
# ======================================================

st.markdown("""
<style>

:root {
    --navy: #142D4E;
    --blue: #2864AE;
    --blue-light: #EDF4FC;
    --text: #24364B;
    --muted: #8391A4;
    --border: #E7ECF2;
    --surface: #FFFFFF;
}

.stApp {
    background: #F5F7FA;
    color: var(--text);
}

.block-container {
    max-width: 1500px;
    padding: 2rem 2.5rem 3rem;
}

header[data-testid="stHeader"] {
    background: rgba(245,247,250,0.9);
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

/* Branding */

.brand {
    font-size: 21px;
    font-weight: 800;
    color: var(--navy);
    letter-spacing: -0.5px;
}

.brand-sub {
    font-size: 9px;
    font-weight: 700;
    color: var(--muted);
    letter-spacing: 2px;
    margin-top: 3px;
}

/* Header */

.eyebrow {
    color: var(--blue);
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 1.8px;
    margin-bottom: 9px;
}

.page-title {
    color: var(--navy);
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0;
}

.page-subtitle {
    color: var(--muted);
    font-size: 13px;
    margin-top: 7px;
}

/* Hero */

.hero {
    background: linear-gradient(115deg, #15365F 0%, #2868AE 100%);
    border-radius: 15px;
    padding: 29px 32px;
    margin: 24px 0 26px;
    color: white;
    box-shadow: 0 8px 22px rgba(30,70,120,0.12);
}

.hero-tag {
    color: #C9DCF3;
    font-size: 10px;
    letter-spacing: 1.6px;
    font-weight: 700;
}

.hero h2 {
    color: #FFFFFF;
    font-size: 24px;
    margin: 10px 0 8px;
    font-weight: 750;
}

.hero p {
    color: #D8E6F6;
    font-size: 13px;
    max-width: 680px;
    line-height: 1.7;
    margin-bottom: 0;
}

/* Sections */

.section-heading {
    color: var(--navy);
    font-size: 18px;
    font-weight: 750;
    margin-top: 24px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 15px;
}

/* Metrics */

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    padding: 19px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(30,50,80,0.025);
}

div[data-testid="stMetricLabel"] {
    color: #77869B;
    font-size: 12px;
}

div[data-testid="stMetricValue"] {
    color: var(--navy);
    font-size: 23px;
    font-weight: 750;
}

/* Assistant */

.assistant-header {
    color: var(--navy);
    font-size: 20px;
    font-weight: 750;
}

.assistant-description {
    color: var(--muted);
    font-size: 12px;
    margin-top: 5px;
    margin-bottom: 18px;
}

/* Inputs */

.stTextInput input {
    background: white !important;
    color: var(--text) !important;
    border: 1px solid #D9E2ED !important;
    border-radius: 9px !important;
    min-height: 47px;
}

.stTextInput input:focus {
    border-color: #5B8EC9 !important;
    box-shadow: 0 0 0 2px rgba(40,100,174,.1);
}

/* Buttons */

.stButton > button {
    min-height: 41px;
    border-radius: 8px;
    border: 1px solid #DDE5EF;
    background: white;
    color: #31577F;
    font-size: 12px;
    font-weight: 650;
}

.stButton > button:hover {
    border-color: #6B97C8;
    background: #F0F5FC;
    color: #1C4D85;
}

.stButton > button[kind="primary"] {
    background: #2864AE;
    color: white;
    border-color: #2864AE;
}

.stButton > button[kind="primary"]:hover {
    background: #1D508F;
    color: white;
}

/* Answer */

.answer-panel {
    background: #FFFFFF;
    border: 1px solid #DFE7F1;
    border-left: 4px solid #3B7DC0;
    border-radius: 11px;
    padding: 20px;
    margin-top: 12px;
}

/* Footer */

.footer {
    text-align: center;
    color: #96A2B2;
    font-size: 11px;
    padding-top: 28px;
}

hr {
    border-color: var(--border) !important;
}

</style>
""", unsafe_allow_html=True)


# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.markdown("""
    <div style="padding:8px 3px 17px;">
        <div style="font-size:27px;">◈</div>
        <div class="brand">INSIGHT<span style="color:#3476BD;">IQ</span></div>
        <div class="brand-sub">BUSINESS INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.caption("WORKSPACE")

    st.markdown("""
    <div style="
        padding:11px;
        border-radius:8px;
        background:#EDF4FC;
        color:#245D9C;
        font-weight:700;
        font-size:13px;">
        ▦ &nbsp; Overview
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("ANALYTICS")

    st.markdown("""
    <div style="font-size:12px;color:#697B91;line-height:2.8;">
        ◫ &nbsp; Revenue performance<br>
        ◈ &nbsp; Product insights<br>
        ◎ &nbsp; Regional analysis<br>
        ▤ &nbsp; Monthly trends
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.caption("AI WORKSPACE")

    if st.button("✦  Ask the AI assistant", use_container_width=True):
        st.session_state.question_input = "What is the total revenue?"
        st.session_state.submit_question = True
        st.session_state.api_error = None
        st.rerun()

    st.divider()

    st.caption("PROJECT STACK")
    st.markdown("""
    <div style="font-size:11px;color:#8794A6;line-height:2;">
        Python · FastAPI<br>
        Streamlit · SQLite<br>
        Gemini integration
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("INSIGHTIQ  ·  VERSION 1.0")


# ======================================================
# PAGE HEADER
# ======================================================

left, right = st.columns([5, 1])

with left:
    st.markdown(
        '<div class="eyebrow">ANALYTICS WORKSPACE</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-title">Sales Overview</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-subtitle">'
        'A clear view of your business performance and sales insights.'
        '</div>',
        unsafe_allow_html=True
    )

with right:
    st.markdown("""
    <div style="
        text-align:center;
        margin-top:17px;
        padding:9px;
        border-radius:20px;
        background:#E9F5EE;
        color:#278052;
        font-size:10px;
        font-weight:750;">
        ● DATA LOADED
    </div>
    """, unsafe_allow_html=True)


# ======================================================
# HERO
# ======================================================

st.markdown("""
<div class="hero">
    <div class="hero-tag">BUSINESS PERFORMANCE CENTER</div>
    <h2>Turn your sales data into better decisions.</h2>
    <p>
        Monitor revenue, understand product performance, compare
        regions and discover business patterns using your AI-powered
        analytics assistant.
    </p>
</div>
""", unsafe_allow_html=True)


# ======================================================
# KPI METRICS
# ======================================================

st.markdown(
    '<div class="section-heading">Business Performance</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Key indicators from the current sales dataset.'
    '</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Total Revenue",
        money(TOTAL_REVENUE),
        help="Total revenue in the current dataset"
    )

with m2:
    st.metric(
        "Top Product",
        TOP_PRODUCT,
        money(TOP_PRODUCT_REVENUE)
    )

with m3:
    st.metric(
        "Leading Region",
        TOP_REGION,
        money(TOP_REGION_REVENUE)
    )

with m4:
    st.metric(
        "Months Analyzed",
        "6",
        "Jan – Jun 2026"
    )


# ======================================================
# CHARTS
# ======================================================

st.markdown(
    '<div class="section-heading">Revenue Performance</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Explore the monthly revenue distribution and leading business segments.'
    '</div>',
    unsafe_allow_html=True
)

chart_col, insight_col = st.columns([1.65, 1])

with chart_col:

    with st.container(border=True):

        st.markdown("##### Monthly Revenue Trend")

        df = pd.DataFrame(MONTHLY_DATA)

        chart_data = df.set_index("Month")

        st.bar_chart(
            chart_data,
            color="#3979BD",
            height=290
        )

        st.caption("Revenue values are shown in INR.")


with insight_col:

    with st.container(border=True):

        st.markdown("##### Top Performing Segments")

        st.markdown("**Top product**")
        st.markdown(
            f"<div style='font-size:20px;font-weight:750;color:#1B365D;'>"
            f"{TOP_PRODUCT}</div>",
            unsafe_allow_html=True
        )
        st.caption(f"Revenue: {money(TOP_PRODUCT_REVENUE)}")

        st.divider()

        st.markdown("**Leading region**")
        st.markdown(
            f"<div style='font-size:20px;font-weight:750;color:#1B365D;'>"
            f"{TOP_REGION}</div>",
            unsafe_allow_html=True
        )
        st.caption(f"Revenue: {money(TOP_REGION_REVENUE)}")

        st.divider()

        st.markdown("**Highest revenue month**")
        highest_month = max(
            MONTHLY_DATA["Revenue"]
        )
        month_name = MONTHLY_DATA["Month"][
            MONTHLY_DATA["Revenue"].index(highest_month)
        ]

        st.markdown(
            f"<div style='font-size:20px;font-weight:750;color:#1B365D;'>"
            f"{month_name} 2026</div>",
            unsafe_allow_html=True
        )
        st.caption(f"Revenue: {money(highest_month)}")


# ======================================================
# AI ASSISTANT
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-heading">AI Business Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Ask questions in natural language and receive meaningful business answers.'
    '</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    st.markdown(
        '<div class="assistant-header">✦ Ask your business data</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="assistant-description">'
        'Your AI assistant can analyze revenue, products, regions and monthly trends.'
        '</div>',
        unsafe_allow_html=True
    )

    st.text_input(
        "Your question",
        placeholder="e.g. Which product generated the highest revenue?",
        key="question_input",
        label_visibility="collapsed"
    )

    ask_col, clear_col, empty_col = st.columns([1.4, 1, 3])

    with ask_col:
        ask_clicked = st.button(
            "✦ Generate Insight",
            type="primary",
            use_container_width=True
        )

    with clear_col:
        st.button(
            "Clear",
            on_click=clear_results,
            use_container_width=True
        )


# ======================================================
# API REQUEST
# ======================================================

should_process = ask_clicked or st.session_state.submit_question

if should_process:

    st.session_state.submit_question = False

    current_question = st.session_state.question_input.strip()

    if not current_question:

        st.warning("Please enter a question first.")

    else:

        st.session_state.answer_data = None
        st.session_state.api_error = None
        st.session_state.last_question = current_question

        with st.spinner("Analyzing your business data..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"question": current_question},
                    timeout=60
                )

                if response.status_code == 200:

                    data = response.json()

                    if isinstance(data, dict) and "result" in data:

                        st.session_state.answer_data = data

                        st.session_state.history.insert(
                            0, current_question
                        )

                    else:
                        st.session_state.api_error = (
                            "The backend returned an unexpected response."
                        )

                else:

                    st.session_state.api_error = (
                        f"Server error: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.session_state.api_error = (
                    "Cannot connect to FastAPI. Start your backend first."
                )

            except requests.exceptions.Timeout:

                st.session_state.api_error = (
                    "The request timed out. Please try again."
                )

            except requests.exceptions.RequestException as error:

                st.session_state.api_error = f"Request failed: {error}"

            except ValueError:

                st.session_state.api_error = (
                    "The server returned an invalid response."
                )


# ======================================================
# ANSWER
# ======================================================

if st.session_state.api_error:
    st.error(st.session_state.api_error)

if st.session_state.answer_data:

    data = st.session_state.answer_data

    st.markdown("#### ✨ Your Analysis")

    st.caption(
        f"Your question: {st.session_state.last_question}"
    )

    with st.container(border=True):

        st.markdown(
            natural_language_answer(data.get("result"))
        )

        with st.expander("How the assistant understood your question"):
            st.write(
                explain_intent(data.get("interpretation"))
            )


# ======================================================
# SUGGESTED QUESTIONS
# ======================================================

st.markdown("---")

st.markdown(
    '<div class="section-heading">Explore More Insights</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Select a question to run an analysis instantly.'
    '</div>',
    unsafe_allow_html=True
)

questions = [
    "What is the total revenue?",
    "Which product generated the highest revenue?",
    "Show monthly revenue trend",
    "Which region has the highest sales?",
    "Compare January and February revenue"
]

for i in range(0, len(questions), 2):

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "↗  " + questions[i],
            key=f"question_{i}",
            on_click=select_example,
            args=(questions[i],),
            use_container_width=True
        )

    if i + 1 < len(questions):

        with col2:
            st.button(
                "↗  " + questions[i + 1],
                key=f"question_{i+1}",
                on_click=select_example,
                args=(questions[i + 1],),
                use_container_width=True
            )


# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.markdown("""
<div class="footer">
    <b>INSIGHTIQ · BUSINESS INTELLIGENCE</b><br>
    Intelligent analytics for better business decisions.<br><br>
    Python · FastAPI · Streamlit · SQLite
</div>
""", unsafe_allow_html=True)
