# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:23:38 2025

@author: damo3
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

st.set_page_config(layout="wide", page_title="Comparator")

st.title("Comparator Simulator")

# Create the tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Objective", "Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

mcq_questions = [
    {
     # --- Question 1 ---
     
     "question": "What configuration is an op-amp typically used in when functioning as a basic voltage comparator?",
     "options" : [
         " Inverting amplifier with negative feedback",
         " Non-inverting amplifier with negative feedback",
         " Open-loop (no feedback)",
         " Voltage follower"
     ],
     "correct_option_index": 2,
     "explanation":  "The high open-loop gain is necessary for rapid saturation."
 },
    {
     "question": "If an op-amp comparator has dual supply voltages of $\pm 12 V$, and its output voltage is measured to be $+10.5 V$, what is the output state?",
     "options" :[
         " Linear (active region)",
         " Positive saturation",
         " Negative saturation",
         " Oscillating"
         ],
     
"correct_option_index": 1,
"explanation": "The output is close to the positive supply rail, indicating **saturation**."
       
     },
    {
     "question": "If the input to an op-amp comparator (Zero-Crossing Detector) is a sine wave, what is the output waveform?",
     "options" :[
     " Sine wave with $180^\circ$ phase shift",
     "Square/Rectangular wave",
     " Triangular wave",
     " DC voltage at $0 V$"
      ],
     "correct_option_index": 1,
     "explanation": "The large gain converts the smooth sine wave into a **square wave**."
     },
    {
     "question":"What is the main drawback of using a basic op-amp (open-loop) as a comparator when the input signal is slow-changing or noisy near the reference voltage?",
     "options" : [
     " Low voltage gain",
     " Input offset voltage is negligible",
     " The output may switch back and forth (chatter) repeatedly",
     " It consumes excessive current"
     ],
     "correct_option_index": 2,
     "explanation":"The noise near the single threshold causes the output to **chatter**.",
     },
    {
     "question": "For an **inverting** op-amp comparator with $V_{ref} = +5 V$ connected to $V_+$, and the signal $V_{in}$ connected to $V_-$, when will the output ($V_{out}$) be at its **positive saturation voltage** ($+V_{sat}$)?\n\n*(Hint: Output is high when $V_+ > V_-$)*",
      "options" : [
      " When $V_i > +5 V$",
      " When $V_i = +5 V$",
      " When $V_i < +5 V$",
      " When $V_i$ is negative"
      ],
     "correct_option_index": 2,
     "explanation":"$V_{out}$ is high when $V_{ref} > V_{in}$, or $+5 \text{V} > V_{in}$."
     }
     
  ]
     
     
     
# --- Prelab Tab ---
with tab1:

    
    st.markdown("""
    **Objective:** To understand the operation of an operational amplifier (op-amp) as a comparator.

    **Pre-requisites:**
    1. Basic knowledge of op-amp characteristics (ideal and practical).
    2. Understanding of voltage levels and saturation voltages.
    3. Familiarity with different types of waveforms (sine, square, triangular).

    """)

