# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:31:36 2025

@author: damo3
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

st.set_page_config(layout="wide", page_title="Schmitt Trigger")

st.title("Schmitt Trigger Simulator")

# Create the tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

# --- Prelab Tab ---
with tab1:
    st.header("Prelab")
    st.markdown("""
    **Objective:** To understand the operation of an operational amplifier (op-amp) configured as a Schmitt Trigger.

    **Pre-requisites:**
    1.  Basic knowledge of op-amp characteristics and voltage-level detection.
    2.  Understanding of positive feedback in op-amp circuits.
    3.  Familiarity with hysteresis and its application in electronics.

    **Questions:**
    1.  What is a Schmitt Trigger and how does it differ from a simple comparator?
    2.  Explain the concept of **hysteresis** in a circuit. Why is it useful?
    3.  Define the **Upper Threshold Point (V_UTP)** and the **Lower Threshold Point (V_LTP)**.
    4.  Draw the circuit diagram for a non-inverting Schmitt Trigger and derive the equations for V_UTP and V_LTP.
    5.  Predict the output waveform for a given input signal and specific R1 and R2 values.
    """)

# --- Theory Tab ---
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

# Assume the rest of your app's code is here
with tab2:
# Using a raw string for markdown to correctly render LaTeX and prevent backslash issues
    #with st.expander("Show Theory Tab Content"):
    st.header("Theory")
    st.markdown(r"""
    A **Schmitt Trigger** is a comparator with **positive feedback**. This feedback creates two different threshold voltages for the input: an **Upper Threshold Point (V_UTP)** and a **Lower Threshold Point (V_LTP)**. The output state of the Schmitt Trigger depends not only on the current input voltage but also on the previous output state. This two-threshold behavior is known as **hysteresis**.

    ### How Hysteresis Works

    The main advantage of a Schmitt Trigger is its ability to convert a noisy or slowly-changing input signal into a clean, noise-free digital output. Because the input must pass a higher threshold to switch from one state and a lower threshold to switch back, small voltage fluctuations (noise) around a single reference point won't cause the output to oscillate.

    ***

    ### Circuit Operation (Non-Inverting Configuration)

    In a non-inverting Schmitt Trigger, the input signal is applied to the non-inverting (+) terminal, and the positive feedback loop is created by connecting a resistor (**R1**) from the output to the non-inverting input, and another resistor (**R2**) from the non-inverting input to ground.

    """)
    st.image("images/schmitttrigger.png", caption="Schmitt Trigger Circuit", use_container_width=True)
    st.markdown(r"""

    The threshold voltages are determined by the resistance values (R1 and R2) and the op-amp's saturation voltages ($V_{sat+}$ and $V_{sat-}$):

    * **Upper Threshold Point (V_UTP):** This is the voltage at which the input must rise to cause the output to switch from high ($V_{sat+}$) to low ($V_{sat-}$).
        $$V_{UTP} = V_{sat+} \left( \frac{R2}{R1 + R2} \right)$$

    * **Lower Threshold Point (V_LTP):** This is the voltage at which the input must fall to cause the output to switch from low ($V_{sat-}$) to high ($V_{sat+}$).
        $$V_{LTP} = V_{sat-} \left( \frac{R2}{R1 + R2} \right)$$

    The **hysteresis width** is the difference between these two thresholds: $H = V_{UTP} - V_{LTP}$. This positive feedback ensures a sharp, clean transition, effectively "de-bouncing" the input signal.
    """)

