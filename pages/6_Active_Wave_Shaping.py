# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:35:34 2025

@author: damo3
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

st.set_page_config(layout="wide", page_title="Active Wave Shaping Circuit")

st.title("Active Wave Shaping Circuit Simulator")

# Create the tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

mcq_questions = [
    {
        "question":("What is the main advantage of an **active clipper circuit** (using an op-amp) over a passive clipper (diode and resistor)?"),
        "options": [
            " It operates only with low-frequency signals.",
"It provides a near-ideal clipping action with almost no voltage drop (i.e., minimal effect from the diode's $0.7 {V}$ drop).",
" It completely eliminates the need for a DC reference voltage.",
" It significantly increases the peak amplitude of the output signal."
],
        "correct_option_index": 1,
        "explanation": " The op-amp is configured to operate as a **precision rectifier/limiter**. Due to the op-amp's extremely high open-loop gain, the diode's forward voltage drop is effectively eliminated from the output equation. This allows the signal to be clipped very precisely at the **reference voltage ($V_{{ref}}$**, making the diode behave almost ideally."
    },
    {
     "question":("In an active clamper circuit, which component is fundamentally responsible for introducing the DC level shift to the AC signal?"),
      "options": [
            "The operational amplifier (op-amp).",
  " The diode, by determining the peak-to-peak voltage.",
  " The capacitor, by charging to the peak value of the input signal.",
  "The current-limiting resistor."
          ],
     "correct_option_index": 2,
     "explanation":"The **capacitor** is the energy storage element. During one half-cycle, the diode is forward-biased, allowing the capacitor to charge to the peak input voltage (minus the clamping reference, if any). Since the capacitor is in series, this stored DC voltage is then added to (or subtracted from) the input AC signal, shifting the entire waveform up or down."
     },
    {
     "question":("An active positive clipper circuit has a sine wave input with a peak of $10\text{V}$ and a reference voltage $V_{\text{ref}} = 4\text{V}$. What is the maximum positive voltage of the clipped output waveform?"),
     "options": [
            " $0.7 {V}$",
   " $10 {V}$",
   " $4 {V}$",
   " $6 {V}$"
         ],
     "correct_option_index": 2,
     "explanation":" A **positive clipper** limits or 'clips' the positive voltage peaks. In an active circuit, the output voltage is precisely limited by the $V_{ {ref}}$ source when the input exceeds $V_{{ref}}$. Therefore, all positive input voltage portions above $4 {V}$ are removed, leaving a maximum positive output of $4 {V}$. The negative portion remains unaffected."
     },
     {
      "question":("For a clamper circuit to function correctly as a **DC restorer**, the $RC$ time constant ($\tau$) of the circuit should be:"),
      "options": [
            " Very small compared to the input signal period ($T$).",
  " Roughly equal to the input signal period ($T$).",
  " Very large (typically $\tau \ge 5T$) to ensure the capacitor holds its charge.",
  "Exactly half of the input signal period ($T$)."
  ],
"correct_option_index": 2,
"explanation":"The clamper's capacitor charges quickly when the diode is ON, but it must **discharge very slowly** when the diode is OFF to maintain the DC shift. If the time constant ($\tau = RC$) is large compared to the signal period ($T$), the capacitor voltage remains relatively constant, ensuring the entire waveform is shifted without significant decay."
        },
     {
      "question":("In the context of wave-shaping, the primary function of a **clipper** is to **limit the amplitude** of the waveform, while a **clamper**'s primary function is to:"),
      "options": [
            " Amplify the signal without distortion.",
  " Shift the DC level of the entire waveform.",
  "Convert the AC signal into a pure DC signal.",
  " Introduce a fixed frequency shift."
    ],
    "correct_option_index": 1,
    "explanation": "A **clipper** *removes* a portion of the signal above or below a certain level, **changing the shape** but not the DC level. A **clamper** *adds* a DC voltage to the signal, effectively **shifting the entire waveform** up or down without changing its peak-to-peak amplitude or shape. This is why clampers are also called DC restorers."  
      }
    ]