with tab2:
   
    # Simulate 'with tab1:' for a standalone executable script
    st.header("Prelab")
  
    
    st.markdown("---")
    st.subheader("Prelab Quick Check: Op-Amp Comparator MCQs 🧠")
    st.text_input("Your Name",key="p1")
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
with tab3:
    st.header("Theory")
    st.markdown("""
    A **comparator** is a circuit that compares an input voltage with a pre-defined reference voltage. The output of the comparator is a digital signal that indicates which of the two voltages is larger. This process is often called **voltage-level detection**.

    ### How a Comparator Works

    A simple comparator can be built using an operational amplifier (op-amp) without any feedback resistor. The op-amp is configured in its open-loop configuration, where its very high open-loop gain causes its output to saturate at either the positive or negative power supply rail.

    The operation depends on the voltage difference between the two input terminals of the op-amp:
    * **Inverting Comparator:** The input signal is applied to the **inverting (-) terminal**, and the reference voltage (V_ref) is applied to the **non-inverting (+) terminal**.
        * If $V_{in} > V_{ref}$, the output saturates to the negative supply voltage ($V_{sat-}$, e.g., -15V).
        * If $V_{in} < V_{ref}$, the output saturates to the positive supply voltage ($V_{sat+}$, e.g., +15V).

    * **Non-Inverting Comparator:** The input signal is applied to the **non-inverting (+) terminal**, and the reference voltage (V_ref) is applied to the **inverting (-) terminal**.
        * If $V_{in} > V_{ref}$, the output saturates to the positive supply voltage ($V_{sat+}$).
        * If $V_{in} < V_{ref}$, the output saturates to the negative supply voltage ($V_{sat-}$).

    The output waveform is always a square wave, regardless of the input waveform, because the output is always driven to one of two states. The frequency of the output square wave is the same as the input frequency. The duty cycle of the output waveform, however, depends on the amplitude of the input signal and the value of the reference voltage.
    """)

