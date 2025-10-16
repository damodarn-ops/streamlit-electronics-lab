# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 14:14:54 2025

@author: damo3
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.integrate import cumulative_trapezoid
import pandas as pd

st.set_page_config(layout="wide", page_title="Integrator/Differentiator Simulator")

st.title("Integrator/Differentiator Simulator")

# --- Layout with Columns ---
col1, col2, col3 = st.columns([1, 1, 2]) # Adjust column ratios for better layout

with col1:
    st.header("Function Generator")
    wave_type = st.radio(
        "Select Waveform",
        ("Sine wave", "Cosine wave", "Triangular wave", "Square wave"),
        index=0, # Default to Sine wave
        key="wave_type_radio"
    )
    # Map string wave type to integer value for compatibility with existing logic
    wave_type_map = {"Sine wave": 1, "Cosine wave": 2, "Triangular wave": 3, "Square wave": 4}
    selected_wave_type_int = wave_type_map[wave_type]

    amplitude = st.slider("Amplitude (V)", 0.0, 5.0, 1.0, 0.001, key="amplitude_slider")

    st.subheader("Frequency")
    freq_val = st.slider("Frequency Value", 0.0, 1100.0, 100.0, 0.001, key="frequency_slider")
    current_freq_unit = st.radio(
        "Frequency Unit",
        ("Hz", "kHz", "MHz"),
        index=0, # Default to Hz
        horizontal=True,
        key="freq_unit_radio"
    )

    def get_actual_frequency(freq_val_local, unit_local):
        if unit_local == "kHz":
            return freq_val_local * 1e3
        elif unit_local == "MHz":
            return freq_val_local * 1e6
        else: # Hz
            return freq_val_local

    actual_frequency = get_actual_frequency(freq_val, current_freq_unit)

with col2:
    st.header("Integrator/Differentiator")
    amplifier_type = st.radio(
        "Select Circuit Type",
        ("Integrator", "Differentiator"),
        index=0, # Default to Integrator
        key="amp_type_radio"
    )
    # Map string amplifier type to integer value
    amplifier_type_map = {"Integrator": 1, "Differentiator": 2}
    selected_amplifier_type_int = amplifier_type_map[amplifier_type]

    R_in_kohm = st.number_input(
        "Resistance (R) (kΩ)",
        min_value=0.001, # R cannot be zero
        value=10.0,
        step=0.1,
        format="%.3f",
        key="R_input"
    )
    C_f_uF = st.number_input(
        "Capacitance (C) (µF)",
        min_value=0.0001, # C cannot be zero
        value=0.1,
        step=0.001,
        format="%.5f",
        key="C_input"
    )

    st.markdown("---")
    st.write("Developed by DAMODAR")


# --- Core Simulation Logic ---
# These functions are largely preserved from your Tkinter code
def generate_waveform(amp, freq, wave_type_val, num_cycles=3):
    if freq == 0:
        sampling_rate = 10000
    else:
        sampling_rate = max(100 * freq, 1000)

    total_duration = num_cycles / freq if freq != 0 else 0.01

    num_points = int(sampling_rate * total_duration)
    if num_points < 2:
        num_points = 2

    t = np.linspace(0, total_duration, num_points, endpoint=False)

    if freq == 0:
        y = np.full_like(t, amp)
    elif wave_type_val == 1:
        y = amp * np.sin(2 * np.pi * freq * t)
    elif wave_type_val == 2:
        y = amp * np.cos(2 * np.pi * freq * t)
    elif wave_type_val == 3:
        y = amp * signal.sawtooth(2 * np.pi * freq * t, width=0.5)
    elif wave_type_val == 4:
        y = amp * signal.square(2 * np.pi * freq * t)
    else:
        y = np.zeros_like(t)

    return y, t, amp, total_duration, freq

def get_amplifier_name(amp_type_value):
    if amp_type_value == 1:
        return "Integrator"
    elif amp_type_value == 2:
        return "Differentiator"
    return "N/A"

