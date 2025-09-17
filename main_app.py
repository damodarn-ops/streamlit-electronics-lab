# main_app.py
import streamlit as st
import os

st.set_page_config(
    page_title="Electronics Lab Simulator",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar
)

# --- HEADER WITH LOGO ---
col_text, col_logo = st.columns([4, 1])

with col_text:
    st.title("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY")
    st.subheader("Department of Electronics and Communication Engineering")

with col_logo:
    st.image("image_a2e0d8.png", width=150)

# --- MAIN TITLE ---
st.markdown("<h2 style='text-align: center;'>Welcome to the Electronics Lab Simulator!</h2>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Click on an experiment below to run it.</p>", unsafe_allow_html=True)

# --- EXPERIMENTS (Map to page names) ---
experiments = {
  
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
    "Info": "Info"  # This is the correct way to add the "Info" entry.
}


# --- DISPLAY EXPERIMENTS AS BOXES ---
cols = st.columns(3)
for i, (exp, page_name) in enumerate(experiments.items()):
    with cols[i % 3]:
        # Instead of button, we make clickable link styled as a card
        st.markdown(
            f"""
            <a href="/{page_name.replace(' ', '%20')}" target="_self"
            style="
                display: block;
                border: 2px solid #4CAF50;
                border-radius: 12px;
                padding: 20px;
                margin: 10px;
                text-align: center;
                background-color: #f9f9f9;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                text-decoration: none;
                color: black;
                font-weight: bold;
                transition: 0.3s;
            "
            onmouseover="this.style.backgroundColor='#e6ffe6';"
            onmouseout="this.style.backgroundColor='#f9f9f9';">
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
