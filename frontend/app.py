import requests
import streamlit as st


# =========================================================
# CONFIG
# =========================================================

API_URL = "http://127.0.0.1:8000/api/v1/question"

st.set_page_config(
    page_title="DataDose",
    page_icon="✦",
    layout="centered",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ================================
       PAGE
       ================================ */

    .stApp {
        background: #FFF9F2;
    }

    .main .block-container {
        max-width: 700px;
        padding: 2.5rem 1.2rem 3rem 1.2rem;
    }

    header {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ================================
       BRAND
       ================================ */

    .brand {
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }

    .brand-mark {
        width: 48px;
        height: 48px;

        margin: 0 auto 0.75rem auto;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #FF6B61;
        color: white;

        border-radius: 15px;

        font-size: 1.45rem;
        font-weight: 800;

        box-shadow: 0 8px 22px rgba(255, 107, 97, 0.22);
    }

    .brand-name {
        color: #182235;

        font-size: 2.45rem;
        font-weight: 800;

        letter-spacing: -1.5px;
    }

    .tagline {
        text-align: center;

        color: #747C89;

        font-size: 0.95rem;

        margin-bottom: 2.8rem;
    }


    /* ================================
       INTRO
       ================================ */

    .intro-title {
        text-align: center;

        color: #182235;

        font-size: 1.5rem;

        font-weight: 750;

        line-height: 1.3;

        margin-bottom: 0.2rem;
    }

    .intro-subtitle {
        text-align: center;

        color: #747C89;

        font-size: 0.92rem;

        margin-bottom: 1.7rem;
    }


    /* ================================
       DIFFICULTY LABEL
       ================================ */

    .difficulty-label {
        color: #182235;

        font-size: 0.88rem;

        font-weight: 700;

        margin-top: 1.3rem;

        margin-bottom: 0.5rem;
    }


    /* ================================
       RADIO BUTTONS
       ================================ */

    div[data-testid="stRadio"] {
        margin-bottom: 1.1rem;
    }

    div[data-testid="stRadio"] > label {
        display: none;
    }

    div[data-testid="stRadio"] > div {
        display: flex;
        gap: 0.55rem;
        width: 100%;
    }

    div[data-testid="stRadio"] label {
        background: #FFFFFF;

        border: 1px solid #E4DED5;

        border-radius: 13px;

        padding: 0.65rem 0.7rem;

        flex: 1;

        justify-content: center;

        transition: all 0.2s ease;
    }

    div[data-testid="stRadio"] label:hover {
        border-color: #2F8F6B;
        background: #F1F8F4;
    }

    div[data-testid="stRadio"] label p {
        color: #182235 !important;

        font-size: 0.88rem;

        font-weight: 600;
    }


    /* ================================
       GENERATE BUTTON
       ================================ */

    div.stButton > button {
        width: 100%;

        min-height: 3.35rem;

        border-radius: 14px;

        border: none;

        background: #2F8F6B;

        color: white;

        font-size: 0.98rem;

        font-weight: 700;

        box-shadow: 0 8px 20px rgba(47, 143, 107, 0.20);

        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: #267A5B;

        color: white;

        border: none;

        transform: translateY(-1px);

        box-shadow: 0 10px 24px rgba(47, 143, 107, 0.25);
    }


    /* ================================
       QUESTION RESULT
       ================================ */

    .answer-card {
        background: #E5F4ED;

        border: 1px solid #D2EADF;

        border-radius: 22px;

        padding: 1.6rem;

        margin-top: 1.6rem;

        box-shadow: 0 8px 25px rgba(47, 143, 107, 0.08);
    }

    .question-label {
        color: #2F8F6B;

        font-size: 0.72rem;

        font-weight: 800;

        letter-spacing: 1px;

        text-transform: uppercase;

        margin-bottom: 0.75rem;
    }

    .question-text {
        color: #182235;

        font-size: 1.12rem;

        line-height: 1.6;

        font-weight: 550;
    }

    .question-level {
        display: inline-block;

        background: #FFFFFF;

        color: #2F8F6B;

        border-radius: 20px;

        padding: 0.35rem 0.8rem;

        font-size: 0.73rem;

        font-weight: 700;

        margin-top: 1rem;
    }


    /* ================================
       FOOTER
       ================================ */

    .bottom-text {
        text-align: center;

        color: #969B9F;

        font-size: 0.82rem;

        margin-top: 2rem;
    }


    /* ================================
       MOBILE
       ================================ */

    @media (max-width: 480px) {

        .main .block-container {
            padding: 1.5rem 0.9rem 2rem 0.9rem;
        }

        .brand-mark {
            width: 44px;
            height: 44px;

            border-radius: 14px;
        }

        .brand-name {
            font-size: 2.1rem;
        }

        .tagline {
            font-size: 0.87rem;

            margin-bottom: 2.2rem;
        }

        .intro-title {
            font-size: 1.35rem;
        }

        .intro-subtitle {
            font-size: 0.86rem;
        }

        div[data-testid="stRadio"] > div {
            gap: 0.35rem;
        }

        div[data-testid="stRadio"] label {
            padding: 0.6rem 0.3rem;
        }

        div[data-testid="stRadio"] label p {
            font-size: 0.82rem;
        }

        div.stButton > button {
            min-height: 3.1rem;

            font-size: 0.94rem;
        }

        .answer-card {
            padding: 1.3rem;

            border-radius: 19px;
        }

        .question-text {
            font-size: 1.03rem;

            line-height: 1.6;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# BRAND
# =========================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-mark">✦</div>
        <div class="brand-name">DataDose</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="tagline">
        Your daily dose of Data Science.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# INTRO
# =========================================================

st.markdown(
    """
    <div class="intro-title">
        Ready for today's challenge?
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="intro-subtitle">
        One question. A little thinking. A step forward.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DIFFICULTY
# =========================================================

st.markdown(
    """
    <div class="difficulty-label">
        Choose your level
    </div>
    """,
    unsafe_allow_html=True,
)

difficulty = st.radio(
    "Difficulty",
    ["Easy", "Medium", "Hard"],
    horizontal=True,
    label_visibility="collapsed",
)


# =========================================================
# GENERATE QUESTION
# =========================================================

if st.button(
    "✦  Get Today's Question",
    use_container_width=True,
):

    payload = {
        "difficulty": difficulty
    }

    try:

        with st.spinner("Preparing your question..."):

            response = requests.post(
                API_URL,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

        st.session_state["question"] = data["question"]
        st.session_state["difficulty"] = data["difficulty"]

    except requests.exceptions.RequestException:

        st.error(
            "Couldn't connect to DataDose. "
            "Please make sure FastAPI is running."
        )


# =========================================================
# DISPLAY QUESTION
# =========================================================

if "question" in st.session_state:

    question = st.session_state["question"]
    level = st.session_state["difficulty"]

    st.markdown(
        f"""
        <div class="answer-card">

            <div class="question-label">
                Today's Question
            </div>

            <div class="question-text">
                {question}
            </div>

            <div class="question-level">
                {level}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="bottom-text">
        One question a day. Keep learning.
    </div>
    """,
    unsafe_allow_html=True,
)