# --- Simulation Tab ---
with tab4:
    # --- Layout with Columns ---
    # col1 for Function Generator, col2 for Comparator controls, col3 for CRO displays.
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.header("Function Generator")
        # Radio buttons for waveform selection.
        wave_type = st.radio(
            "Select Waveform",
            ("Sine wave", "Cosine wave", "Triangular wave", "Square wave"),
            index=0, # Default to Sine wave
            key="wave_type_radio_comparator" # Unique key for this page's widgets
        )
        # Map string wave type to integer value for compatibility with existing logic.
        wave_type_map = {"Sine wave": 1, "Cosine wave": 2, "Triangular wave": 3, "Square wave": 4}
        selected_wave_type_int = wave_type_map[wave_type]

        # Slider for amplitude control.
        amplitude = st.slider("Amplitude (V)", 0.0, 5.0, 1.0, 0.001, key="amplitude_slider_comparator")

        st.subheader("Frequency")
        # Slider for frequency value.
        freq_val = st.slider("Frequency Value", 0.0, 1100.0, 100.0, 0.001, key="frequency_slider_comparator")
        # Radio buttons for frequency unit (Hz, kHz, MHz).
        current_freq_unit = st.radio(
            "Frequency Unit",
            ("Hz", "kHz", "MHz"),
            index=0, # Default to Hz
            horizontal=True,
            key="freq_unit_radio_comparator"
        )

        # Helper function to convert frequency value based on selected unit.
        def get_actual_frequency(freq_val_local, unit_local):
            if unit_local == "kHz":
                return freq_val_local * 1e3
            elif unit_local == "MHz":
                return freq_val_local * 1e6
            else: # Hz
                return freq_val_local

        actual_frequency = get_actual_frequency(freq_val, current_freq_unit)

    with col2:
        st.header("Comparator Type")
        # Radio buttons for selecting comparator type.
        comparator_type = st.radio(
            "Select Comparator Type",
            ("Inverting Comparator", "Non-Inverting Comparator"),
            index=0, # Default to Inverting Comparator
            key="comparator_type_radio"
        )
        # Map string comparator type to integer value.
        comparator_type_map = {"Inverting Comparator": 1, "Non-Inverting Comparator": 2}
        selected_comparator_type_int = comparator_type_map[comparator_type]

        # Number input for Reference Voltage.
        V_ref = st.number_input(
            "Reference Voltage (V_ref) (V)",
            value=0.0,
            step=0.1,
            format="%.2f", # Format to 2 decimal places.
            key="V_ref_input"
        )

        st.markdown("---") # Horizontal line for visual separation.
        st.write("Developed by DAMODAR")


    # --- Core Simulation Logic ---
    # These functions are largely preserved from your Tkinter code, adapted for Streamlit's flow.

    def generate_waveform(amp, freq, wave_type_val, num_cycles=3):
        """
        Generates the input waveform based on amplitude, frequency, and waveform type.
        """
        if freq == 0:
            sampling_rate = 10000 # Default sampling for DC.
        else:
            # Adjust sampling rate based on frequency to ensure enough points per cycle.
            # At least 100 points per cycle, or a minimum of 1000 points overall.
            sampling_rate = max(100 * freq, 1000)

        # Calculate total duration for the specified number of cycles.
        total_duration = num_cycles / freq if freq != 0 else 0.01 # Avoid division by zero, set a small default for DC.

        num_points = int(sampling_rate * total_duration)
        if num_points < 2:
            num_points = 2

        # Generate time array.
        t = np.linspace(0, total_duration, num_points, endpoint=False)

        # Generate waveform based on selected type.
        if freq == 0: # DC voltage.
            y = np.full_like(t, amp) # Flat line at amplitude.
        elif wave_type_val == 1: # Sine wave.
            y = amp * np.sin(2 * np.pi * freq * t)
        elif wave_type_val == 2: # Cosine wave.
            y = amp * np.cos(2 * np.pi * freq * t)
        elif wave_type_val == 3: # Triangular wave.
            y = amp * signal.sawtooth(2 * np.pi * freq * t, width=0.5) # width=0.5 for symmetric triangle.
        elif wave_type_val == 4: # Square wave.
            y = amp * signal.square(2 * np.pi * freq * t)
        else:
            y = np.zeros_like(t) # No waveform selected, return zeros.

        return y, t, amp, total_duration, freq

    def get_comparator_name(comp_type_value):
        """Returns the name of the comparator based on its integer value."""
        if comp_type_value == 1:
            return "Inverting Comparator"
        elif comp_type_value == 2:
            return "Non-Inverting Comparator"
        return "N/A"

    def simulate_comparator_circuit(amp_input, actual_frequency, selected_wave_type_int,
                                     selected_comparator_type_int, V_ref_val):
        """
        Performs the comparator circuit simulation and calculates output parameters.
        """
        # Generate the input waveform.
        y_input, t, amp_input_actual, total_duration, input_freq = generate_waveform(
            amp_input, actual_frequency, selected_wave_type_int
        )

        # Define typical op-amp saturation voltages.
        V_sat_plus = 15.0
        V_sat_minus = -15.0

        y_output = np.zeros_like(y_input)
        
        # Calculate input time period in seconds.
        input_time_s = 1 / input_freq if input_freq != 0 else 0

        comparator_name = get_comparator_name(selected_comparator_type_int)

        # --- Comparator Logic ---
        if selected_comparator_type_int == 1:  # Inverting Comparator
            # If input voltage is greater than V_ref, output goes to V_sat_minus.
            y_output[y_input > V_ref_val] = V_sat_minus
            # If input voltage is less than or equal to V_ref, output goes to V_sat_plus.
            y_output[y_input <= V_ref_val] = V_sat_plus

        elif selected_comparator_type_int == 2: # Non-Inverting Comparator
            # If input voltage is greater than V_ref, output goes to V_sat_plus.
            y_output[y_input > V_ref_val] = V_sat_plus
            # If input voltage is less than or equal to V_ref, output goes to V_sat_minus.
            y_output[y_input <= V_ref_val] = V_sat_minus
        
        # The output is inherently clipped to V_sat_plus and V_sat_minus by the logic.
        # An explicit clip here ensures it's strictly within these bounds if any edge cases arise.
        y_output = np.clip(y_output, V_sat_minus, V_sat_plus)
        
        # For a comparator, the output high and low values are the saturation voltages.
        output_high = V_sat_plus
        output_low = V_sat_minus

        return y_input, y_output, t, amp_input_actual, total_duration, input_freq, input_time_s, \
                 V_ref_val, output_high, output_low, comparator_name

    # --- CRO Displays ---
    with col3:
        st.header("Circuit Diagram")
        
        if comparator_type == "Inverting Comparator":
          st.image("images/invertingcomparator.png", caption="Inverting Comparator Circuit", width='stretch')
        elif comparator_type == "Non-Inverting Comparator":
           st.image("images/noninvertingcomparator.png", caption="Non-Inverting Comparator Circuit", width='stretch')
    
        
    st.header("CRO Displays")
    st.text_input("Your Name",key="p2")
     # Create three columns *outside* the col1/col2/col3 definition to span the full width
    plot_col1, plot_col2, plot_col3 = st.columns(3) 

    # Perform the simulation based on current widget values.
    y_input, y_output, t, amp_input, total_duration, input_freq, input_time_s, \
    V_ref_val, output_high, output_low, comparator_name = simulate_comparator_circuit(
            amplitude, actual_frequency, selected_wave_type_int,
            selected_comparator_type_int, V_ref
        )

        # Plotting for CRO Channel 1 (Input Signal).
    fig1, ax1 = plt.subplots(figsize=(3, 2), dpi=100)
    ax1.plot(t, y_input, color='lime')
    ax1.set_facecolor("black")
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
        
        # Plot V_ref line on input graph for better visualization.
    ax1.axhline(V_ref_val, color='red', linestyle='--', linewidth=1, label=f'V_ref={V_ref_val:.2f}V')
    ax1.legend(loc='lower left', fontsize=7, facecolor='darkgray', edgecolor='white')

        # Adjust Y-axis limits to include V_ref if it's outside the signal range, with padding.
    max_plot_amp = max(amp_input * 1.5, abs(V_ref_val) * 1.2)
    if max_plot_amp == 0: max_plot_amp = 1 # Ensure a minimum range if all values are 0.
    ax1.set_ylim(-max_plot_amp, max_plot_amp)
        
    ax1.set_xlim(0, total_duration)
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.set_title("Ch 1: Input Signal", color='black', fontsize=10)
    ax1.text(0.02, 0.95, f'Amp: {amp_input:.2f} V', transform=ax1.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    with plot_col1: # Display fig1 in the first plot column  
                 st.pyplot(fig1) # Display the Matplotlib figure in Streamlit.

        # Plotting for CRO Channel 2 (Output Signal).
    fig2, ax2 = plt.subplots(figsize=(3, 2), dpi=100)
    ax2.plot(t, y_output, color='cyan')
    ax2.set_facecolor("black")
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
        
        # Set Y-axis limits based on saturation voltages with padding.
    ax2.set_ylim(output_low * 1.2, output_high * 1.2)
        
    ax2.set_xlim(0, total_duration)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    ax2.set_title("Ch 2: Output Signal", color='black', fontsize=10)
    ax2.text(0.02, 0.95, f'Output High: {output_high:.2f} V', transform=ax2.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    ax2.text(0.02, 0.85, f'Output Low: {output_low:.2f} V', transform=ax2.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    with plot_col2: # Display fig1 in the first plot column  
                   st.pyplot(fig2) # Display the Matplotlib figure in Streamlit.

        # Plotting for Combined View (Channel 1 & 2).
    fig_combined, ax_combined = plt.subplots(figsize=(6, 3), dpi=100)
    ax_combined.plot(t, y_input, color='lime', label='Input (Ch 1)')
    ax_combined.plot(t, y_output, color='cyan', label='Output (Ch 2)')
    ax_combined.set_facecolor("black")
    ax_combined.axhline(0, color='gray', linewidth=0.5)
    ax_combined.axvline(0, color='gray', linewidth=0.5)
        
        # Plot V_ref line on combined graph.
    ax_combined.axhline(V_ref_val, color='red', linestyle='--', linewidth=1, label=f'V_ref={V_ref_val:.2f}V')

        # Determine combined Y-axis limit.
    max_combined_amp = max(amp_input * 1.5, abs(V_ref_val) * 1.2, output_high * 1.2)
    if max_combined_amp == 0: max_combined_amp = 1
    ax_combined.set_ylim(-max_combined_amp, max_combined_amp)
        
    ax_combined.set_xlim(0, total_duration)
    ax_combined.tick_params(axis='x', colors='white')
    ax_combined.tick_params(axis='y', colors='white')
    ax_combined.set_title("Combined View (Ch 1 & Ch 2)", color='black', fontsize=10)
    ax_combined.legend(loc='upper right', fontsize=8, facecolor='darkgray', edgecolor='white')
    with plot_col3: # Display fig1 in the first plot column  
                    st.pyplot(fig_combined) # Display the Matplotlib figure in Streamlit.

    # --- Dynamic Parameters Table ---
    st.header("Simulation Results")

    # Initialize session state for history if it doesn't exist.
    if 'simulation_history_comparator' not in st.session_state: # Unique key for this page's history.
        st.session_state.simulation_history_comparator = []

    # Button to log the current result to the table.
    if st.button("Log Current Results to Table", key="log_button_comparator"):
        new_entry = {
            "#": len(st.session_state.simulation_history_comparator) + 1,
            "Comparator Type": comparator_name,
            "Input Amp (V)": f"{amp_input:.2f}",
            "Input Freq (Hz)": f"{input_freq:.1f}",
            "Input Time Period (s)": f"{input_time_s:.3f}",
            "Reference Voltage (V)": f"{V_ref_val:.2f}",
            "Output High (V)": f"{output_high:.2f}",
            "Output Low (V)": f"{output_low:.2f}"
        }
        st.session_state.simulation_history_comparator.append(new_entry)

    # Display the history as a Pandas DataFrame.
    if st.session_state.simulation_history_comparator:
        df_history = pd.DataFrame(st.session_state.simulation_history_comparator)
        st.dataframe(df_history, width='stretch') # use_container_width makes the table responsive.

    # Button to clear the table history.
    if st.button("Clear Table History", key="clear_table_button_comparator"):
        st.session_state.simulation_history_comparator = [] # Reset the history list.
        st.rerun() # Rerun the app to immediately reflect the cleared table.

# --- Postlab Tab ---
with tab5:
    st.header("Postlab")
    st.text_input("Your Name",key="p3")
    st.markdown("""
    **Conclusion:**
    """)
    st.write("Summarize your observations from the simulation.")
    st.text_area("Your Answer", height=100, key="postlab_q1")
    st.write("Explain how the output waveform changed based on the input signal and the reference voltage.")
    st.text_area("Your Answer", height=100, key="postlab_q2")
    st.write("Discuss the difference between the inverting and non-inverting comparator circuits.")
    st.text_area("Your Answer", height=100, key="postlab_q3")
    st.markdown("""
    **Analysis:**
    """)
    st.write("For a sinusoidal input with an amplitude of 2V and V_ref = 1V, describe the resulting output waveform (high/low voltages, duty cycle).")
    st.text_area("Your Answer", height=100, key="postlab_q4")
    st.write("What happens to the output if the reference voltage is set to a value greater than the peak-to-peak voltage of the input signal?")
    st.text_area("Your Answer", height=100, key="postlab_q5")
    st.write("Explain a real-world application of a comparator circuit (e.g., zero-crossing detector, threshold detector).")
    st.text_area("Your Answer", height=100, key="postlab_q6")

# --- Feedback Tab ---
with tab6:
    st.header("Feedback")
    st.markdown("""
    We value your feedback to improve this simulator. Please let us know your thoughts.
    """)
    st.text_input("Your Name")
    st.text_input("Registration number/Faculty ID")
    st.slider("How would you rate this simulator?(best -5)", 1, 5)
   
    st.text_input("1.  What did you find most useful about this simulator?")
    st.text_input("2.  Were there any features that were confusing or difficult to use?")
    st.text_input("3.  What new features would you like to see added in the future?")
   
    st.text_area("Any other comments or suggestions.", height=200, key="feedback_text")
    if st.button("Submit Feedback"):
      st.success("Thank you for your feedback!")
