import os
import re
import html
import requests
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DataDose",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CONFIG
# ============================================================

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

QUESTION_ENDPOINT = f"{BACKEND_URL}/api/v1/question"


# ============================================================
# SESSION STATE
# ============================================================

st.session_state.setdefault("started", False)
st.session_state.setdefault("name", "")
st.session_state.setdefault("email", "")
st.session_state.setdefault("difficulty", "Medium")
st.session_state.setdefault("question", None)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   APP
   ============================================================ */

[data-testid="stAppViewContainer"] {
    background: #0a1020;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"],
#MainMenu,
footer {
    display: none;
}

.block-container {
    max-width: 650px;
    padding-top: 40px;
    padding-bottom: 35px;
}


/* ============================================================
   LANDING BRAND
   ============================================================ */

.brand {
    text-align: center;
    margin-bottom: 40px;
}

.brand-icon {
    width: 40px;
    height: 40px;
    margin: 0 auto 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 11px;

    background: #10312f;
    border: 1px solid #176b63;

    color: #2dd4bf;
    font-size: 18px;
    font-weight: 700;
}

.brand-title {
    color: #f8fafc;
    font-size: 32px;
    font-weight: 750;
    letter-spacing: -1px;
}

.brand-subtitle {
    color: #64748b;
    font-size: 13px;
    margin-top: 6px;
}


/* ============================================================
   PRACTICE HEADER
   ============================================================ */

.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 38px;
}

.app-logo {
    color: #f8fafc;
    font-size: 18px;
    font-weight: 700;
}

.app-logo span {
    color: #2dd4bf;
}

.app-mode {
    color: #64748b;
    font-size: 12px;
}


/* ============================================================
   WELCOME
   ============================================================ */

.welcome-label {
    color: #64748b;
    font-size: 12px;
    margin-bottom: 3px;
}

.welcome-name {
    color: #f8fafc;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: -0.4px;
    margin-bottom: 27px;
}


/* ============================================================
   LABEL
   ============================================================ */

.section-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-testid="stTextInput"] label {
    display: none !important;
}

div[data-testid="stTextInput"] input {
    height: 48px;

    background: #111827 !important;
    color: #f8fafc !important;

    border: 1px solid #273449 !important;
    border-radius: 10px !important;

    font-size: 14px;

    box-shadow: none !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #2dd4bf !important;
    box-shadow: 0 0 0 1px #2dd4bf !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #64748b !important;
}


/* ============================================================
   BUTTON BASE
   ============================================================ */

.stButton > button {
    width: 100%;
    height: 45px;

    background: #111827 !important;
    color: #cbd5e1 !important;

    border: 1px solid #273449 !important;
    border-radius: 10px !important;

    font-size: 14px;
    font-weight: 600;

    transition: all 0.15s ease;
}

.stButton > button:hover {
    background: #172033 !important;
    color: #2dd4bf !important;
    border-color: #2dd4bf !important;
}


/* ============================================================
   SELECTED DIFFICULTY
   ============================================================ */

.selected > div > button,
.selected button {
    background: #0f766e !important;
    color: #ffffff !important;
    border-color: #0f766e !important;
}

.selected > div > button:hover,
.selected button:hover {
    background: #0d9488 !important;
    color: #ffffff !important;
    border-color: #0d9488 !important;
}


/* ============================================================
   PRIMARY BUTTON
   ============================================================ */

.primary > div > button,
.primary button {
    background: #0f766e !important;
    color: #ffffff !important;
    border-color: #0f766e !important;

    height: 48px;

    font-weight: 650;
}

.primary > div > button:hover,
.primary button:hover {
    background: #0d9488 !important;
    color: #ffffff !important;
    border-color: #0d9488 !important;

    box-shadow: 0 5px 18px rgba(20, 184, 166, 0.16);
}


/* ============================================================
   QUESTION CARD
   ============================================================ */

.question-card {
    margin-top: 24px;

    padding: 25px 27px;

    background: #111827;

    border: 1px solid #263449;

    border-radius: 14px;

    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.16);
}

.question-meta {
    color: #2dd4bf;

    font-size: 10px;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 1px;

    margin-bottom: 12px;
}

.question-text {
    color: #f8fafc;

    font-size: 19px;
    font-weight: 600;

    line-height: 1.55;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    color: #475569;
    text-align: center;
    font-size: 11px;
    margin-top: 28px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# EMAIL VALIDATION
# ============================================================

def valid_email(email):
    return bool(
        re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email.strip()
        )
    )


# ============================================================
# BACKEND REQUEST
# ============================================================

def generate_question(difficulty):

    try:

        response = requests.post(
            QUESTION_ENDPOINT,
            json={
                "difficulty": difficulty
            },
            timeout=30
        )

    except requests.exceptions.ConnectionError:
        return None, "Unable to connect to the backend."

    except requests.exceptions.Timeout:
        return None, "The backend took too long to respond."

    except requests.exceptions.RequestException:
        return None, "Unable to contact the question service."

    if response.status_code != 200:

        try:

            data = response.json()
            detail = data.get("detail")

            if detail:
                return None, str(detail)

        except Exception:
            pass

        return (
            None,
            f"Backend returned error {response.status_code}."
        )

    try:

        data = response.json()

    except ValueError:

        return None, "Backend returned invalid JSON."

    question = data.get("question")

    if not question:

        nested = data.get("data")

        if isinstance(nested, dict):
            question = nested.get("question")

    if not question:

        return None, "No question was returned."

    return str(question).strip(), None