# --- Prelab Tab ---
with tab1:
    st.header("Prelab")
    st.markdown("""
    **Objective:** To understand the operation of active clipper and clamper circuits using op-amps.

    **Pre-requisites:**
    1.  Basic knowledge of operational amplifiers (op-amps).
    2.  Understanding of diodes and their ideal behavior.
    3.  Familiarity with capacitors and their role in DC level shifting.

    """)
    st.subheader("Multiple Choice Questions (MCQ)")
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
with tab2:
    st.header("Theory")
    st.markdown("""
    Active wave shaping circuits use **operational amplifiers** in conjunction with diodes and other passive components to modify the shape of an input signal. The op-amp provides a high input impedance and a low output impedance, which makes the circuit's performance independent of the load.

    ### Clippers (Limiters)
    A **clipper** circuit removes or "clips" a portion of an input signal that is above or below a specific voltage level. The output signal's shape is different from the input, but its AC components remain.

    * **Positive Clipper:** Limits the positive portion of the input signal. The output waveform is flat at the reference voltage for all input voltages greater than V_ref.
    * **Negative Clipper:** Limits the negative portion of the input signal. The output waveform is flat at the reference voltage for all input voltages less than V_ref.

    The clipping action is due to the non-linear behavior of a diode, which is either forward-biased or reverse-biased depending on the input voltage relative to the reference voltage.

    ### Clampers (DC Restorers)
    A **clamper** circuit shifts the entire input signal's DC level without altering the shape of the waveform. This is achieved by using a capacitor to store charge and a diode to control the charging path. The capacitor charges to the peak of the input signal and then adds this DC voltage to the input, effectively shifting the entire waveform up or down.

    * **Positive Clamper:** Shifts the entire input signal upwards, so its lowest peak is clamped to the reference voltage.
    * **Negative Clamper:** Shifts the entire input signal downwards, so its highest peak is clamped to the reference voltage.

    Unlike clippers, the input and output waveforms have the same peak-to-peak voltage. The op-amp is crucial for maintaining signal integrity and providing precise clamping without loading effects.
    """)

