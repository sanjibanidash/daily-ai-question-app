import os
import time

import requests
import streamlit as st
from dotenv import load_dotenv


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="DataDose",
    page_icon="✦",
    layout="centered",
)


# =========================================================
# BACKEND API CONFIGURATION
# =========================================================

load_dotenv()

backend_url = os.getenv("BACKEND_URL")

if not backend_url:
    try:
        backend_url = st.secrets["BACKEND_URL"]
    except Exception:
        backend_url = None

if not backend_url:
    st.error("BACKEND_URL is not configured.")
    st.stop()

QUESTION_API_URL = f"{backend_url.rstrip('/')}/api/v1/question"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- Main page ---------- */

    .stApp {
        background-color: #f7faf9;
    }

    .block-container {
        max-width: 760px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }


    /* ---------- Header ---------- */

    .logo {
        width: 46px;
        height: 46px;
        background: #13806f;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px auto;
        color: white;
        font-size: 25px;
        font-weight: 700;
    }

    .brand {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: #20325f;
        margin-bottom: 4px;
    }

    .tagline {
        text-align: center;
        color: #71809d;
        font-size: 15px;
        margin-bottom: 58px;
    }


    /* ---------- Hero ---------- */

    .eyebrow {
        text-align: center;
        color: #13806f;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 3px;
        margin-bottom: 14px;
    }

    .hero-title {
        text-align: center;
        color: #20325f;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        text-align: center;
        color: #71809d;
        font-size: 15px;
        margin-bottom: 42px;
    }


    /* ---------- Difficulty ---------- */

    .difficulty-title {
        color: #20325f;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    /* Make radio text visible */

    div[data-testid="stRadio"] label {
        color: #20325f !important;
        opacity: 1 !important;
    }

    div[data-testid="stRadio"] label p {
        color: #20325f !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stRadio"] {
        margin-bottom: 12px;
    }


    /* ---------- Generate button ---------- */

    div.stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        border: none;
        background: #137866;
        color: white !important;
        font-size: 15px;
        font-weight: 700;
        box-shadow: 0 8px 22px rgba(19, 120, 102, 0.18);
    }

    div.stButton > button:hover {
        background: #106a5b;
        color: white !important;
    }


    /* ---------- Question section ---------- */

    .question-label {
        color: #13806f;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 3px;
        margin-top: 48px;
        margin-bottom: 14px;
    }

    .question-card {
        background: white;
        border: 1px solid #dfe7e4;
        border-radius: 16px;
        padding: 28px 30px;
        min-height: 130px;
        box-shadow: 0 8px 25px rgba(31, 50, 95, 0.06);
    }

    .question-text {
        color: #20325f !important;
        font-size: 20px;
        line-height: 1.6;
        font-weight: 600;
    }


    /* ---------- Difficulty badge ---------- */

    .badge {
        display: inline-block;
        margin-top: 16px;
        padding: 6px 12px;
        border-radius: 20px;
        background: #e9f7f3;
        color: #13806f;
        font-size: 12px;
        font-weight: 700;
    }


    /* ---------- Generation time ---------- */

    .generated-time {
        text-align: right;
        color: #8b98ad;
        font-size: 11px;
        margin-top: 24px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="logo">✦</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="brand">DataDose</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="tagline">Your daily dose of Data Science.</div>',
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="eyebrow">DAILY LEARNING</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-title">Ready for today\'s challenge?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-subtitle">'
    'One thoughtful question every day to sharpen your Data Science and AI skills.'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# DIFFICULTY SELECTOR
# =========================================================

st.markdown(
    '<div class="difficulty-title">Choose your level</div>',
    unsafe_allow_html=True,
)

difficulty = st.radio(
    "Difficulty",
    ["Easy", "Medium", "Hard"],
    horizontal=True,
    label_visibility="collapsed",
)


# =========================================================
# QUESTION GENERATOR
# =========================================================

def generate_question(difficulty: str):

    response = requests.post(
        QUESTION_API_URL,
        json={
            "difficulty": difficulty
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["question"], data["difficulty"]


# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button("✦  Generate Today's Question"):

    start_time = time.time()

    with st.spinner("Preparing your question..."):

        try:

            question, returned_difficulty = generate_question(difficulty)

            question = question.strip()

            if not question:
                st.error("The backend returned an empty question.")
                st.stop()

            st.session_state["question"] = question

            st.session_state["difficulty"] = returned_difficulty

            st.session_state["generation_time"] = (
                time.time() - start_time
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the DataDose backend. "
                "Make sure FastAPI is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The backend took too long to respond. "
                "Please try again."
            )

        except requests.exceptions.HTTPError as e:

            st.error(
                "The DataDose backend returned an error."
            )

            st.code(str(e))

        except Exception as e:

            st.error(
                "Something went wrong while generating the question."
            )

            st.code(str(e))


# =========================================================
# QUESTION CARD
# =========================================================

if "question" in st.session_state:

    st.markdown(
        '<div class="question-label">TODAY\'S QUESTION</div>',
        unsafe_allow_html=True,
    )

    question = st.session_state["question"]

    question_difficulty = st.session_state["difficulty"]

    generation_time = st.session_state["generation_time"]

    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-text">
                {question}
            </div>
        </div>

        <div class="badge">
            {question_difficulty}
        </div>

        <div class="generated-time">
            Generated in {generation_time:.2f} seconds
        </div>
        """,
        unsafe_allow_html=True,
    )