# ============================================================
# LANDING PAGE
# ============================================================

if not st.session_state.started:

    st.markdown(
        '<div class="brand">'
        '<div class="brand-icon">✦</div>'
        '<div class="brand-title">DataDose</div>'
        '<div class="brand-subtitle">'
        'Your daily dose of Data Science.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("start_form"):

        name = st.text_input(
            "Name",
            value=st.session_state.name,
            placeholder="Your name"
        )

        email = st.text_input(
            "Email",
            value=st.session_state.email,
            placeholder="Your email"
        )

        st.markdown(
            "<div style='height:8px'></div>",
            unsafe_allow_html=True
        )

        submit = st.form_submit_button(
            "Start Practicing  →"
        )

    if submit:

        name = name.strip()
        email = email.strip()

        if not name:

            st.error("Please enter your name.")

        elif not email:

            st.error("Please enter your email.")

        elif not valid_email(email):

            st.error("Please enter a valid email address.")

        else:

            st.session_state.name = name
            st.session_state.email = email
            st.session_state.started = True

            st.rerun()

    st.markdown(
        '<div class="footer">Practice · Learn · Improve</div>',
        unsafe_allow_html=True
    )


# ============================================================
# PRACTICE PAGE
# ============================================================

else:

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="app-header">'
        '<div class="app-logo">'
        '<span>✦</span> DataDose'
        '</div>'
        '<div class="app-mode">Daily practice</div>'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # WELCOME
    # --------------------------------------------------------

    safe_name = html.escape(
        st.session_state.name
    )

    st.markdown(
        '<div class="welcome-label">Welcome back</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="welcome-name">{safe_name}</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # DIFFICULTY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">Difficulty</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        3,
        gap="small"
    )


    # ========================================================
    # EASY
    # ========================================================

    with col1:

        if st.session_state.difficulty == "Easy":

            st.markdown(
                '<div class="selected">',
                unsafe_allow_html=True
            )

        if st.button(
            "Easy",
            use_container_width=True,
            key="easy"
        ):

            st.session_state.difficulty = "Easy"
            st.session_state.question = None

            st.rerun()

        if st.session_state.difficulty == "Easy":

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


    # ========================================================
    # MEDIUM
    # ========================================================

    with col2:

        if st.session_state.difficulty == "Medium":

            st.markdown(
                '<div class="selected">',
                unsafe_allow_html=True
            )

        if st.button(
            "Medium",
            use_container_width=True,
            key="medium"
        ):

            st.session_state.difficulty = "Medium"
            st.session_state.question = None

            st.rerun()

        if st.session_state.difficulty == "Medium":

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


    # ========================================================
    # HARD
    # ========================================================

    with col3:

        if st.session_state.difficulty == "Hard":

            st.markdown(
                '<div class="selected">',
                unsafe_allow_html=True
            )

        if st.button(
            "Hard",
            use_container_width=True,
            key="hard"
        ):

            st.session_state.difficulty = "Hard"
            st.session_state.question = None

            st.rerun()

        if st.session_state.difficulty == "Hard":

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    st.markdown(
        "<div style='height:17px'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="primary">',
        unsafe_allow_html=True
    )

    generate = st.button(
        "Generate Question  →",
        use_container_width=True,
        key="generate"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # GENERATE QUESTION
    # --------------------------------------------------------

    if generate:

        with st.spinner("Generating..."):

            question, error = generate_question(
                st.session_state.difficulty
            )

        if error:

            st.error(error)

        else:

            st.session_state.question = question


    # --------------------------------------------------------
    # QUESTION CARD
    # --------------------------------------------------------

    if st.session_state.question:

        safe_question = html.escape(
            st.session_state.question
        )

        safe_difficulty = html.escape(
            st.session_state.difficulty
        )

        question_card = (
            '<div class="question-card">'
            '<div class="question-meta">'
            f'{safe_difficulty} · Interview Question'
            '</div>'
            '<div class="question-text">'
            f'{safe_question}'
            '</div>'
            '</div>'
        )

        st.markdown(
            question_card,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # START OVER
    # --------------------------------------------------------

    st.markdown(
        "<div style='height:15px'></div>",
        unsafe_allow_html=True
    )

    if st.button(
        "← Start over",
        use_container_width=True,
        key="start_over"
    ):

        st.session_state.started = False
        st.session_state.name = ""
        st.session_state.email = ""
        st.session_state.difficulty = "Medium"
        st.session_state.question = None

        st.rerun()


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown(
        '<div class="footer">'
        'DataDose · Daily Data Science Practice'
        '</div>',
        unsafe_allow_html=True
    )