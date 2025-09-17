# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:43:53 2025

@author: damo3
"""

# pages/9_Square_Wave_Generator.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

st.set_page_config(layout="wide", page_title="Square Wave Generator")

st.title("Square Wave Generator Simulator")

# Create the tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

# --- Prelab Tab ---
with tab1:
    st.header("Prelab")
    st.markdown("""
    **Objective:** To understand the operation of an op-amp based square wave generator (astable multivibrator) and its relationship to the circuit's components.

    **Pre-requisites:**
    1.  Basic knowledge of operational amplifiers (op-amps) and their comparator function.
    2.  Understanding of resistor-capacitor (RC) circuits and their charging/discharging behavior.
    3.  Familiarity with positive feedback in op-amp circuits.

    **Questions:**
    1.  What is the primary function of the RC circuit (RF and C) in this generator?
    2.  What is the role of the voltage divider (R1 and R2) at the non-inverting input?
    3.  Explain the concept of positive and negative saturation in an op-amp.
    4.  How does the capacitor's voltage affect the op-amp's output state?
    5.  How would changing the value of C or RF affect the output frequency?
    """)

# --- Theory Tab ---
with tab2:
    st.header("Theory")
    st.markdown(r"""
    An op-amp **square wave generator**, also known as an **astable multivibrator**, is a circuit that produces a continuous square wave output without any external trigger signal. It operates by utilizing an op-amp as a comparator with **positive feedback** and an **RC circuit** that acts as a timing element.

    ### Principle of Operation
    The op-amp's output will be in one of two states: a high positive saturation voltage ($+V_{sat}$) or a low negative saturation voltage ($-V_{sat}$). The circuit works in a cycle of charging and discharging the capacitor (C).

    1.  **Capacitor Charging:** When the output is at $+V_{sat}$, the capacitor C charges through the feedback resistor $R_F$. The voltage across the capacitor, $V_C$, increases exponentially towards $+V_{sat}$.
    2.  **Comparator Action:** The voltage at the non-inverting input ($V_+$) is a fraction of the output voltage, determined by the voltage divider $R_1$ and $R_2$. The threshold voltage for the comparator is given by:
        $$V_{threshold} = \beta \times V_{out} = \frac{R_2}{R_1 + R_2} \times V_{out}$$
    3.  **State Change:** When the capacitor's voltage ($V_C$) exceeds the positive threshold voltage at the non-inverting input, the op-amp's output flips from $+V_{sat}$ to $-V_{sat}$. The capacitor then begins to discharge towards $-V_{sat}$.
    4.  **Reverse State Change:** When the capacitor's voltage falls below the negative threshold voltage ($-V_{threshold}$), the op-amp's output flips back to $+V_{sat}$, and the cycle repeats.

    ### Period and Frequency
    The period ($T$) of the square wave is determined by the time it takes for the capacitor to charge and discharge between the positive and negative threshold voltages. For a symmetric output, the period is given by:
    $$T = 2 R_F C \ln\left(1 + \frac{2R_2}{R_1}\right)$$
    The frequency ($f$) is the reciprocal of the period:
    $$f = \frac{1}{T}$$
    """)

# --- Simulation Tab ---
with tab3:
    # --- Layout with Columns ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Generator Parameters")
    
        # Number input for Feedback Resistance (RF) in kΩ.
        RF_kohm = st.number_input(
            "Feedback Resistance (RF) (kΩ)",
            min_value=0.001,
            value=10.0,
            step=0.1,
            format="%.3f",
            key="RF_input_sq_wave"
        )
    
        # Number input for Capacitance (C) in µF.
        C_uF = st.number_input(
            "Capacitance (C) (µF)",
            min_value=0.0001,
            value=0.1,
            step=0.001,
            format="%.5f",
            key="C_input_sq_wave"
        )
    
        # Number input for Resistance R1 (part of voltage divider for thresholds) in kΩ.
        R1_kohm = st.number_input(
            "Resistance (R1) (kΩ)",
            min_value=0.001,
            value=10.0,
            step=0.1,
            format="%.3f",
            key="R1_input_sq_wave"
        )
    
        # Number input for Resistance R2 (part of voltage divider for thresholds) in kΩ.
        R2_kohm = st.number_input(
            "Resistance (R2) (kΩ)",
            min_value=0.001,
            value=10.0,
            step=0.1,
            format="%.3f",
            key="R2_input_sq_wave"
        )
    
        st.markdown("---")
        st.write("Developed by DAMODAR")

    # --- Core Simulation Logic ---
    def calculate_square_wave_parameters(RF_kohm, C_uF, R1_kohm, R2_kohm):
        RF_ohms = RF_kohm * 1000
        C_farads = C_uF * 1e-6
        R1_ohms = R1_kohm * 1000
        R2_ohms = R2_kohm * 1000
    
        amp_supply = 15.0
    
        T = 0.0
        T_on = 0.0
        T_off = 0.0
        freq = 0.0
        y_signal = np.array([])
        t_time = np.array([])
        total_duration = 0.0
        C_amp = 0.0
    
        if (R1_ohms + R2_ohms) == 0:
            st.error("Sum of R1 and R2 cannot be zero. Please adjust values.")
            return None
            
        # Simplified beta for the original log function T = 2 * RF * C * ln((1 + beta) / (1 - beta))
        # The correct formula is T = 2 * RF * C * ln(1 + 2*R2/R1). Let's use that.
        # This simplifies to T = 2 * RF * C * ln( (R1+2*R2)/R1 )
        # This implies a beta of R2/(R1+R2)
        beta = R2_ohms / (R1_ohms + R2_ohms)
        
        # We need a stable oscillation, which depends on the timing.
        # The period formula T = 2 * RF * C * ln(1 + 2*R2/R1) is a common one for symmetric output
        # Let's check for log validity
        log_argument = (1 + 2 * R2_ohms / R1_ohms) if R1_ohms > 0 else 0
        if log_argument <= 1:
            st.error("Invalid R1/R2 values. R1 must be positive and not lead to a log argument <= 1.")
            return None

        try:
            T = 2 * RF_ohms * C_farads * np.log(1 + 2 * R2_ohms / R1_ohms)
        except (ValueError, ZeroDivisionError):
            st.error("Error in calculating period. Check RF, C, R1, R2 values.")
            return None

        T_on = T / 2
        T_off = T / 2
        
        if T == 0 or np.isinf(T) or np.isnan(T):
            freq = 0.0
        else:
            freq = 1 / T
        
        C_amp = beta * amp_supply

        num_cycles = 5
        amp = amp_supply
    
        if freq == 0 or np.isinf(freq) or np.isnan(freq):
            sampling_rate = 10000
            total_duration = 0.01
            y_signal = np.full(int(sampling_rate * total_duration), 0.0)
            t_time = np.linspace(0, total_duration, int(sampling_rate * total_duration), endpoint=False)
            st.warning("No oscillation detected with current parameters. Output will be flat.")
        else:
            sampling_rate = max(100 * freq, 1000)
            total_duration = num_cycles / freq
            num_points = int(sampling_rate * total_duration)
            if num_points < 2: num_points = 2
            t_time = np.linspace(0, total_duration, num_points, endpoint=False)
            y_signal = amp * signal.square(2 * np.pi * freq * t_time)
    
        return {
            "RF_kohm": RF_kohm,
            "C_uF": C_uF,
            "R1_kohm": R1_kohm,
            "R2_kohm": R2_kohm,
            "Period_s": T,
            "T_on_s": T_on,
            "T_off_s": T_off,
            "Frequency_Hz": freq,
            "Output_Amplitude_V": amp,
            "Total_Duration_s": total_duration,
            "Capacitor_Threshold_V": C_amp,
            "y_signal": y_signal,
            "t_time": t_time
        }

    # --- CRO Display and Simulation Results ---
    with col2:
        st.header("Circuit Diagram")
        
        st.image("images/squarewavegenerator.png", caption="Square Wave Generator Circuit", use_container_width=True)
        
        st.subheader("CRO Display")
    
        sim_results = calculate_square_wave_parameters(RF_kohm, C_uF, R1_kohm, R2_kohm)
    
        if sim_results is not None:
            fig1, ax1 = plt.subplots(figsize=(6, 3), dpi=100)
            ax1.plot(sim_results["t_time"], sim_results["y_signal"], color='red')
            ax1.set_title(f"Output Signal\nFrequency: {sim_results['Frequency_Hz']:.2f} Hz, Period: {sim_results['Period_s']:.2e} s")
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Amplitude (V)")
            ax1.grid(True)
            ax1.set_facecolor("black")
            ax1.axhline(0, color='gray', linewidth=0.5)
            ax1.axvline(0, color='gray', linewidth=0.5)
            
            plot_ylim = sim_results["Output_Amplitude_V"] * 1.1 if sim_results["Output_Amplitude_V"] != 0 else 1.0
            ax1.set_ylim(-plot_ylim, plot_ylim)
            ax1.set_xlim(0, sim_results["Total_Duration_s"])
            ax1.tick_params(axis='x', colors='white')
            ax1.tick_params(axis='y', colors='white')
            
            ax1.text(0.02, 0.95, f'Amp: {sim_results["Output_Amplitude_V"]:.2f} V', transform=ax1.transAxes,
                      fontsize=8, color='white', verticalalignment='top')
            ax1.text(0.02, 0.85, f'Freq: {sim_results["Frequency_Hz"]:.2f} Hz', transform=ax1.transAxes,
                      fontsize=8, color='white', verticalalignment='top')
            st.pyplot(fig1)
    
            st.header("Simulation Results")
    
            if 'square_wave_history' not in st.session_state:
                st.session_state.square_wave_history = []
    
            if st.button("Log Current Results to Table", key="log_button_sq_wave"):
                new_entry = {
                    "RF (kΩ)": f"{sim_results['RF_kohm']:.2f}",
                    "C (µF)": f"{sim_results['C_uF']:.2f}",
                    "R1 (kΩ)": f"{sim_results['R1_kohm']:.2f}",
                    "R2 (kΩ)": f"{sim_results['R2_kohm']:.2f}",
                    "Period (T) (s)": f"{sim_results['Period_s']:.2e}",
                    "T_on (s)": f"{sim_results['T_on_s']:.2e}",
                    "T_off (s)": f"{sim_results['T_off_s']:.2e}",
                    "Amplitude (V)": f"{sim_results['Output_Amplitude_V']:.2f}",
                    "Duration (s)": f"{sim_results['Total_Duration_s']:.2e}",
                    "C_Amp (V)": f"{sim_results['Capacitor_Threshold_V']:.2f}"
                }
                st.session_state.square_wave_history.append(new_entry)
    
            if st.session_state.square_wave_history:
                df_history = pd.DataFrame(st.session_state.square_wave_history)
                st.dataframe(df_history, use_container_width=True)
    
            if st.button("Clear Table History", key="clear_table_button_sq_wave"):
                st.session_state.square_wave_history = []
                st.rerun()
        else:
            st.warning("Please adjust parameters to allow for oscillation.")

# --- Postlab Tab ---
with tab4:
    st.header("Postlab")
    st.markdown("""
    **Conclusion:**
    * Summarize your observations from the simulation regarding the effect of changing RF, C, R1, and R2 on the output frequency and amplitude.
    * Explain why this circuit is often called a "free-running" or "astable" multivibrator.
    * What would happen if the capacitor C was replaced by a short circuit? Explain the outcome.

    **Analysis:**
    * Using the formula, calculate the period and frequency of the square wave if $R_F = 20k\Omega$, $C = 0.05\mu F$, $R_1 = 10k\Omega$, and $R_2 = 10k\Omega$.
    * If you wanted to double the frequency of the output, what simple change could you make to the circuit's components?
    * How does the output amplitude of the square wave relate to the op-amp's power supply?
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