# --- Simulation Tab ---
with tab3:
    # --- Layout with Columns ---
    # col1 for Function Generator, col2 for Wave Shaping controls, col3 for CRO displays.
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.header("Function Generator")
        # Radio buttons for waveform selection.
        wave_type = st.radio(
            "Select Waveform",
            ("Sine wave", "Cosine wave", "Triangular wave", "Square wave"),
            index=0, # Default to Sine wave
            key="wave_type_radio_shaping" # Unique key for this page's widgets
        )
        # Map string wave type to integer value for compatibility with existing logic.
        wave_type_map = {"Sine wave": 1, "Cosine wave": 2, "Triangular wave": 3, "Square wave": 4}
        selected_wave_type_int = wave_type_map[wave_type]

        # Slider for amplitude control.
        amplitude = st.slider("Amplitude (V)", 0.0, 5.0, 1.0, 0.001, key="amplitude_slider_shaping")

        st.subheader("Frequency")
        # Slider for frequency value.
        freq_val = st.slider("Frequency Value", 0.0, 1100.0, 100.0, 0.001, key="frequency_slider_shaping")
        # Radio buttons for frequency unit (Hz, kHz, MHz).
        current_freq_unit = st.radio(
            "Frequency Unit",
            ("Hz", "kHz", "MHz"),
            index=0, # Default to Hz
            horizontal=True,
            key="freq_unit_radio_shaping"
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
        st.header("Wave Shaping Circuit Type")
        # Radio buttons for selecting wave shaping type.
        shaping_type = st.radio(
            "Select Circuit Type",
            ("Positive Clipper", "Negative Clipper", "Positive Clamper", "Negative Clamper"),
            index=0, # Default to Positive Clipper
            key="shaping_type_radio"
        )
        # Map string shaping type to integer value.
        shaping_type_map = {
            "Positive Clipper": 1,
            "Negative Clipper": 2,
            "Positive Clamper": 3,
            "Negative Clamper": 4
        }
        selected_shaping_type_int = shaping_type_map[shaping_type]

        # Number input for Reference Voltage.
        V_ref = st.number_input(
            "Reference Voltage (V_ref) (V)",
            value=0.0,
            step=0.1,
            format="%.2f", # Format to 2 decimal places.
            key="V_ref_input_shaping"
        )

        st.markdown("---") # Horizontal line for visual separation.
        st.write("Developed by DAMODAR")

    # --- Core Simulation Logic ---
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

    def get_shaping_circuit_name(shaping_type_value):
        """Returns the name of the wave shaping circuit based on its integer value."""
        if shaping_type_value == 1:
            return "Positive Clipper"
        elif shaping_type_value == 2:
            return "Negative Clipper"
        elif shaping_type_value == 3:
            return "Positive Clamper"
        elif shaping_type_value == 4:
            return "Negative Clamper"
        return "N/A"

    def simulate_wave_shaping_circuit(amp_input, actual_frequency, selected_wave_type_int,
                                      selected_shaping_type_int, V_ref_val):
        """
        Performs the wave shaping circuit simulation and calculates output parameters.
        """
        # Generate the input waveform.
        y_input, t, amp_input_actual, total_duration, input_freq = generate_waveform(
            amp_input, actual_frequency, selected_wave_type_int
        )

        # Define typical op-amp power supply limits (for clipping).
        clipping_limit = 15.0
        
        y_output = np.copy(y_input) # Start with a copy of input to modify.
        
        # Calculate input time period in seconds.
        input_time_s = 1 / input_freq if input_freq != 0 else 0

        shaping_circuit_name = get_shaping_circuit_name(selected_shaping_type_int)

        # --- Wave Shaping Logic ---
        if selected_shaping_type_int == 1:  # Positive Clipper (clips positive peaks above V_ref)
            y_output = np.minimum(y_input, V_ref_val)
            
        elif selected_shaping_type_int == 2: # Negative Clipper (clips negative peaks below V_ref)
            y_output = np.maximum(y_input, V_ref_val)

        elif selected_shaping_type_int == 3: # Positive Clamper (shifts min peak to V_ref)
            # Calculate the shift amount needed to move the minimum of the input to V_ref.
            if len(y_input) > 0:
                min_input_val = np.min(y_input)
                shift_amount = V_ref_val - min_input_val
                y_output = y_input + shift_amount
            else:
                y_output = np.zeros_like(y_input)

        elif selected_shaping_type_int == 4: # Negative Clamper (shifts max peak to V_ref)
            # Calculate the shift amount needed to move the maximum of the input to V_ref.
            if len(y_input) > 0:
                max_input_val = np.max(y_input)
                shift_amount = V_ref_val - max_input_val
                y_output = y_input + shift_amount
            else:
                y_output = np.zeros_like(y_input)

        # Ensure the output does not exceed the op-amp's power supply limits.
        y_output = np.clip(y_output, -clipping_limit, clipping_limit)
        
        # Calculate output high and low values after shaping and clipping.
        output_high = np.max(y_output) if len(y_output) > 0 else 0
        output_low = np.min(y_output) if len(y_output) > 0 else 0

        return y_input, y_output, t, amp_input_actual, total_duration, input_freq, input_time_s, \
                 V_ref_val, output_high, output_low, shaping_circuit_name

    # --- CRO Displays ---
    with col3:
         st.header("Circuit Diagram")
        
         if shaping_type == "Positive Clipper":
          st.image("images/postiveclipper.png", caption="Positive Clipper Circuit", width='stretch')
         elif shaping_type== "Negative Clipper":
          st.image("images/negativeclipper.png", caption="Negative Clipper Circuit", width='stretch')
         elif shaping_type== "Positive Clamper":
          st.image("images/positiveclamper.png", caption="Positive Clamper Circuit", width='stretch')
         elif shaping_type== "Negative Clamper":
          st.image("images/negativeclamper.png", caption="Negative Clamper Circuit", width='stretch')
        
    st.header("CRO Displays")
    plot_col1, plot_col2, plot_col3 = st.columns(3) 
    st.text_input("Your Name",key="p2")
        # Perform the simulation based on current widget values.
    y_input, y_output, t, amp_input, total_duration, input_freq, input_time_s, \
    V_ref_val, output_high, output_low, shaping_circuit_name = simulate_wave_shaping_circuit(
            amplitude, actual_frequency, selected_wave_type_int,
            selected_shaping_type_int, V_ref
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

        # Adjust Y-axis limits to include input amplitude and V_ref, with padding.
    max_plot_amp_input = max(amp_input * 1.5, abs(V_ref_val) * 1.2)
    if max_plot_amp_input == 0: max_plot_amp_input = 1 # Ensure a minimum range if all values are 0.
    ax1.set_ylim(-max_plot_amp_input, max_plot_amp_input)
         
    ax1.set_xlim(0, total_duration)
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.set_title("Ch 1: Input Signal", color='white', fontsize=10)
    ax1.text(0.02, 0.95, f'Amp: {amp_input:.2f} V', transform=ax1.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    with plot_col1:    
        st.pyplot(fig1) # Display the Matplotlib figure in Streamlit.

        # Plotting for CRO Channel 2 (Output Signal).
    fig2, ax2 = plt.subplots(figsize=(3, 2), dpi=100)
    ax2.plot(t, y_output, color='cyan')
    ax2.set_facecolor("black")
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
        
        # Set Y-axis limits based on the output signal's range, with padding.
        # Ensure a minimum range even if output is flat.
    max_plot_amp_output = max(abs(output_high), abs(output_low)) * 1.2
    if max_plot_amp_output == 0: max_plot_amp_output = 1
    ax2.set_ylim(-max_plot_amp_output, max_plot_amp_output)
        
    ax2.set_xlim(0, total_duration)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    ax2.set_title("Ch 2: Output Signal", color='white', fontsize=10)
    ax2.text(0.02, 0.95, f'Output High: {output_high:.2f} V', transform=ax2.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    ax2.text(0.02, 0.85, f'Output Low: {output_low:.2f} V', transform=ax2.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    with plot_col2:     
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
    max_combined_amp = max(max_plot_amp_input, max_plot_amp_output)
    if max_combined_amp == 0: max_combined_amp = 1
    ax_combined.set_ylim(-max_combined_amp, max_combined_amp)
        
    ax_combined.set_xlim(0, total_duration)
    ax_combined.tick_params(axis='x', colors='white')
    ax_combined.tick_params(axis='y', colors='white')
    ax_combined.set_title("Combined View (Ch 1 & Ch 2)", color='white', fontsize=10)
    ax_combined.legend(loc='upper right', fontsize=8, facecolor='darkgray', edgecolor='white')
    with plot_col3:     
        st.pyplot(fig_combined) # Display the Matplotlib figure in Streamlit.

    # --- Dynamic Parameters Table ---
    st.header("Simulation Results")

    # Initialize session state for history if it doesn't exist.
    if 'simulation_history_shaping' not in st.session_state: # Unique key for this page's history.
        st.session_state.simulation_history_shaping = []

    # Button to log the current result to the table.
    if st.button("Log Current Results to Table", key="log_button_shaping"):
        new_entry = {
            "#": len(st.session_state.simulation_history_shaping) + 1,
            "Circuit Type": shaping_circuit_name,
            "Input Amp (V)": f"{amp_input:.2f}",
            "Input Freq (Hz)": f"{input_freq:.1f}",
            "Input Time Period (s)": f"{input_time_s:.3f}",
            "Reference Voltage (V)": f"{V_ref_val:.2f}",
            "Output High (V)": f"{output_high:.2f}",
            "Output Low (V)": f"{output_low:.2f}"
        }
        st.session_state.simulation_history_shaping.append(new_entry)

    # Display the history as a Pandas DataFrame.
    if st.session_state.simulation_history_shaping:
        df_history = pd.DataFrame(st.session_state.simulation_history_shaping)
        st.dataframe(df_history, width='stretch') # use_container_width makes the table responsive.

    # Button to clear the table history.
    if st.button("Clear Table History", key="clear_table_button_shaping"):
        st.session_state.simulation_history_shaping = [] # Reset the history list.
        st.rerun() # Rerun the app to immediately reflect the cleared table.

# --- Postlab Tab ---
with tab4:
    st.header("Postlab")
    st.text_input("Your Name",key="p3")
    st.subheader("Conclusion:")
   
    st.write(" Summarize your observations from the simulation for clippers and clampers.")
    st.text_area("Your Answer ", height=100, key="postlab_q1")
    st.write(" Explain the effect of changing the reference voltage on the output waveforms.")
    st.text_area("Your Answer ", height=100, key="postlab_q2")
    st.write(" Discuss the importance of the op-amp in active wave shaping circuits.")
    st.text_area("Your Answer ", height=100, key="postlab_q3")
    st.subheader("Conclusion:")
    
    st.write(" For a sinusoidal input with an amplitude of 3V and a V_ref of 1V, describe the resulting output waveforms for a **Positive Clipper** and a **Negative Clipper**.")
    st.text_area("Your Answer ", height=100, key="postlab_q4")
    st.write(" For the same input, describe the output waveforms for a **Positive Clamper** and a **Negative Clamper**.")
    st.text_area("Your Answer ", height=100, key="postlab_q5")
    st.write(" Explain a real-world application for a clipper circuit and a clamper circuit.")
    st.text_area("Your Answer ", height=100, key="postlab_q6")

# --- Feedback Tab ---
with tab5:
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
