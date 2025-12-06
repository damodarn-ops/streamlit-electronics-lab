import streamlit as st

def show_info():
    st.markdown("### List of Experiments:")
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

def show_info1():
    st.markdown("### Instruction:")
    st.markdown("""
    * Each experiment consists of 6 tabs namely **Objective**, **Prelab**, **Theory**, **Simulation**, **Postlab**,and **Feedback**.
    * **Objective:** This tab outlines the **primary goal of the experiment** and the **specific learning outcomes** you are expected to achieve upon its completion.
    * **Prelab:** This tab contains multiple-choice questions (MCQs) designed to test your basic understanding of the experiment.    
    * **Theory:** This tab provides the fundamental concepts and principles related to the experiment, helping you understand the underlying science before performing the simulation.
    * **Post-lab:** This tab contains multiple-choice questions (MCQs) designed to assess your understanding of the experiment after completing the simulation.
    * **Simulation:** This tab allows you to perform the experiment according to the circuit diagram. Select inputs as per the specific circuit diagram, if required, and choose the desired circuit (for example, in a basic op-amp simulator, select from inverting amplifier, non-inverting amplifier, or voltage follower). The plots will be automatically generated. To record data for tabulation, click on **Log Current Simulation**.
    * **Feedback:** This tab allows you to provide your comments or suggestions about the experiment and the virtual lab. Your feedback helps us improve the learning experience.
    
    """)

st.title("Information about the Simulator")
show_info()
show_info1()