def simulate_circuit(amp_input, actual_frequency, selected_wave_type_int,
                     selected_amplifier_type_int, R_in_kohm, C_f_uF):
    y_input, t, amp_input_actual, total_duration, input_freq = generate_waveform(
        amp_input, actual_frequency, selected_wave_type_int
    )

    R_in_ohms = R_in_kohm * 1000
    C_f_farads = C_f_uF * 1e-6

    y_output = np.zeros_like(y_input)
    output_amplitude = 0
    phase_diff_deg = 0
    output_freq = input_freq
    amplifier_name = get_amplifier_name(selected_amplifier_type_int)
    
    # Define the clipping limit (e.g., +/- 15V for a typical op-amp)
    clipping_limit = 15.0

    if selected_amplifier_type_int == 1:  # Integrator
        if R_in_ohms == 0 or C_f_farads == 0:
            st.warning("Input R or Feedback C cannot be zero for Integrator. Output will be zero.")
            y_output = np.zeros_like(y_input)
            output_amplitude = 0
        else:
            dt = t[1] - t[0] if len(t) > 1 else 0
            if dt > 0:
                y_integrated = cumulative_trapezoid(y_input, dx=dt, initial=0)
                gain_factor = -1 / (R_in_ohms * C_f_farads)
                y_output = gain_factor * y_integrated

                if input_freq > 0 and (selected_wave_type_int == 1 or selected_wave_type_int == 2):
                    phase_diff_deg = 90
                elif input_freq == 0:
                    y_output = gain_factor * y_input * t # Integration of constant is linear
                    phase_diff_deg = 0
                else:
                    phase_diff_deg = "N/A"
            else:
                y_output = np.zeros_like(y_input)

    elif selected_amplifier_type_int == 2:  # Differentiator
        if C_f_farads == 0 or R_in_ohms == 0: # C_in, R_f
            st.warning("Input C or Feedback R cannot be zero for Differentiator. Output will be zero.")
            y_output = np.zeros_like(y_input)
            output_amplitude = 0
        else:
            dt = t[1] - t[0] if len(t) > 1 else 0
            if dt > 0:
                y_differentiated = np.diff(y_input) / dt
                t_differentiated = (t[:-1] + t[1:]) / 2

                gain_factor = -(R_in_ohms * C_f_farads) # R_f * C_in from op-amp differentiator setup
                y_output_temp = gain_factor * y_differentiated
                y_output = np.interp(t, t_differentiated, y_output_temp)

                if input_freq > 0 and (selected_wave_type_int == 1 or selected_wave_type_int == 2):
                    phase_diff_deg = -90
                elif input_freq == 0:
                    y_output = np.zeros_like(y_input)
                    phase_diff_deg = 0
                else:
                    phase_diff_deg = "N/A"
            else:
                y_output = np.zeros_like(y_input)
    
    # Apply clipping after calculation
    y_output = np.clip(y_output, -clipping_limit, clipping_limit)

    if np.all(y_output == 0):
        output_amplitude = 0
    else:
        output_amplitude = np.max(np.abs(y_output))
        
    amplitude_display_text = f'Amp: {output_amplitude:.2f} V'
    if abs(output_amplitude - clipping_limit) < 0.01 and amp_input > 0:
        amplitude_display_text += ' (Clipped)'
    elif output_amplitude == 0 and amp_input !=0:
        amplitude_display_text += ' (No Output)'

    return y_input, y_output, t, amp_input_actual, total_duration, input_freq, \
           output_amplitude, phase_diff_deg, amplifier_name, amplitude_display_text

