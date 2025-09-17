import streamlit as st

def show_info():
    st.markdown("### Available Experiments:")
    st.markdown("""
    * **Basic Op-Amp Simulator:** A basic simulation for common op-amp configurations.
    * **Integrator/Differentiator:** Simulate the behavior of op-amp based integrator and differentiator circuits with various input waveforms.
    * **Precision Rectifier:** Explore half-wave and full-wave precision rectifier circuits.
    * **Comparator:** Understand the basic functionality of a comparator circuit.
    * **Schmitt Trigger:** Simulate the hysteresis behavior of a Schmitt Trigger circuit.
    * **Active Wave Shaping:** Experiment with active clipper and clamper circuits.
    * **RC Phase Shift Oscillator:** Simulate the frequency and component requirements for an RC phase shift oscillator.
    * **Wien Bridge Oscillator:** Simulate the frequency and component requirements for a Wien Bridge oscillator.
    * **Square Wave Generator:** Design and simulate an op-amp based square wave generator (astable multivibrator).
    * **Active Filter:** Analyze the frequency response of active lowpass and highpass filters.
    """)

st.title("Information about the Simulator")
show_info()