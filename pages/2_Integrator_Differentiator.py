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

# --- Create tabs for the app sections ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

# --- Core Simulation Logic (defined outside tabs for scope) ---
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
                    y_output = gain_factor * y_input * t
                    phase_diff_deg = 0
                else:
                    phase_diff_deg = "N/A"
            else:
                y_output = np.zeros_like(y_input)

    elif selected_amplifier_type_int == 2:  # Differentiator
        if C_f_farads == 0 or R_in_ohms == 0:
            st.warning("Input C or Feedback R cannot be zero for Differentiator. Output will be zero.")
            y_output = np.zeros_like(y_input)
            output_amplitude = 0
        else:
            dt = t[1] - t[0] if len(t) > 1 else 0
            if dt > 0:
                y_differentiated = np.diff(y_input) / dt
                t_differentiated = (t[:-1] + t[1:]) / 2

                gain_factor = -(R_in_ohms * C_f_farads)
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

# --- Prelab Tab ---
# Define the MCQs and answers
mcq_questions = [
    {
        "question": "1. What is the primary function of an operational amplifier in an ideal circuit configuration?",
        "options": ["To act as a low-pass filter", "To amplify voltage differences between its inputs", "To provide a constant output voltage", "To generate a signal without any input"],
        "correct_option_index": 1,
        "explanation": "The primary function of an ideal op-amp is to amplify the voltage difference between its inverting and non-inverting inputs. This high gain allows it to perform various functions when combined with external feedback components."
    },
    {
        "question": "2. An op-amp integrator circuit is typically used to convert a square wave input into which type of output waveform?",
        "options": ["Sine wave", "Triangular wave", "Another square wave", "Sawtooth wave"],
        "correct_option_index": 1,
        "explanation": "An integrator circuit's output is proportional to the integral of its input signal. The integral of a constant voltage (the flat top of a square wave) is a linear ramp (a triangle wave). When the square wave's polarity flips, the direction of the ramp reverses, forming a triangular wave."
    },
    {
        "question": "3. An op-amp differentiator circuit converts a triangular wave input into which type of output waveform?",
        "options": ["Sine wave", "Square wave", "Triangular wave", "Constant DC voltage"],
        "correct_option_index": 1,
        "explanation": "A differentiator circuit's output is proportional to the derivative of its input signal. The derivative of a triangular wave's linear ramps is a constant value. When the slope of the triangular wave changes, the output flips to a new constant value, resulting in a square wave."
    },
]

# --- Prelab Tab ---
with tab1:
    st.header("Prelab: Review Questions")
    st.markdown("""
        **Instructions:** Before you begin the simulation, answer the following questions to test your understanding of op-amp circuits.
    """)
    st.subheader("Question 1")
    st.write("What is the primary function of an operational amplifier in an ideal circuit configuration?")
    st.text_area("Your Answer for Q1", height=100, key="prelab_q1")

    st.subheader("Question 2")
    st.write("How does an integrator circuit modify an input signal? For example, what is the output of an integrator when a square wave is applied to its input?")
    st.text_area("Your Answer for Q2", height=100, key="prelab_q2")

    st.subheader("Question 3")
    st.write("How does a differentiator circuit modify an input signal? What is the output when a triangular wave is applied to its input?")
    st.text_area("Your Answer for Q3", height=100, key="prelab_q3")
    
    st.markdown("---")
    st.subheader("Multiple Choice Questions (MCQ)")

    user_answers = {}
    for i, mcq in enumerate(mcq_questions):
        user_answers[i] = st.radio(mcq["question"], mcq["options"], key=f"mcq_{i}")

    if st.button("Submit Answers", key="submit_mcq"):
        st.subheader("Results")
        all_correct = True
        for i, mcq in enumerate(mcq_questions):
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

# --- Theory Tab ---
with tab2:
    st.header("Theory")
    st.markdown("""
        Here you will find the theoretical background for the two circuits you will be simulating.
    """)

    st.subheader("Op-Amp Integrator")
    st.markdown("""
        An op-amp integrator is an electronic circuit that performs the mathematical operation of integration on its input signal.
        It uses a resistor at the input and a capacitor in the feedback path. The output voltage is proportional to the time integral of the input voltage.
    """)
    st.image("images/integrator.png", caption="Op-Amp Integrator Circuit Diagram", use_container_width=True) 
   # [Image of an Op-Amp Integrator circuit diagram]

    st.markdown("""
        The output voltage ($V_{out}$) is given by the formula:
        $$ V_{out}(t) = -\\frac{1}{R_1 C_f} \\int V_{in}(t) dt $$
    """)

    st.subheader("Op-Amp Differentiator")
    st.markdown("""
        An op-amp differentiator is an electronic circuit that performs the mathematical operation of differentiation on its input signal.
        It uses a capacitor at the input and a resistor in the feedback path. The output voltage is proportional to the rate of change of the input voltage.
    """)
    st.image("images/differentiator.png", caption="Op-Amp Differentiator Circuit Diagram", use_container_width=True) 

#[Image of an Op-Amp Differentiator circuit diagram]

    st.markdown("""
        The output voltage ($V_{out}$) is given by the formula:
        $$ V_{out}(t) = -R_f C_1 \\frac{d V_{in}(t)}{dt} $$
    """)