# --- CRO Displays ---
with col3:
    st.header("CRO Displays")

    y_input, y_output, t, amp_input, total_duration, input_freq, \
    output_amplitude, phase_diff_deg, amplifier_name, output_amp_display_text = simulate_circuit(
        amplitude, actual_frequency, selected_wave_type_int,
        selected_amplifier_type_int, R_in_kohm, C_f_uF
    )

    # CRO Channel 1 - Input Signal
    fig1, ax1 = plt.subplots(figsize=(3, 2), dpi=100)
    ax1.plot(t, y_input, color='lime')
    ax1.set_facecolor("black")
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
    ax1.set_ylim(-amp_input * 1.5 if amp_input != 0 else -1, amp_input * 1.5 if amp_input != 0 else 1)
    ax1.set_xlim(0, total_duration)
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.set_title("Ch 1: Input Signal", color='white', fontsize=10)
    ax1.text(0.02, 0.95, f'Amp: {amp_input:.2f} V', transform=ax1.transAxes,
             fontsize=8, color='white', verticalalignment='top')
    st.pyplot(fig1)

    # CRO Channel 2 - Output Signal
    fig2, ax2 = plt.subplots(figsize=(3, 2), dpi=100)
    ax2.plot(t, y_output, color='cyan')
    ax2.set_facecolor("black")
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
    plot_ylim = max(output_amplitude * 1.2, 1.0)
    ax2.set_ylim(-plot_ylim, plot_ylim)
    ax2.set_xlim(0, total_duration)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    ax2.set_title("Ch 2: Output Signal", color='white', fontsize=10)
    ax2.text(0.02, 0.95, output_amp_display_text, transform=ax2.transAxes,
             fontsize=8, color='white', verticalalignment='top')
    st.pyplot(fig2)

    # Combined Plot (Channel 1 & 2)
    fig_combined, ax_combined = plt.subplots(figsize=(6, 3), dpi=100)
    ax_combined.plot(t, y_input, color='lime', label='Input (Ch 1)')
    ax_combined.plot(t, y_output, color='cyan', label='Output (Ch 2)')
    ax_combined.set_facecolor("black")
    ax_combined.axhline(0, color='gray', linewidth=0.5)
    ax_combined.axvline(0, color='gray', linewidth=0.5)
    max_combined_amp = max(amp_input * 1.5, plot_ylim)
    ax_combined.set_ylim(-max_combined_amp, max_combined_amp)
    ax_combined.set_xlim(0, total_duration)
    ax_combined.tick_params(axis='x', colors='white')
    ax_combined.tick_params(axis='y', colors='white')
    ax_combined.set_title("Combined View (Ch 1 & Ch 2)", color='white', fontsize=10)
    ax_combined.legend(loc='upper right', fontsize=8, facecolor='darkgray', edgecolor='white')
    st.pyplot(fig_combined)

# --- Dynamic Parameters Table ---
st.header("Simulation Results")

# Initialize session state for history if it doesn't exist
if 'simulation_history' not in st.session_state:
    st.session_state.simulation_history = []

# Button to log the current result to the table
if st.button("Log Current Results to Table", key="log_button"):
    new_entry = {
        "#": len(st.session_state.simulation_history) + 1,
        "Integrator/Differentiator": amplifier_name,
        "R (kΩ)": f"{R_in_kohm:.1f}",
        "C (µF)": f"{C_f_uF:.3f}",
        "Input Amp (V)": f"{amp_input:.2f}",
        "Input Freq (Hz)": f"{input_freq:.1f}",
        "Output Amp (V)": f"{output_amplitude:.2f}",
        "Output Freq (Hz)": f"{input_freq:.1f}", # Output freq is usually same as input for linear circuits
        "Phase Diff (deg)": f"{phase_diff_deg:.1f}" if isinstance(phase_diff_deg, (int, float)) else phase_diff_deg
    }
    st.session_state.simulation_history.append(new_entry)

# Display the history as a DataFrame
if st.session_state.simulation_history:
    df_history = pd.DataFrame(st.session_state.simulation_history)
    st.dataframe(df_history, use_container_width=True)

# Button to clear the table
if st.button("Clear Table History", key="clear_table_button"):
    st.session_state.simulation_history = []
    st.rerun() # Rerun to clear the displayed table immediately