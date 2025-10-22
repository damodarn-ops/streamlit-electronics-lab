# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:18:52 2025

@author: damo3
"""

# pages/3_Precision_Rectifier.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

st.set_page_config(layout="wide", page_title="Precision Rectifier")

# Create tabs for different sections of the page.
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

import streamlit as st

import streamlit as st

# --- Tab 1: Prelab ---
with tab1:
    st.header("Prelab: Precision Rectifier")
    st.markdown("""
    ### Objective
    The objective of this lab is to understand the operation of precision half-wave and full-wave rectifiers using operational amplifiers (op-amps). We will explore how op-amps overcome the forward voltage drop of diodes, allowing for rectification of very low-amplitude signals.

  
    """)
   

    # --- Add the MCQ section here ---
    st.markdown("---")
    st.subheader("Quick Check: Test Your Knowledge")

    # Define the list of questions, options, and correct answers
    mcq_list = [
        {
            "question": "1. What is the primary function of a precision rectifier?",
            "options": [
                " To rectify low-amplitude AC signals by using an op-amp to overcome the diode's forward voltage drop.",
                " To amplify low-frequency signals without distortion.",
                " To convert a DC signal into a rectified AC signal.",
                " To provide a stable voltage reference for a circuit."
            ],
            "correct_option_index": 0,
            "explanation":  "A. To rectify low-amplitude AC signals by using an op-amp to overcome the diode's forward voltage drop."
        },
        {
            "question": "2. In a precision half-wave rectifier, the op-amp essentially places the diode inside the feedback loop. What is the benefit of this arrangement?",
            "options": [
                " It increases the output impedance of the circuit.",
                " It makes the circuit insensitive to temperature changes.",
                " The op-amp's gain effectively eliminates the diode's forward voltage drop from the output signal.",
                " It provides a constant current source to the diode."
            ],
            "correct_option_index": 2,
            "explanation":  "The op-amp's gain effectively eliminates the diode's forward voltage drop from the output signal."
        },
        {
            "question": "3. Which of the following components is NOT typically found in a basic precision half-wave rectifier circuit?",
            "options": [
                " Op-amp",
                " Diode",
                " Resistors",
                " Inductor"
            ],
            "correct_option_index": 3,
            "explanation":  "Inductor"
        },
        {
            "question": "4. For a precision full-wave rectifier, how does the circuit handle the negative half of the input sinusoidal signal?",
            "options": [
                " It simply blocks the negative half-cycle.",
                " It inverts the negative half-cycle and adds it to the positive half-cycle.",
                " It converts the negative half-cycle to a DC voltage.",
                " It rectifies it into a negative half-wave output."
            ],
            "correct_option_index": 0,
            "explanation":  "It inverts the negative half-cycle and adds it to the positive half-cycle."
        },
        {
        "question": "5. An ideal op-amp used in a precision rectifier has what effect on the rectification threshold (the voltage required to 'turn on' the rectification)?",
        "options": [
            " It raises the threshold to the op-amp's supply voltage.",
            " It lowers the threshold to the diode's forward voltage ($V_D$).",
            " It makes the threshold practically zero volts.",
            " It doubles the threshold voltage."
        ],
        "correct_option_index": 2,
        "explanation":  "It makes the threshold practically zero volts."
    }

    ]

   
    st.markdown("---")
    st.subheader("Multiple Choice Questions (MCQ)")
    st.text_input("Your Name",key="p1")
    user_answers = {}
    for i, mcq in enumerate(mcq_list):
        user_answers[i] = st.radio(mcq["question"], mcq["options"], key=f"mcq_{i}")

    if st.button("Submit Answers", key="submit_mcq"):
        st.subheader("Results")
        all_correct = True
        for i, mcq in enumerate(mcq_list):
            correct_answer = mcq["options"][mcq["correct_option_index"]]
            if user_answers[i] == correct_answer:
                st.success(f"**Question {i+1}: Correct!** ✅")
                st.markdown(f"**Explanation:** {mcq['explanation']}")
            else:
                st.error(f"**Question {i+1}: Incorrect.** ❌")
                st.markdown(f"**Correct Answer:** {correct_answer}")
                st.markdown(f"**Explanation:** {mcq['explanation']}")
                all_correct = False
        
        if all_correct:
            st.balloons()
            st.info("You've answered all questions correctly! You are ready to proceed to the simulation. 🎉")
        else:
            st.warning("Please review the theory and try again. 🤔")
        
# --- Tab 2: Theory ---
with tab2:
    st.header("Theory: The Precision Rectifier")
    st.markdown("""
    A **precision rectifier**, also known as a superdiode, is an electronic circuit that functions as a rectifier for very small input voltages. Unlike a conventional diode rectifier, which has a forward voltage drop of approximately 0.7V for silicon diodes, a precision rectifier uses an operational amplifier (op-amp) to effectively eliminate this voltage drop.

    ### Precision Half-Wave Rectifier
    This circuit rectifies only one half of the input AC signal. The op-amp is configured in a way that when the input is positive, the output diode (D2) conducts, and the op-amp's output is an amplified version of the input, effectively rectifying the signal. When the input is negative, the op-amp's output goes to its negative rail, and the diode D2 is reverse-biased, causing the output voltage to be zero.

    

    ### Precision Full-Wave Rectifier
    This circuit rectifies both the positive and negative halves of the input AC signal. The negative half of the input is inverted and then added to the positive half, resulting in a rectified output that contains the rectified version of the entire input signal. The output frequency is double the input frequency.

    

    ### Key Differences:
    -   **Half-Wave:** Rectifies only positive half-cycles. Output frequency is the same as input frequency.
    -   **Full-Wave:** Rectifies both half-cycles. Output frequency is double the input frequency.

    ### Ideal vs. Real-world Op-amps
    -   **Ideal Op-amp:** No input offset voltage, infinite input impedance, zero output impedance, infinite gain, and infinite bandwidth. In this ideal case, the rectification is perfect with no voltage drop.
    -   **Real-world Op-amp:** Has limitations such as a small voltage drop, input offset voltage, finite bandwidth, and slew rate. These factors can affect the precision and performance of the rectifier, especially at high frequencies.
    """)

# --- Tab 3: Simulation ---
with tab3:
    st.header("Precision Rectifier Simulator")

    # --- Layout with Columns ---
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.header("Function Generator")
        wave_type = st.radio(
            "Select Waveform",
            ("Sine wave", "Cosine wave", "Triangular wave", "Square wave"),
            index=0,
            key="wave_type_radio_rectifier"
        )
        wave_type_map = {"Sine wave": 1, "Cosine wave": 2, "Triangular wave": 3, "Square wave": 4}
        selected_wave_type_int = wave_type_map[wave_type]

        amplitude = st.slider("Amplitude (V)", 0.0, 5.0, 1.0, 0.001, key="amplitude_slider_rectifier")

        st.subheader("Frequency")
        freq_val = st.slider("Frequency Value", 0.0, 1100.0, 100.0, 0.001, key="frequency_slider_rectifier")
        current_freq_unit = st.radio(
            "Frequency Unit",
            ("Hz", "kHz", "MHz"),
            index=0,
            horizontal=True,
            key="freq_unit_radio_rectifier"
        )

        def get_actual_frequency(freq_val_local, unit_local):
            if unit_local == "kHz":
                return freq_val_local * 1e3
            elif unit_local == "MHz":
                return freq_val_local * 1e6
            else:
                return freq_val_local

        actual_frequency = get_actual_frequency(freq_val, current_freq_unit)

    with col2:
        st.header("Precision Rectifier Type")
        rectifier_type = st.radio(
            "Select Rectifier Type",
            ("Precision Half Wave Rectifier", "Precision Full Wave Rectifier"),
            index=0,
            key="rectifier_type_radio"
        )
        rectifier_type_map = {"Precision Half Wave Rectifier": 1, "Precision Full Wave Rectifier": 2}
        selected_rectifier_type_int = rectifier_type_map[rectifier_type]

        st.markdown("---")
        st.write("Developed by DAMODAR")

    # --- Core Simulation Logic ---
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

    def get_rectifier_name(rectifier_type_value):
        if rectifier_type_value == 1:
            return "Half Wave Rectifier"
        elif rectifier_type_value == 2:
            return "Full Wave Rectifier"
        return "N/A"

    def simulate_rectifier_circuit(amp_input, actual_frequency, selected_wave_type_int, selected_rectifier_type_int):
        y_input, t, amp_input_actual, total_duration, input_freq = generate_waveform(
            amp_input, actual_frequency, selected_wave_type_int
        )

        y_output = np.copy(y_input)
        output_amplitude = 0
        phase_diff_deg = 0
        
        input_time_ms = (1 / input_freq) * 1000 if input_freq != 0 else 0
        output_freq = input_freq
        output_time_ms = input_time_ms
        rectifier_name = get_rectifier_name(selected_rectifier_type_int)

        if selected_rectifier_type_int == 1:
            y_output[y_output < 0] = 0
        elif selected_rectifier_type_int == 2:
            y_output = np.abs(y_output)
            output_freq = 2 * input_freq
            output_time_ms = (1 / output_freq) * 1000 if output_freq != 0 else 0

        clipping_limit = 15.0
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

        return y_input, y_output, t, amp_input_actual, total_duration, input_freq, input_time_ms, \
               output_amplitude, output_freq, output_time_ms, phase_diff_deg, rectifier_name, amplitude_display_text

    with col3:
        st.header(" Circuit Diagram")
        if rectifier_type == "Precision Half Wave Rectifier":
            st.image("images/precisionhalfwaverectifier.png", caption="Half Wave Rectifier Circuit", width='stretch')
        elif rectifier_type == "Precision Full Wave Rectifier":
            st.image("images/precisionfullwaverectifier.png", caption="Full Wave Rectifier Circuit", width='stretch')
        
        
       
        
    st.header("CRO Displays")
    st.text_input("Your Name",key="p2")
 # Create three columns *outside* the col1/col2/col3 definition to span the full width
    plot_col1, plot_col2, plot_col3 = st.columns(3) 
    y_input, y_output, t, amp_input, total_duration, input_freq, input_time_ms, \
        output_amplitude, output_freq, output_time_ms, phase_diff_deg, rectifier_name, output_amp_display_text = simulate_rectifier_circuit(
            amplitude, actual_frequency, selected_wave_type_int, selected_rectifier_type_int
        )

    fig1, ax1 = plt.subplots(figsize=(3, 2), dpi=100)
    ax1.plot(t, y_input, color='lime')
    ax1.set_facecolor("black")
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
    ax1.set_ylim(-amp_input * 1.5 if amp_input != 0 else -1, amp_input * 1.5 if amp_input != 0 else 1)
    ax1.set_xlim(0, total_duration)
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.set_title("Ch 1: Input Signal", color='black', fontsize=10)
    ax1.text(0.02, 0.95, f'Amp: {amp_input:.2f} V', transform=ax1.transAxes,
                     fontsize=8, color='white', verticalalignment='top')
    with plot_col1: # Display fig1 in the first plot column    
            st.pyplot(fig1)

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
    ax2.set_title("Ch 2: Output Signal", color='black', fontsize=10)
    ax2.text(0.02, 0.95, output_amp_display_text, transform=ax2.transAxes,
                     fontsize=8, color='white', verticalalignment='top')
    with plot_col2: # Display fig2 in the second plot column     
         st.pyplot(fig2)

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
    ax_combined.set_title("Combined View (Ch 1 & Ch 2)", color='black', fontsize=10)
    ax_combined.legend(loc='upper right', fontsize=8, facecolor='darkgray', edgecolor='white')
    with plot_col3: # Display combined_fig in the third plot column     
         st.pyplot(fig_combined)

    st.header("Simulation Results")
    if 'simulation_history_rectifier' not in st.session_state:
        st.session_state.simulation_history_rectifier = []

    if st.button("Log Current Results to Table", key="log_button_rectifier"):
        new_entry = {
            "#": len(st.session_state.simulation_history_rectifier) + 1,
            "Precision Rectifier": rectifier_name,
            "Input Amp (V)": f"{amp_input:.2f}",
            "Input Freq (Hz)": f"{input_freq:.1f}",
            "Input Time period (ms)": f"{input_time_ms:.3f}",
            "Output Amp (V)": f"{output_amplitude:.2f}",
            "Output Freq (Hz)": f"{output_freq:.1f}",
            "Output Time period (ms)": f"{output_time_ms:.4f}",
            "Phase Diff (deg)": f"{phase_diff_deg:.1f}"
        }
        st.session_state.simulation_history_rectifier.append(new_entry)

    if st.session_state.simulation_history_rectifier:
        df_history = pd.DataFrame(st.session_state.simulation_history_rectifier)
        st.dataframe(df_history, width='stretch')

    if st.button("Clear Table History", key="clear_table_button_rectifier"):
        st.session_state.simulation_history_rectifier = []
        st.rerun()

# --- Tab 4: Postlab ---
# --- Tab 4: Postlab ---
with tab4:
    st.header("Postlab: Analysis and Conclusion")
    st.text_input("Your Name",key="p3")
    st.markdown("""
    **Instructions:** Use the simulation results you logged to the table to answer the following questions.
    """)
    st.subheader("Question 1: Observations")
    st.write("Describe the key differences you observed between the output of the precision half-wave rectifier and the precision full-wave rectifier.")
    st.text_area("Your Answer for Q1", height=100, key="postlab_rectifier_q1")
    
    st.subheader("Question 2: Amplitude Analysis")
    st.write("What happened to the output waveform's amplitude when the input signal's amplitude was changed?")
    st.text_area("Your Answer for Q2", height=100, key="postlab_rectifier_q2")

    st.subheader("Question 3: Frequency Analysis")
    st.write("How did the output waveform's frequency change with respect to the input frequency for both rectifier types? Use the logged data in the simulation table to support your answer.")
    st.text_area("Your Answer for Q3", height=100, key="postlab_rectifier_q3")
    
    st.subheader("Conclusion")
    st.write("Based on your observations and the logged simulation data, write a brief conclusion about the operation of precision rectifiers.")
    st.text_area("Your Conclusion", height=200, key="postlab_rectifier_conclusion")

# --- Tab 5: Feedback ---
with tab5:
    st.header("Feedback")
    st.write("We would eager to hear your thoughts on this simulator.")
    st.text_input("Your Name")
    st.text_input("Registration number/Faculty ID")
    st.slider("How would you rate this simulator?(best -5)", 1, 5)
    st.markdown("""
        We appreciate your feedback! Please let us know if you found this simulator useful and how we can improve it.
    """)
    st.text_area("Your Feedback", height=200, key="feedback_text")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")