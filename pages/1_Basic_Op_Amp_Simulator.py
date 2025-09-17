# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 21:04:27 2025

@author: damo3
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import io # To capture Matplotlib plots as images

# --- Constants ---
CLIPPING_LIMIT = 15.0 # Define the clipping limit for output voltage

# --- Helper Functions ---
def get_actual_frequency(freq_val, unit):
    """Converts frequency value based on selected unit."""
    if unit == "kHz":
        return freq_val * 1e3
    elif unit == "MHz":
        return freq_val * 1e6
    else: # Hz
        return freq_val

def generate_waveform(amp, freq, wave_type, num_cycles=3):
    """Generates the specified waveform."""
    sampling_rate = 1000000
    
    if freq == 0:
        duration = 0.01
        t = np.linspace(0, duration * num_cycles, int(sampling_rate * duration * num_cycles), endpoint=False)
        y = np.zeros_like(t)
    else:
        period = 1 / freq
        total_duration = period * num_cycles
        num_points = int(sampling_rate * total_duration)
        if num_points < 1000:
            num_points = 1000
        t = np.linspace(0, total_duration, num_points, endpoint=False)
        
        if wave_type == "Sine wave":
            y = amp * np.sin(2 * np.pi * freq * t)
        elif wave_type == "Cosine wave":
            y = amp * np.cos(2 * np.pi * freq * t)
        elif wave_type == "Triangular wave":
            y = amp * signal.sawtooth(2 * np.pi * freq * t, width=0.5)
        elif wave_type == "Square wave":
            y = amp * signal.square(2 * np.pi * freq * t)
        else: # Default or no selection
            y = np.zeros_like(t)

    return y, t, amp, total_duration, freq

def get_amplifier_name(amp_type_value):
    """Returns human-readable amplifier name."""
    if amp_type_value == "Inverting Amplifier":
        return "Inverting"
    elif amp_type_value == "Non-Inverting Amplifier":
        return "Non-Inverting"
    elif amp_type_value == "Voltage Follower": 
        return "Buffer"
    return "N/A"

def calculate_amplifier_output(y_input, amp_input, R1_kohm, Rf_kohm, amplifier_type_name):
    """Calculates amplifier output based on type and resistances."""
    R1_val = R1_kohm * 1000
    Rf_val = Rf_kohm * 1000

    y_output = np.zeros_like(y_input)
    output_amplitude = 0
    phase_diff_deg = 0

    if amplifier_type_name == "Inverting Amplifier":
        if R1_val != 0:
            gain = -(Rf_val / R1_val)
            y_output = gain * y_input
            output_amplitude = abs(gain) * amp_input
            phase_diff_deg = 180 if amp_input != 0 else 0
        else:
            output_amplitude = 0
            y_output = np.zeros_like(y_input)
            phase_diff_deg = 0
    elif amplifier_type_name == "Non-Inverting Amplifier":
        if R1_val != 0:
            gain = 1 + (Rf_val / R1_val)
            y_output = gain * y_input
            output_amplitude = gain * amp_input
            phase_diff_deg = 0
        else: # R1 = 0, behaves as buffer
            gain = 1
            y_output = gain * y_input
            output_amplitude = gain * amp_input
            phase_diff_deg = 0
    elif amplifier_type_name == "Voltage Follower":
        gain = 1
        y_output = gain * y_input
        output_amplitude = amp_input
        phase_diff_deg = 0
    
    # --- Output Clipping Logic ---
    y_output = np.clip(y_output, -CLIPPING_LIMIT, CLIPPING_LIMIT)
    
    if np.all(y_output == 0):
        output_amplitude = 0
    else:
        output_amplitude = np.max(np.abs(y_output))
        
    return y_output, output_amplitude, phase_diff_deg

# --- Main App Layout ---
st.set_page_config(layout="wide", page_title="Op-Amp Lab Simulation")
st.title("Op-Amp Lab Simulator")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