# --- Simulation Tab ---
with tab3:
    # --- Layout with Columns ---
    # col1 for Function Generator, col2 for Schmitt Trigger controls, col3 for CRO displays.
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.header("Function Generator")
        # Radio buttons for waveform selection.
        wave_type = st.radio(
            "Select Waveform",
            ("Sine wave", "Cosine wave", "Triangular wave", "Square wave"),
            index=0, # Default to Sine wave
            key="wave_type_radio_schmitt" # Unique key for this page's widgets
        )
        # Map string wave type to integer value for compatibility with existing logic.
        wave_type_map = {"Sine wave": 1, "Cosine wave": 2, "Triangular wave": 3, "Square wave": 4}
        selected_wave_type_int = wave_type_map[wave_type]

        # Slider for amplitude control.
        amplitude = st.slider("Amplitude (V)", 0.0, 5.0, 1.0, 0.001, key="amplitude_slider_schmitt")

        st.subheader("Frequency")
        # Slider for frequency value.
        freq_val = st.slider("Frequency Value", 0.0, 1100.0, 100.0, 0.001, key="frequency_slider_schmitt")
        # Radio buttons for frequency unit (Hz, kHz, MHz).
        current_freq_unit = st.radio(
            "Frequency Unit",
            ("Hz", "kHz", "MHz"),
            index=0, # Default to Hz
            horizontal=True,
            key="freq_unit_radio_schmitt"
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
        st.header("Schmitt Trigger Parameters")
        st.info("Note: For typical non-inverting Schmitt Trigger, R1 is connected to the output and R2 to ground, with input to the non-inverting terminal. The thresholds are set by R1, R2, and the saturation voltages.")
        st.markdown("For this simulation, we assume a non-inverting configuration where hysteresis is determined by R1 (feedback) and R2 (input to ground).")

        # Number input for Resistance R1 (feedback resistor).
        R1_val_kohm = st.number_input(
            "Resistance (R1) (kΩ)",
            min_value=0.1, # R1 cannot be zero
            value=10.0,
            step=0.1,
            format="%.1f",
            key="R1_input_schmitt"
        )
        # Number input for Resistance R2 (resistor to ground from non-inverting input).
        R2_val_kohm = st.number_input(
            "Resistance (R2) (kΩ)",
            min_value=0.1, # R2 cannot be zero
            value=100.0,
            step=0.1,
            format="%.1f",
            key="R2_input_schmitt"
        )

        st.markdown("---") # Horizontal line for visual separation.
        st.write("R1 >> R2 (for output wave form)")


    # --- Core Simulation Logic ---
    def generate_waveform(amp, freq, wave_type_val, num_cycles=3):
        """
        Generates the input waveform based on amplitude, frequency, and waveform type.
        """
        # Adjust sampling rate based on frequency to ensure enough points per cycle.
        # At least 100 points per cycle, or a minimum of 1000 points overall.
        if freq == 0:
            sampling_rate = 10000 # Default sampling for DC.
        else:
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

    def simulate_schmitt_trigger(amp_input, actual_frequency, selected_wave_type_int,
                                 R1_val_kohm, R2_val_kohm):
        """
        Performs the Schmitt Trigger simulation and calculates output parameters.
        """
        # Generate the input waveform.
        y_input, t, amp_input_actual, total_duration, input_freq = generate_waveform(
            amp_input, actual_frequency, selected_wave_type_int
        )

        # Convert resistances from kΩ to Ohms.
        R1_val = R1_val_kohm * 1000
        R2_val = R2_val_kohm * 1000

        # Define typical op-amp saturation voltages.
        V_sat_plus = 15.0
        V_sat_minus = -15.0

        # Calculate Upper Threshold Point (V_UTP) and Lower Threshold Point (V_LTP).
        # These are for a non-inverting Schmitt Trigger (positive feedback).
        if (R1_val + R2_val) == 0:
            st.error("Sum of R1 and R2 cannot be zero. Please check resistance values.")
            V_UTP = 0
            V_LTP = 0
            y_output = np.zeros_like(y_input)
        else:
            V_UTP = (R2_val / (R1_val + R2_val)) * V_sat_plus
            V_LTP = (R2_val / (R1_val + R2_val)) * V_sat_minus

            y_output = np.zeros_like(y_input)

            if len(y_input) > 0:
                if y_input[0] > V_UTP:
                    y_output[0] = V_sat_minus # Start low if input is above UTP
                elif y_input[0] < V_LTP:
                    y_output[0] = V_sat_plus # Start high if input is below LTP
                else:
                    y_output[0] = V_sat_plus

            for i in range(1, len(y_input)):
                if y_output[i-1] == V_sat_plus:
                    if y_input[i] > V_UTP:
                        y_output[i] = V_sat_minus
                    else:
                        y_output[i] = y_output[i-1]
                elif y_output[i-1] == V_sat_minus:
                    if y_input[i] < V_LTP:
                        y_output[i] = V_sat_plus
                    else:
                        y_output[i] = y_output[i-1]
            
            y_output = np.clip(y_output, V_sat_minus, V_sat_plus)

        return y_input, y_output, t, amp_input_actual, total_duration, input_freq, \
                 V_UTP, V_LTP, V_sat_plus, V_sat_minus, R1_val_kohm, R2_val_kohm

    # --- CRO Displays ---
    with col3:
        st.header(" Circuit Diagram")
        
        st.image("images/schmitttrigger.png", caption="Schmitt Trigger Circuit", use_container_width=True)   
        
        st.subheader("CRO Displays")

        # Perform the simulation based on current widget values.
        y_input, y_output, t, amp_input, total_duration, input_freq, \
        V_UTP, V_LTP, V_sat_plus, V_sat_minus, R1_val_kohm, R2_val_kohm = simulate_schmitt_trigger(
            amplitude, actual_frequency, selected_wave_type_int,
            R1_val_kohm, R2_val_kohm
        )

        # Plotting for CRO Channel 1 (Input Signal).
        fig1, ax1 = plt.subplots(figsize=(3, 2), dpi=100)
        ax1.plot(t, y_input, color='lime')
        ax1.set_facecolor("black")
        ax1.axhline(0, color='gray', linewidth=0.5)
        ax1.axvline(0, color='gray', linewidth=0.5)
        
        # Plot UTP and LTP lines on input graph for better visualization.
        ax1.axhline(V_UTP, color='red', linestyle='--', linewidth=1, label=f'V_UTP={V_UTP:.2f}V')
        ax1.axhline(V_LTP, color='blue', linestyle='--', linewidth=1, label=f'V_LTP={V_LTP:.2f}V')
        ax1.legend(loc='lower left', fontsize=7, facecolor='darkgray', edgecolor='white')

        # Adjust Y-axis limits to include input amplitude, UTP, and LTP, with padding.
        max_plot_amp = max(amp_input * 1.5, abs(V_UTP) * 1.2, abs(V_LTP) * 1.2)
        if max_plot_amp == 0: max_plot_amp = 1 # Ensure a minimum range if all values are 0.
        ax1.set_ylim(-max_plot_amp, max_plot_amp)
        
        ax1.set_xlim(0, total_duration)
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.set_title("Ch 1: Input Signal", color='white', fontsize=10)
        ax1.text(0.02, 0.95, f'Amp: {amp_input:.2f} V', transform=ax1.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
        st.pyplot(fig1) # Display the Matplotlib figure in Streamlit.

        # Plotting for CRO Channel 2 (Output Signal).
        fig2, ax2 = plt.subplots(figsize=(3, 2), dpi=100)
        ax2.plot(t, y_output, color='cyan')
        ax2.set_facecolor("black")
        ax2.axhline(0, color='gray', linewidth=0.5)
        ax2.axvline(0, color='gray', linewidth=0.5)
        
        # Set Y-axis limits based on saturation voltages with padding.
        ax2.set_ylim(V_sat_minus * 1.2, V_sat_plus * 1.2)
        
        ax2.set_xlim(0, total_duration)
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')
        ax2.set_title("Ch 2: Output Signal", color='white', fontsize=10)
        ax2.text(0.02, 0.95, f'Output High: {V_sat_plus:.2f} V', transform=ax2.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
        ax2.text(0.02, 0.85, f'Output Low: {V_sat_minus:.2f} V', transform=ax2.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
        st.pyplot(fig2) # Display the Matplotlib figure in Streamlit.

        # Plotting for Combined View (Channel 1 & 2).
        fig_combined, ax_combined = plt.subplots(figsize=(6, 3), dpi=100)
        ax_combined.plot(t, y_input, color='lime', label='Input (Ch 1)')
        ax_combined.plot(t, y_output, color='cyan', label='Output (Ch 2)')
        ax_combined.set_facecolor("black")
        ax_combined.axhline(0, color='gray', linewidth=0.5)
        ax_combined.axvline(0, color='gray', linewidth=0.5)
        
        # Plot UTP and LTP lines on combined graph.
        ax_combined.axhline(V_UTP, color='red', linestyle='--', linewidth=1, label=f'V_UTP ({V_UTP:.2f}V)')
        ax_combined.axhline(V_LTP, color='blue', linestyle='--', linewidth=1, label=f'V_LTP ({V_LTP:.2f}V)')

        # Determine combined Y-axis limit.
        max_combined_amp = max(amp_input * 1.5, abs(V_UTP) * 1.2, abs(V_LTP) * 1.2, V_sat_plus * 1.2)
        if max_combined_amp == 0: max_combined_amp = 1
        ax_combined.set_ylim(-max_combined_amp, max_combined_amp)
        
        ax_combined.set_xlim(0, total_duration)
        ax_combined.tick_params(axis='x', colors='white')
        ax_combined.tick_params(axis='y', colors='white')
        ax_combined.set_title("Combined View (Ch 1 & Ch 2)", color='white', fontsize=10)
        ax_combined.legend(loc='upper right', fontsize=8, facecolor='darkgray', edgecolor='white')
        st.pyplot(fig_combined) # Display the Matplotlib figure in Streamlit.

    # --- Dynamic Parameters Table ---
    st.header("Simulation Results")

    # Initialize session state for history if it doesn't exist.
    if 'simulation_history_schmitt' not in st.session_state: # Unique key for this page's history.
        st.session_state.simulation_history_schmitt = []

    # Button to log the current result to the table.
    if st.button("Log Current Results to Table", key="log_button_schmitt"):
        new_entry = {
            "#": len(st.session_state.simulation_history_schmitt) + 1,
            "R1 (kΩ)": f"{R1_val_kohm:.1f}",
            "R2 (kΩ)": f"{R2_val_kohm:.1f}",
            "V_UTP (V)": f"{V_UTP:.2f}",
            "V_LTP (V)": f"{V_LTP:.2f}"
        }
        st.session_state.simulation_history_schmitt.append(new_entry)

    # Display the history as a Pandas DataFrame.
    if st.session_state.simulation_history_schmitt:
        df_history = pd.DataFrame(st.session_state.simulation_history_schmitt)
        st.dataframe(df_history, use_container_width=True) # use_container_width makes the table responsive.

    # Button to clear the table history.
    if st.button("Clear Table History", key="clear_table_button_schmitt"):
        st.session_state.simulation_history_schmitt = [] # Reset the history list.
        st.rerun() # Rerun the app to immediately reflect the cleared table.

# --- Postlab Tab ---
with tab4:
    st.header("Postlab")
    st.markdown("""
    **Conclusion:**
    * Summarize your observations from the simulation, specifically on the relationship between R1, R2, and the threshold voltages.
    * Explain how the hysteresis loop is visible in the combined input-output graph.
    * Discuss the effect of varying the amplitude of the input signal relative to the hysteresis width.

    **Analysis:**
    * If R1 = 10 kΩ and R2 = 1 kΩ, calculate the V_UTP and V_LTP values and verify them with the simulation.
    * What happens to the output if the input signal's peak-to-peak voltage is less than the hysteresis width?
    * How does the Schmitt Trigger circuit solve the problem of false triggering due to noise in a simple comparator circuit?
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