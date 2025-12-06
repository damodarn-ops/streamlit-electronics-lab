import streamlit as st
import os

st.set_page_config(
    page_title="Electronics Lab Simulator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR THEME BASED ON PROVIDED IMAGE ---
st.markdown(
    """
    <style>
    /* Main app background color */
    .stApp {
        background-color: #1a4d7d; /* Dark blue from the image background */
        color: white; /* Ensure text is readable on dark background */
    }

    /* Adjust Streamlit's default elements for better visibility on dark background */
    .css-1av0vzn { /* Streamlit's header container class */
        background-color: #1a4d7d; /* Match the main background */
        color: white;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white; /* White headings for contrast */
    }

    p {
        color: white; /* White paragraph text for contrast */
    }

    /* Specific styles for the main title and welcome text */
    .main-title {
        color: #ff8c00; /* Orange color from "RAEEUCCI-2026" */
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .welcome-text {
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Card styling - adjusted for the dark background and new orange color */
    .experiment-card {
        display: block;
        border: 2px solid #ff8c00; /* Orange border for the cards */
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        background-color: #ff8c00; /* The new orange background color */
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        text-decoration: none;
        color: white !important; /* This ensures the text is white on orange */
        font-weight: bold;
        transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
    }

    .experiment-card:hover {
        transform: translateY(-5px); /* Lift effect on hover */
        box-shadow: 0 8px 16px rgba(0,0,0,0.4); /* Stronger shadow on hover */
        background-color: #ffa500; /* A more distinct light orange on hover */
    }

    /* Footer adjustments */
    .stMarkdown p {
        color: white !important; /* Ensure footer text is white */
    }

    hr {
        border-top: 1px solid #ff8c00; /* Orange separator line */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- HEADER WITH LOGO ---
col_text, col_logo = st.columns([4, 1])

with col_text:
    st.title("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY")
    st.subheader("Department of Electronics and Communication Engineering")

with col_logo:
    # Ensure the logo path is correct
    st.image("image_a2e0d8.png", width=150)

# --- MAIN TITLE ---
st.markdown("<h2 class='main-title'>Welcome to the Electronics Lab Simulator!</h2>", unsafe_allow_html=True)
st.markdown("<p class='welcome-text'>Click on an experiment below to run it.</p>", unsafe_allow_html=True)

# --- EXPERIMENTS (Map to page names) ---
experiments = {
    "Info": "Info",
    "Basic Op-Amp Simulator": "Basic_Op_Amp_Simulator",
    "Integrator / Differentiator": "Integrator_Differentiator",
    "Precision Rectifier": "Precision_Rectifier",
    "Comparator": "Comparator",
    "Schmitt Trigger": "Schmitt_Trigger",
    "Active Wave Shaping": "Active_Wave_Shaping",
    "RC Phase Shift Oscillator": "RC_Phase_Shift_Oscillator",
    "Wien Bridge Oscillator": "Wien_Bridge_Oscillator",
    "Square Wave Generator": "Square_Wave_Generator",
    "Active Filter": "Active_Filter",
    "Feedback": "Feedback"
}

# --- DISPLAY EXPERIMENTS AS BOXES ---
cols = st.columns(3)
for i, (exp, page_name) in enumerate(experiments.items()):
    with cols[i % 3]:
        st.markdown(
            f"""
            <a href="/{page_name.replace(' ', '%20')}" target="_self"
            class="experiment-card">
                {exp}
            </a>
            """,
            unsafe_allow_html=True
        )

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>Developed by <b>Dr. Damodar Panigrahy</b>, Assistant Professor, Department of ECE, SRMIST, Kattankulathur.</p>",
    unsafe_allow_html=True
)