with tab1:
    st.header("Prelab Tasks")
    st.markdown("""
    - **Objective:** To get familiar with the fundamental concepts of operational amplifiers (Op-Amps) and their basic configurations.
    - **Instructions:**
        1. Read through the "Theory" tab to understand the principles of Inverting, Non-Inverting, and Voltage Followers.
        2. Calculate the theoretical gain and output voltage for the following scenarios. You will compare these values to the simulation results later.
        - **Inverting Amplifier:**
            - $R_1 = 10k\Omega$, $R_f = 100k\Omega$, $V_{in} = 1V$
            - $R_1 = 20k\Omega$, $R_f = 50k\Omega$, $V_{in} = 2V$
        - **Non-Inverting Amplifier:**
            - $R_1 = 10k\Omega$, $R_f = 100k\Omega$, $V_{in} = 1V$
            - $R_1 = 20k\Omega$, $R_f = 50k\Omega$, $V_{in} = 2V$
    """)
    st.markdown("---")
    
 # --- MCQ Questions Section ---
    st.subheader("MCQ Questions")

    questions = [
        {
            "question": "What is the typical output impedance of an ideal operational amplifier?",
            "options": ["Infinite", "Zero", "Approximately 1 kΩ", "Approximately 10 kΩ"],
            "answer": "Zero",
            "explanation": "An ideal operational amplifier is characterized by zero output impedance, which means it can drive any load without a drop in output voltage."
        },
        {
            "question": "An inverting amplifier has R1 = 10 kΩ and Rf = 50 kΩ. What is its gain?",
            "options": ["5", "-5", "6", "-6"],
            "answer": "-5",
            "explanation": "The gain of an inverting amplifier is given by the formula  st.latex(" -\left(\frac{R_f}{R_1}\right)")"
        },
        {
            "question": "Which of the following amplifier configurations provides a unity gain (gain of 1)?",
            "options": ["Inverting Amplifier", "Non-Inverting Amplifier with R1=0", "Voltage Follower", "Non-Inverting Amplifier with Rf=0"],
            "answer": "Voltage Follower",
            "explanation": "A Voltage Follower is a special case of a non-inverting amplifier where the gain is exactly 1, meaning the output voltage follows the input voltage."
        }
    ]

    user_answers = {}
    for i, q in enumerate(questions):
        st.markdown(f"**Question {i+1}:** {q['question']}")
        user_answers[i] = st.radio(
            "Select your answer:",
            q["options"],
            key=f"q{i}_options"
        )
        st.markdown("---")

    if st.button("Submit Answers"):
        st.subheader("Results")
        for i, q in enumerate(questions):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            if user_answers[i] == q["answer"]:
                st.success(f"Correct! Your answer: {user_answers[i]}. The correct answer is: {q['answer']} 🎉")
            else:
                st.error(f"Incorrect. Your answer: {user_answers[i]}. The correct answer is: {q['answer']} ❌")
            st.info(f"**Explanation:** {q['explanation']}")
            st.markdown("---")

with tab2:
    st.subheader("Circuit Theory")
    st.write("This section provides a brief overview of the theoretical concepts behind the circuits you will be simulating.")
    st.markdown("#### The Operational Amplifier (Op-Amp)")
    st.write("An operational amplifier is a DC-coupled high-gain electronic voltage amplifier with a differential input and, usually, a single-ended output. A key characteristic of the ideal Op-Amp is that it has infinite input impedance and zero output impedance.")
    st.markdown("#### Inverting Amplifier")
    st.write("In this configuration, the input signal is applied to the inverting input terminal. The output voltage is out of phase with the input and its gain is determined by the ratio of the feedback resistor ($R_f$) to the input resistor ($R_1$).")
    st.image("images/invertingamplifier.png", caption="Inverting Amplifier Circuit", use_container_width=True)
    st.latex(r"V_{out} = -\left(\frac{R_f}{R_1}\right) V_{in}")
    
    st.markdown("#### Non-Inverting Amplifier")
    st.write("Here, the input signal is applied to the non-inverting input terminal. The output voltage is in phase with the input and its gain is given by the formula:")
    st.image("images/Noninvertingamplifier.png", caption="Non-Inverting Amplifier Circuit", use_container_width=True)
    st.latex(r"V_{out} = \left(1 + \frac{R_f}{R_1}\right) V_{in}")
    
    st.markdown("#### Buffer Amplifier (Voltage Follower)")
    st.write("A buffer amplifier is a non-inverting amplifier with a gain of 1. It is used to isolate one stage of a circuit from another, providing high input impedance and low output impedance.")
    st.image("images/voltagefollower.png", caption="Buffer Amplifier (Voltage Follower) Circuit", use_container_width=True)
    st.latex(r"V_{out} = V_{in}")

