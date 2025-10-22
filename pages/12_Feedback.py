# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 01:33:50 2025

@author: damo3
"""

import streamlit as st

def show_info():
    # Use st.title() to display the main title.
    st.title("Feedback about the simulator")
    
    # Use st.markdown() with a link for the URL.
    feedback_link = "https://forms.gle/poXiv51je3qWHjB89"
    st.markdown(f"Please provide your feedback using this link: **[Feedback Form]({feedback_link})**")
    
    # You could also use st.info() for a prominent information box.
    # st.info(f"Access the feedback form here: {feedback_link}")

show_info()