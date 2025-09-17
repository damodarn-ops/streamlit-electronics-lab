# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:38:39 2025

@author: damo3
"""

# pages/7_RC_Phase_Shift_Oscillator.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

st.set_page_config(layout="wide", page_title="RC Phase Shift Oscillator")

st.title("RC Phase Shift Oscillator Simulator")

# Create the tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

# --- Prelab Tab ---
with tab1:
    st.header("Prelab")
    st.markdown("""
    **Objective:** To understand the operation of an RC phase shift oscillator and verify the conditions for sustained oscillation.

    **Pre-requisites:**
    1.  Knowledge of operational amplifiers (op-amps).
    2.  Understanding of resistor-capacitor (RC) networks and their phase shifting properties.
    3.  Familiarity with the Barkhausen criterion for oscillation.

    **Questions:**
    1.  What is the Barkhausen criterion for oscillation?
    2.  Explain why a phase shift of 180° is required from the feedback network in an RC phase shift oscillator.
    3.  How is the remaining 180° phase shift achieved?
    4.  What is the minimum gain required from the amplifier stage to sustain oscillations?
    5.  How does changing the value of R or C affect the frequency of oscillation?
    """)

# --- Theory Tab ---
with tab2:
    st.header("Theory")
    st.markdown(r"""
    An **RC phase shift oscillator** is a type of electronic oscillator that generates a sine wave output. It is composed of a three-stage RC ladder network and an inverting amplifier (typically an op-amp).

    ### Principle of Operation
    The circuit operates based on the **Barkhausen Criterion**, which states that for sustained oscillations to occur, two conditions must be met:
    1.  The **loop gain** ($A\beta$) must be equal to or greater than unity ($|A\beta| \ge 1$).
    2.  The **total phase shift** around the feedback loop must be 0° or 360° ($∠A\beta = 0°$ or $360°$).

    ### RC Phase Shift Network
    The oscillator uses a three-stage RC ladder network, which provides a total phase shift of **180°** at a specific frequency. Each RC section contributes a phase shift. While a single RC circuit can provide up to 90° of phase shift, cascading three identical sections allows for a stable 180° shift at the resonant frequency.

    ### The Amplifier
    The amplifier stage is an **inverting amplifier**, which provides its own 180° phase shift. It also provides the necessary gain to compensate for the signal attenuation caused by the RC network. The minimum gain required to overcome the attenuation of the three-stage RC network is **29**. Thus, the gain of the amplifier must be equal to or greater than 29 to satisfy the Barkhausen criterion for loop gain.

    ### Frequency of Oscillation
    The oscillation frequency ($f_o$) is determined by the values of R and C in the RC network and is given by the formula:
    $$f_o = \frac{1}{2 \pi R C \sqrt{6}}$$
    
    The amplifier gain ($A_v$) required for sustained oscillation is:
    $$A_v = \frac{R_F}{R_1} \ge 29$$
    """)

# --- Simulation Tab ---
with tab3:
    # --- Layout with Columns ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Oscillator Parameters")
        
        # Number input for Resistance (R) in kΩ.
        R_kohm = st.number_input(
            "Resistance (R) (kΩ)",
            min_value=0.001,
            value=10.0,
            step=0.1,
            format="%.3f",
            key="R_input_oscillator"
        )
        
        # Number input for Capacitance (C) in µF.
        C_uF = st.number_input(
            "Capacitance (C) (µF)",
            min_value=0.0001,
            value=0.1,
            step=0.001,
            format="%.5f",
            key="C_input_oscillator"
        )
        
        # Number input for Desired Signal Frequency.
        f_desired = st.number_input(
            "Desired Signal Frequency (Hz)",
            min_value=0.0,
            value=100.0,
            step=1.0,
            format="%.1f",
            key="f_desired_input_oscillator"
        )
        
        st.markdown("---")
        st.write("Developed by DAMODAR")

    # --- Core Simulation Logic ---
    def calculate_oscillation_parameters(R_kohm, C_uF, f_desired):
        R_ohms = R_kohm * 1000
        C_farads = C_uF * 1e-6
        f_observed = 0.0
        R_calculated_kohm_for_desired = 0.0
        R1_kohm_amp = 0.0
        RF_kohm_amp = 0.0
        
        if R_ohms > 0 and C_farads > 0:
            try:
                f_observed = 1 / (2 * np.pi * R_ohms * C_farads * np.sqrt(6))
            except ZeroDivisionError:
                st.error("R or C cannot be zero for frequency calculation.")
                f_observed = 0.0
        else:
            st.warning("Resistance (R) and Capacitance (C) must be positive for oscillation.")
            f_observed = 0.0
            
        if f_desired > 0 and C_farads > 0:
            try:
                R_calc_ohms_for_desired = 1 / (2 * np.pi * f_desired * C_farads * np.sqrt(6))
                R_calculated_kohm_for_desired = R_calc_ohms_for_desired / 1000
            except ZeroDivisionError:
                st.error("Desired frequency or capacitance cannot be zero for R calculation.")
                R_calculated_kohm_for_desired = 0.0
        else:
            R_calculated_kohm_for_desired = 0.0

        if R_calculated_kohm_for_desired > 0:
            R1_kohm_amp = 10 * R_calculated_kohm_for_desired
            RF_kohm_amp = 29 * R1_kohm_amp
        else:
            R1_kohm_amp = 10.0
            RF_kohm_amp = 29 * R1_kohm_amp

        num_cycles = 5
        amp = 1.0
        
        total_duration = num_cycles / f_observed if f_observed != 0 else 0.01
        sampling_rate = max(100 * f_observed, 1000) if f_observed != 0 else 10000
        num_points = int(sampling_rate * total_duration)
        if num_points < 2: num_points = 2

        t = np.linspace(0, total_duration, num_points, endpoint=False)
        y_signal = amp * np.sin(2 * np.pi * f_observed * t)
        
        time_period = 1 / f_observed if f_observed != 0 else float('inf')

        return {
            "R_input_kohm": R_kohm,
            "C_input_uF": C_uF,
            "f_desired": f_desired,
            "output_amplitude": amp,
            "time_period_s": time_period,
            "f_output": f_observed,
            "R_calculated_kohm_for_desired": R_calculated_kohm_for_desired,
            "R1_kohm_amp": R1_kohm_amp,
            "RF_kohm_amp": RF_kohm_amp,
            "y_signal": y_signal,
            "t_time": t,
            "total_duration": total_duration
        }

    # --- CRO Display and Simulation Results ---
    with col2:
        st.header("Circuit Diagram")
        
        st.image("images/RCphaseshiftoscillator.png", caption="RC Phaseshift Oscillator Circuit", use_container_width=True)
        
        st.subheader("CRO Display")

        sim_results = calculate_oscillation_parameters(R_kohm, C_uF, f_desired)

        # Plotting for Output Signal (CH1)
        fig1, ax1 = plt.subplots(figsize=(6, 3), dpi=100)
        ax1.plot(sim_results["t_time"], sim_results["y_signal"], color='red')
        ax1.set_title("Oscillator Output Signal")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Amplitude (V)")
        ax1.grid(True)
        ax1.set_facecolor("black")
        ax1.axhline(0, color='gray', linewidth=0.5)
        ax1.axvline(0, color='gray', linewidth=0.5)
        
        plot_ylim = sim_results["output_amplitude"] * 1.5 if sim_results["output_amplitude"] != 0 else 1.0
        ax1.set_ylim(-plot_ylim, plot_ylim)
        ax1.set_xlim(0, sim_results["total_duration"])
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        
        ax1.text(0.02, 0.95, f'Amp: {sim_results["output_amplitude"]:.2f} V', transform=ax1.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
        ax1.text(0.02, 0.85, f'Freq: {sim_results["f_output"]:.2f} Hz', transform=ax1.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
        st.pyplot(fig1)

        st.header("Simulation Results")

        if 'oscillator_history' not in st.session_state:
            st.session_state.oscillator_history = []

        if st.button("Log Current Results to Table", key="log_button_oscillator"):
            new_entry = {
                "Input R (kΩ)": f"{sim_results['R_input_kohm']:.2f}",
                "Input C (µF)": f"{sim_results['C_input_uF']:.2f}",
                "Desired Freq (Hz)": f"{sim_results['f_desired']:.2f}",
                "Output Amp (V)": f"{sim_results['output_amplitude']:.2f}",
                "Time Period (s)": f"{sim_results['time_period_s']:.4f}",
                "Output Freq (Hz)": f"{sim_results['f_output']:.2f}",
                "Calc. R for F_des (kΩ)": f"{sim_results['R_calculated_kohm_for_desired']:.2f}",
                "Amp R1 (kΩ)": f"{sim_results['R1_kohm_amp']:.2f}",
                "Amp RF (kΩ)": f"{sim_results['RF_kohm_amp']:.2f}"
            }
            st.session_state.oscillator_history.append(new_entry)

        if st.session_state.oscillator_history:
            df_history = pd.DataFrame(st.session_state.oscillator_history)
            st.dataframe(df_history, use_container_width=True)

        if st.button("Clear Table History", key="clear_table_button_oscillator"):
            st.session_state.oscillator_history = []
            st.rerun()

# --- Postlab Tab ---
with tab4:
    st.header("Postlab")
    st.markdown("""
    **Conclusion:**
    * Summarize your observations from the simulation, focusing on the relationship between R, C, and the output frequency.
    * Explain how the calculated amplifier resistor values (R1 and RF) are related to the required gain.
    * Discuss the limitations of this ideal simulation compared to a real-world circuit.

    **Analysis:**
    * Using the formula, calculate the required R and C values for a 500 Hz oscillation.
    * If the input R is 10kΩ and C is 0.01µF, what is the output frequency?
    * What are some advantages and disadvantages of using an RC phase shift oscillator?
    """)

# --- Feedback Tab ---
with tab5:
    st.header("Feedback")
    st.markdown("""
    We value your feedback to improve this simulator. Please let us know your thoughts.

    **Instructions:**
    1.  What did you find most useful about this simulator?
    2.  Were there any features that were confusing or difficult to use?
    3.  What new features would you like to see added in the future?
    4.  Any other comments or suggestions.
    """)