with tab3:
    st.header("Simulation")
    
    # Create columns for layout
    col1, col2, col3 = st.columns([1, 1, 2]) # Function Generator, Amplifier, CRO Displays
    
    with col1:
        st.header("Function Generator")
        
        wave_type = st.radio(
            "Select Waveform:",
            ("Sine wave", "Cosine wave", "Triangular wave", "Square wave", "None"),
            index=0, # Default to Sine wave
            key="wave_type_radio"
        )
    
        amplitude = st.slider(
            "Amplitude (V)",
            min_value=0.0, max_value=5.0, value=1.0, step=0.01,
            format="%.2f V",
            key="amplitude_slider"
        )
    
        st.write("Frequency")
        freq_col1, freq_col2 = st.columns([2, 1])
        with freq_col1:
            frequency_value = st.slider(
                "Frequency Value",
                min_value=0.0, max_value=1100.0, value=100.0, step=0.1,
                label_visibility="collapsed", # Hide default label to combine with units
                key="frequency_slider"
            )
     #   with freq_col2:
            freq_unit = st.radio(
                "Unit",
                ("Hz", "kHz", "MHz"),
                index=0, # Default to Hz
                horizontal=True,
                label_visibility="collapsed", # Hide default label
                key="freq_unit_radio"
            )
        
        actual_frequency = get_actual_frequency(frequency_value, freq_unit)
    
    with col2:
        st.header("Amplifier Settings")
        
        amplifier_type = st.radio(
            "Select Amplifier Type:",
            ("Inverting Amplifier", "Non-Inverting Amplifier", "Voltage Follower", "None"),
            index=0, # Default to Inverting Amplifier
            key="amp_type_radio"
        )
        
        # Determine if inputs should be disabled
        disable_inputs = (amplifier_type == "Voltage Follower")
        
        # Set default values for voltage follower but disable the widgets
        r1_default = 10.0
        rf_default = 100.0

        r1_kohm = st.number_input(
            "Input Resistance (R1) (kΩ)",
            min_value=0.01,
            value=r1_default,
            step=0.1,
            format="%.2f",
            key="r1_input",
            disabled=disable_inputs
        )
    
        rf_kohm = st.number_input(
            "Feedback Resistance (Rf) (kΩ)",
            min_value=0.01,
            value=rf_default,
            step=0.1,
            format="%.2f",
            key="rf_input",
            disabled=disable_inputs
        )
    
    # Use a state variable for the simulation results table
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = []
    if 'row_id_counter' not in st.session_state:
        st.session_state.row_id_counter = 0
    
    # --- Simulation Logic and Plotting (triggered when inputs change) ---
    
    # Generate input waveform
    y_input, t, amp_input, total_duration, input_freq = generate_waveform(amplitude, actual_frequency, wave_type)
    
    # Use fixed values for Voltage Follower to ensure correct calculation
    if amplifier_type == "Voltage Follower":
        r1_kohm_calc = float('inf')  # Represents R1 as an open circuit
        rf_kohm_calc = 0.0          # Represents Rf as a short circuit
    else:
        r1_kohm_calc = r1_kohm
        rf_kohm_calc = rf_kohm
    
    # Calculate output waveform
    y_output, output_amplitude, phase_diff_deg = calculate_amplifier_output(
        y_input, amp_input, r1_kohm_calc, rf_kohm_calc, amplifier_type
    )
    
    with col3:
        st.header(" Circuit Diagram")
        
        # --- Code to display the circuit diagram is now here ---
      
        
        if amplifier_type == "Inverting Amplifier":
            st.image("images/invertingamplifier.png", caption="Inverting Amplifier Circuit", use_container_width=True)
        elif amplifier_type == "Non-Inverting Amplifier":
            st.image("images/Noninvertingamplifier.png", caption="Non-Inverting Amplifier Circuit", use_container_width=True)
        elif amplifier_type == "Voltage Follower":
            st.image("images/voltagefollower.png", caption="Buffer Amplifier (Voltage Follower) Circuit", use_container_width=True)
        else:
            st.info("Select an amplifier type to display its circuit diagram.")
    
        
        st.markdown("---")
        st.subheader("CRO Waveforms")
        
        
        
    

        # New layout for combined and output plots

 # Plot 1: Input Signal (Top Plot)
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    ax1.plot(t, y_input, color='lime')
    ax1.set_facecolor("black")
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
    ax1.set_ylim(-amplitude * 1.5 if amplitude > 0 else -1, amplitude * 1.5 if amplitude > 0 else 1)
    ax1.set_xlim(0, total_duration)
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.set_title("Input Waveform", color='black') # Changed title
    if amplitude != 0:
        ax1.text(0.02, 0.95, f'Amplitude: {amplitude:.2f} V', transform=ax1.transAxes, 
                 fontsize=10, color='white', verticalalignment='top')
    st.pyplot(fig1)
    plt.close(fig1)

    # Plot 2: Output Signal (Right-hand side)
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.plot(t, y_output, color='cyan')
    ax2.set_facecolor("black")
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
    plot_ylim = max(output_amplitude * 1.2, 1.0)
    ax2.set_ylim(-plot_ylim, plot_ylim)
    ax2.set_xlim(0, total_duration)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    ax2.set_title("Output Waveform", color='black') # Changed title

    amplitude_display_text = f'Amplitude: {output_amplitude:.2f} V'
    if abs(output_amplitude - CLIPPING_LIMIT) < 0.01 and amplitude > 0:
        amplitude_display_text += ' (Clipped)'
    elif output_amplitude == 0 and amp_input != 0 and amplifier_type != "None":
        amplitude_display_text += ' (No Output)'

    ax2.text(0.02, 0.95, amplitude_display_text, transform=ax2.transAxes,
             fontsize=10, color='white', verticalalignment='top')
    st.pyplot(fig2)
    plt.close(fig2)


    fig_combined, ax_combined = plt.subplots(figsize=(6, 3))
    ax_combined.plot(t, y_input, color='lime', label='Input (Ch 1)')
    ax_combined.plot(t, y_output, color='cyan', label='Output (Ch 2)')
    ax_combined.set_facecolor("black")
    ax_combined.axhline(0, color='gray', linewidth=0.5)
    ax_combined.axvline(0, color='gray', linewidth=0.5)
    max_combined_amp = max(amplitude * 1.5, output_amplitude * 1.2, 1.0)
    ax_combined.set_ylim(-max_combined_amp, max_combined_amp)
    ax_combined.set_xlim(0, total_duration)
    ax_combined.tick_params(axis='x', colors='white')
    ax_combined.tick_params(axis='y', colors='white')
    ax_combined.set_title("Combined Waveform", color='black') # Changed title
    ax_combined.legend(loc='upper right', facecolor='darkgray', edgecolor='white')
    st.pyplot(fig_combined)
    plt.close(fig_combined)

        
    
    # --- Simulation Results Table ---
    st.markdown("---") # Horizontal line for separation
    st.header("Simulation Results")
    
    # Button to log current simulation
    if st.button("Log Current Simulation"):
        st.session_state.row_id_counter += 1
        new_entry = {
            "#": st.session_state.row_id_counter,
            "Amplifier Type": get_amplifier_name(amplifier_type),
            "R1 (kΩ)": "N/A" if disable_inputs else f"{r1_kohm:.1f}",
            "Rf (kΩ)": "N/A" if disable_inputs else f"{rf_kohm:.1f}",
            "Input Amp (V)": f"{amp_input:.2f}",
            "Input Freq (Hz)": f"{input_freq:.1f}",
            "Output Amp (V)": f"{output_amplitude:.2f}",
            "Output Freq (Hz)": f"{input_freq:.1f}", # Output frequency is generally same as input
            "Phase Diff (deg)": f"{phase_diff_deg:.1f}"
        }
        st.session_state.simulation_results.append(new_entry)
    
    # Display the table
    if st.session_state.simulation_results:
        st.dataframe(st.session_state.simulation_results, hide_index=True)
    else:
        st.info("No simulations logged yet. Adjust parameters and click 'Log Current Simulation'.")
    
    # Button to clear table
    if st.button("Clear Log"):
        st.session_state.simulation_results = []
        st.session_state.row_id_counter = 0
        st.rerun() # Rerun the app to clear the displayed table

with tab4:
    st.header("Postlab Questions")
    st.markdown("""
    - **Instructions:** Use the logged simulation results to answer the following questions.
    1. Compare the theoretical gain values you calculated in the Prelab to the output amplitude values from the simulation. Are they the same? If not, what factors might cause the difference (e.g., clipping)?
    2. Explain the phase relationship between the input and output waveforms for each amplifier type.
    3. What is the primary purpose of a Voltage Follower, and how do your simulation results for the Voltage Follower demonstrate this?
    4. What happens to the output waveform when the gain is too high for a given input amplitude? How does the "Clipped" message in the simulation confirm this?
    """)
    
with tab5:
    st.header("Feedback")
    st.markdown("""
    Your feedback is valuable to us! Please provide your comments on the simulator.
    """)
    st.write("We would love to hear your thoughts on this simulator.")
    st.text_input("Your Name and Registration number")
    st.slider("How would you rate this simulator?", 1, 5)
    st.text_area("Your comments...")
    st.button("Submit Feedback")

   