# --- Simulation Tab ---
with tab3:
    st.header("Simulation")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.subheader("Function Generator")
        wave_type = st.radio(
            "Select Waveform",
            ("Sine wave", "Cosine wave", "Triangular wave", "Square wave"),
            index=0,
            key="wave_type_radio_sim"
        )
        wave_type_map = {"Sine wave": 1, "Cosine wave": 2, "Triangular wave": 3, "Square wave": 4}
        selected_wave_type_int = wave_type_map[wave_type]

        amplitude = st.slider("Amplitude (V)", 0.0, 5.0, 1.0, 0.001, key="amplitude_slider_sim")

        st.subheader("Frequency")
        freq_val = st.slider("Frequency Value", 0.0, 1100.0, 100.0, 0.001, key="frequency_slider_sim")
        current_freq_unit = st.radio(
            "Frequency Unit",
            ("Hz", "kHz", "MHz"),
            index=0,
            horizontal=True,
            key="freq_unit_radio_sim"
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
        st.subheader("Amplifier Type")
        amplifier_type = st.radio(
            "Select Circuit Type",
            ("Integrator", "Differentiator"),
            index=0,
            key="amp_type_radio_sim"
        )
        amplifier_type_map = {"Integrator": 1, "Differentiator": 2}
        selected_amplifier_type_int = amplifier_type_map[amplifier_type]

        st.markdown("---")
        
        R_in_kohm = st.number_input(
            "Resistance (R) (kΩ)",
            min_value=0.001,
            value=10.0,
            step=0.1,
            format="%.3f",
            key="R_input_sim"
        )
        C_f_uF = st.number_input(
            "Capacitance (C) (µF)",
            min_value=0.0001,
            value=0.1,
            step=0.001,
            format="%.5f",
            key="C_input_sim"
        )

    with col3:
       
        st.header(" Circuit Diagram")
        
        # --- Code to display the circuit diagram is now here ---
      
        
        if amplifier_type == "Integrator":
            st.image("images/integrator.png", caption="Integrating Amplifier Circuit", use_container_width=True)
        elif amplifier_type == "Differentiator":
            st.image("images/differentiator.png", caption="Differentiator Circuit", use_container_width=True)
       
        
        
        
        
        st.subheader("CRO Displays")

        y_input, y_output, t, amp_input, total_duration, input_freq, \
        output_amplitude, phase_diff_deg, amplifier_name, output_amp_display_text = simulate_circuit(
            amplitude, actual_frequency, selected_wave_type_int,
            selected_amplifier_type_int, R_in_kohm, C_f_uF
        )
        
       
        fig1, ax1 = plt.subplots(figsize=(6, 3), dpi=100)
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
        st.pyplot(fig1)
        plt.close(fig1)

        #with plot_row_col2:
        fig2, ax2 = plt.subplots(figsize=(6, 3), dpi=100)
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
        st.pyplot(fig2)
        plt.close(fig2)

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
        st.pyplot(fig_combined)
        plt.close(fig_combined)

    st.header("Simulation Results")
    
    if 'simulation_history' not in st.session_state:
        st.session_state.simulation_history = []
    
    if st.button("Log Current Results to Table", key="log_button_sim"):
        new_entry = {
            "#": len(st.session_state.simulation_history) + 1,
            "Integrator/Differentiator": amplifier_name,
            "R (kΩ)": f"{R_in_kohm:.1f}",
            "C (µF)": f"{C_f_uF:.3f}",
            "Input Amp (V)": f"{amp_input:.2f}",
            "Input Freq (Hz)": f"{input_freq:.1f}",
            "Output Amp (V)": f"{output_amplitude:.2f}",
            "Output Freq (Hz)": f"{input_freq:.1f}",
            "Phase Diff (deg)": f"{phase_diff_deg:.1f}" if isinstance(phase_diff_deg, (int, float)) else phase_diff_deg
        }
        st.session_state.simulation_history.append(new_entry)
    
    if st.session_state.simulation_history:
        df_history = pd.DataFrame(st.session_state.simulation_history)
        st.dataframe(df_history, use_container_width=True)
    
    if st.button("Clear Table History", key="clear_table_button_sim"):
        st.session_state.simulation_history = []
        st.rerun()


# --- Postlab Tab ---
with tab4:
    st.header("Postlab: Analysis and Conclusion")
    st.markdown("""
        **Instructions:** Use the simulation results you logged to the table to answer the following questions.
    """)
    st.subheader("Question 1")
    st.write("When you used the Integrator circuit with a square wave input, what was the shape of the output waveform? Explain why this happens.")
    st.text_area("Your Answer for Q1", height=100, key="postlab_q1")
    
    st.subheader("Question 2")
    st.write("What happens to the output amplitude of the Differentiator circuit as you increase the input frequency? What does this tell you about the circuit's response to frequency?")
    st.text_area("Your Answer for Q2", height=100, key="postlab_q2")

    st.subheader("Question 3")
    st.write("Based on your simulation, describe the phase relationship between the input sine wave and the output of both the Integrator and the Differentiator circuits.")
    st.text_area("Your Answer for Q3", height=100, key="postlab_q3")


# --- Feedback Tab ---
with tab5:
    st.header("Feedback")
    st.markdown("""
        We appreciate your feedback! Please let us know if you found this simulator useful and how we can improve it.
    """)
    st.text_area("Your Feedback", height=200, key="feedback_text")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
