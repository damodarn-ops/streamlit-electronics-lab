# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:47:47 2025

@author: damo3
"""

# pages/10_Active_Filter.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

st.set_page_config(layout="wide", page_title="Active Filter")

st.title("Active Filter Simulator")

# Create the tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Objective", "Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

# Define the MCQs and answers
mcq_questions = [
    {
        "question": " The primary difference between an active and passive filter is the use of:",
        "options": ["Resistors only", "Capacitors only", "An active component like an op-amp", "Inductors only"],
        "answer_index": 2,
        "explanation": "Active filters use active components (like op-amps or transistors) to provide gain and buffering, while passive filters only use passive components (resistors, capacitors, inductors)."
    },
    {
        "question": " A key advantage of an active filter is that it can:",
        "options": ["Only attenuate signals", "Provide signal gain", "Only be used for low frequencies", "Work without a power supply"],
        "answer_index": 1,
        "explanation": "Active filters, unlike passive filters, can provide voltage gain in the passband, amplifying the signal."
    },
    {
        "question": " The cutoff frequency ($f_c$) of a first-order RC filter is determined by the values of:",
        "options": ["Resistance and Inductance", "Capacitance and Inductance", "Resistance and Capacitance", "Voltage and Current"],
        "answer_index": 2,
        "explanation": "The cutoff frequency for an RC filter is directly dependent on the values of the resistor (R) and capacitor (C), calculated as $f_c = \\frac{1}{2\\pi RC}$."
    },
    # --- New MCQ 4 ---
    {
        "question": " The primary role of the Op-Amp in a first-order active filter is to:",
        "options": ["Set the cutoff frequency.", "Act as a current sink.", "Provide gain and isolate the filter stage from the load.", "Serve as the passive RC component."],
        "answer_index": 2,
        "explanation": "The op-amp provides voltage gain in the passband and, most importantly, acts as a buffer (isolating the filter stage from the next stage/load), which prevents the load from affecting the filter's characteristic frequency."
    },
    # --- New MCQ 5 ---
    {
        "question": " The voltage gain ($A_v$) for the non-inverting op-amp configuration used in many active filters is given by the formula:",
        "options": ["$A_v = -\\frac{R_f}{R_{in}}$", "$A_v = 1 + \\frac{R_f}{R_{g}}$", "$A_v = \\frac{R_f}{R_{in}}$", "$A_v = 1$"],
        "answer_index": 1,
        "explanation": "The voltage gain of a non-inverting op-amp amplifier is set by the feedback resistor ($R_f$) and the resistor to ground ($R_g$, often called $R_1$ and $R_2$ in the prelab) using the formula $A_v = 1 + \\frac{R_f}{R_{g}}$."
    }
]

mcq_questions1 = [
    {
     "question":"Low-pass filter allows:",
     "options": ["High", "Low", "All", "None"   ],
     "correct_option_index": 1,
     "explanation":"LPF allows low frequencies to pass while attenuating high frequencies."
     
     
     },
    {
     "question":"At cut-off frequency, output becomes:",
     "options": ["Zero", "Max", "0.707 times", "2 times"  ],
     "correct_option_index": 2,
     "explanation":"At cut-off frequency, output drops to 1/√2 (~0.707) of maximum."
     
     },
    {
     "question":"Cut-off frequency formula of first order LPF:",
     "options": ["$1/RC$", "$1/2πRC$", "πRC", "2πRC" ],
     "correct_option_index": 1,
     "explanation":"The cut-off frequency for a first-order RC filter is $f_c$ = $1/(2πRC)$."
     },
    {
     "question":"Roll-off rate of first order HPF",
     "options": ["+20 dB/dec", "-20 dB/dec", "0 dB/dec", "-40 dB/dec"  ],
     "correct_option_index": 0,
     "explanation":"HPF has a +20 dB/decade slope below the cut-off frequency." 
     },
    {
     "question":"Phase shift at fc (HPF):",
     "options": [ "0°", "+45°", "-45°", "90°"   ],
     "correct_option_index": 1,
     "explanation":"At cut-off, HPF introduces a phase shift of +45°."
     }
    ]




with tab1:
    
    st.markdown("""
    **Objective:** To understand the operation and frequency response of first-order active low-pass and high-pass filters.

    **Pre-requisites:**
    1.  Understanding of basic passive RC filter circuits.
    2.  Knowledge of operational amplifiers (op-amps) in non-inverting amplifier configuration.
    3.  Familiarity with concepts like cutoff frequency ($f_c$) and gain.

    
    """)

# --- Prelab Tab ---
with tab2:
    st.header("Prelab: Active Filters")
    
    st.markdown("---")
    st.header("Multiple Choice Questions (MCQ)")
    st.text_input("Your Name",key="p1")
    user_answers = {}
    for i, mcq in enumerate(mcq_questions):
       question_number = i + 1  # Calculates the question number starting from 1
     # Display the question with the number prepended
       question_prompt = f"**Question {question_number}**: {mcq['question']}"
       
       # *** FIX HERE: Use question_prompt instead of mcq["question"] ***
       user_answers[i] = st.radio(question_prompt, mcq["options"], key=f"mcqp_{i}")

    if st.button("Submit Answers", key="submit_mcq1"):
       st.subheader("Results")
       # Initialize score variables
       correct_count = 0
       total_questions = len(mcq_questions)
       
       all_correct = True
       for i, mcq in enumerate(mcq_questions):
           correct_answer = mcq["options"][mcq["correct_option_index"]]
           if user_answers[i] == correct_answer:
               st.success(f"**Question {i+1}: Correct!** ✅")
               st.markdown(f"**Explanation:** {mcq['explanation']}")
               correct_count += 1  # Increment the score
           else:
               st.error(f"**Question {i+1}: Incorrect.** ❌")
               st.markdown(f"**Correct Answer:** {correct_answer}")
               st.markdown(f"**Explanation:** {mcq['explanation']}")
               all_correct = False
       # Display the final score immediately after the per-question results
       st.markdown("---")
       st.subheader(f"📊 Final Score: {correct_count} / {total_questions}")
       st.markdown("---")
       
       if all_correct:
           st.balloons()
           st.info("You've answered all questions correctly! . 🎉")
       else:
           st.warning("Please review the theory and try again. 🤔")


# --- Theory Tab ---
# --- Theory Tab ---
with tab3:
    st.header("Theory: Active Filter Fundamentals")
    st.markdown(r"""
    An **active filter** uses an active component like an **op-amp** in addition to resistors (R) and capacitors (C). The op-amp provides **gain** and acts as a **buffer**, preventing the filter from being loaded by subsequent stages.

    ### First-Order Active Low-Pass Filter
    A low-pass filter allows low-frequency signals to pass through while attenuating high-frequency signals.
    
    * **Cutoff Frequency ($f_c$):** The frequency at which the output power is half of the input power, or the gain is attenuated by 3 dB.
       
    
    $$f_c = \frac{1}{2 \pi R C}$$
    * **Passband Gain ($A_v$):** The gain of the filter at frequencies below the cutoff.
        $$A_v = 1 + \frac{R_F}{R_1}$$

    ### First-Order Active High-Pass Filter
    A high-pass filter allows high-frequency signals to pass through while attenuating low-frequency signals.
    
    * **Cutoff Frequency ($f_c$):** Same as the low-pass filter, determined by the R and C values.
        $$f_c = \frac{1}{2 \pi R C}$$
    * **Passband Gain ($A_v$):** The gain of the filter at frequencies above the cutoff.
        $$A_v = 1 + \frac{R_F}{R_1}$$
        
     $$A_v(dB) =20*log(A_v)$$
    """)

# --- Simulation Tab ---
with tab4:
    # --- Layout with Columns ---
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.header("Function Generator")
        wave_type = st.radio(
            "Select Waveform",
            ("Sine wave", "Cosine wave", "Triangular wave", "Square wave"),
            index=0,
            key="wave_type_radio_filter"
        )
        wave_type_map = {"Sine wave": 1, "Cosine wave": 2, "Triangular wave": 3, "Square wave": 4}
        selected_wave_type_int = wave_type_map[wave_type]

        amplitude = st.slider("Amplitude (V)", 0.0, 5.0, 1.0, 0.001, key="amplitude_slider_filter")

        st.subheader("Frequency")
        freq_val = st.slider("Frequency Value", 0.0, 1100.0, 100.0, 0.001, key="frequency_slider_filter")
        current_freq_unit = st.radio(
            "Frequency Unit",
            ("Hz", "kHz", "MHz"),
            index=0,
            horizontal=True,
            key="freq_unit_radio_filter"
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
        st.header("Active Filter Type")
        filter_type = st.radio(
            "Select Filter Type",
            ("Lowpass Filter", "Highpass Filter"),
            index=0,
            key="filter_type_radio"
        )
        filter_type_map = {"Lowpass Filter": 1, "Highpass Filter": 2}
        selected_filter_type_int = filter_type_map[filter_type]

        R1_kohm = st.number_input(
            "$R_1$ (kΩ) (Gain Resistor)",
            min_value=0.001,
            value=10.0,
            step=0.1,
            format="%.3f",
            key="R1_input_filter"
        )
        RF_kohm = st.number_input(
            "$R_f$ (kΩ) (Feedback Resistor)",
            min_value=0.001,
            value=10.0,
            step=0.1,
            format="%.3f",
            key="RF_input_filter"
        )
        C_uF = st.number_input(
            "C (µF) (Filter Capacitor)",
            min_value=0.0001,
            value=0.1,
            step=0.001,
            format="%.5f",
            key="C_input_filter"
        )
        R_kohm = st.number_input(
            "R (kΩ) (Filter Resistor)",
            min_value=0.001,
            value=10.0,
            step=0.1,
            format="%.3f",
            key="R_input_filter"
        )

      

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

    def get_filter_name(filter_type_value):
        if filter_type_value == 1:
            return "Lowpass Filter"
        elif filter_type_value == 2:
            return "Highpass Filter"
        return "N/A"

    def simulate_filter_circuit(amp_input, actual_frequency, selected_wave_type_int,
                                selected_filter_type_int, R1_kohm, RF_kohm, C_uF, R_kohm):
        y_input, t, amp_input_actual, total_duration, input_freq = generate_waveform(
            amp_input, actual_frequency, selected_wave_type_int
        )

        R1_ohms = R1_kohm * 1000
        RF_ohms = RF_kohm * 1000
        C_farads = C_uF * 1e-6
        R_ohms = R_kohm * 1000

        y_output = np.zeros_like(y_input)
        
        filter_name = get_filter_name(selected_filter_type_int)

        Av_ideal = 1 + (RF_ohms / R1_ohms) if R1_ohms != 0 else float('inf')

        fc = 0.0
        if R_ohms > 0 and C_farads > 0:
            fc = 1 / (2 * np.pi * R_ohms * C_farads)
        else:
            st.error("R and C for filter must be non-zero to calculate cutoff frequency.")
            return y_input, np.zeros_like(y_input), t, amp_input_actual, total_duration, \
                   input_freq, 0.0, 0.0, 0.0, filter_name, 1.0, "No Output/Blocked", 0.0

        if selected_filter_type_int == 1:
            if input_freq == 0:
                y_output = y_input * Av_ideal
            else:
                normalized_freq = input_freq / fc
                gain_at_freq = Av_ideal / np.sqrt(1 + (normalized_freq)**2)
                y_output = y_input * gain_at_freq

        elif selected_filter_type_int == 2:
            if input_freq == 0:
                y_output = np.zeros_like(y_input)
            else:
                normalized_freq = input_freq / fc
                gain_at_freq = Av_ideal * normalized_freq / np.sqrt(1 + (normalized_freq)**2)
                y_output = y_input * gain_at_freq

        clipping_limit = 15.0
        y_output = np.clip(y_output, -clipping_limit, clipping_limit)
        
        output_amplitude = np.max(np.abs(y_output)) if len(y_output) > 0 else 0.0
        
        amplitude_display_text = f'Amp: {output_amplitude:.2f} V'
        if abs(output_amplitude - clipping_limit) < 0.01 and amp_input_actual > 0 and output_amplitude > 0:
            amplitude_display_text += ' (Clipped)'
        elif output_amplitude == 0 and amp_input_actual != 0:
            amplitude_display_text += ' (No Output/Blocked)'

        gain_vv = 0.0
        gain_db = -999.0

        if amp_input_actual > 0:
            gain_vv = output_amplitude / amp_input_actual
            if gain_vv > 0:
                gain_db = 20 * np.log10(gain_vv)
            else:
                gain_db = -float('inf')
        else:
            gain_vv = float('nan')
            gain_db = float('nan')

        plot_ylim_output = max(output_amplitude * 1.2, 1.0)

        return y_input, y_output, t, amp_input_actual, total_duration, input_freq, \
               output_amplitude, gain_vv, gain_db, filter_name, plot_ylim_output, amplitude_display_text, fc

    # --- CRO Displays and Plotting ---
    with col3:
        (y_input, y_output, t, amp_input_actual, total_duration, input_freq, 
 output_amplitude, gain_vv, gain_db, filter_name, plot_ylim_output, 
 amplitude_display_text, fc) = simulate_filter_circuit(
    amplitude, actual_frequency, selected_wave_type_int,
    selected_filter_type_int, R1_kohm, RF_kohm, C_uF, R_kohm
)
        # Helper function to format frequency for the metric
        def format_freq(f):
         if f >= 1e6: return f"{f/1e6:.2f} MHz"
         if f >= 1e3: return f"{f/1e3:.2f} kHz"
         return f"{f:.2f} Hz"
     
       
        st.header("Calculated Values")
        st.metric(
          label="Cutoff Frequency ($f_c$)", 
            value=format_freq(fc)
         )
        gain_display = f"{gain_db:.2f} dB" if gain_db != -float('inf') else "-∞ dB"
        st.metric(
           label="Calculated Gain", value=gain_display
           )
        st.header(" Circuit Diagram")
        
        if filter_type == "Lowpass Filter":
            st.image("images/LPF.png", caption="Lowpass Filter Circuit", width='stretch')
        elif filter_type == "Highpass Filter":
            st.image("images/HPF.png", caption="Highpass Filter Circuit", width='stretch')
        
    st.header("CRO Displays")
    st.text_input("Your Name",key="p2")
# Create three columns *outside* the col1/col2/col3 definition to span the full width
    plot_col1, plot_col2 = st.columns(2)
    sim_data = simulate_filter_circuit(
            amplitude, actual_frequency, selected_wave_type_int,
            selected_filter_type_int, R1_kohm, RF_kohm, C_uF, R_kohm
        )

    y_input, y_output, t, amp_input, total_duration, input_freq, \
    output_amplitude, gain_vv, gain_db, filter_name, plot_ylim_output, amplitude_display_text, fc = sim_data

    fig1, ax1 = plt.subplots(figsize=(3, 2), dpi=100)
    ax1.plot(t, y_input, color='lime')
    ax1.set_facecolor("black")
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
        
    max_plot_amp_input = amp_input * 1.5 if amp_input != 0 else 1.0
    ax1.set_ylim(-max_plot_amp_input, max_plot_amp_input)
        
    ax1.set_xlim(0, total_duration)
    ax1.tick_params(axis='x', colors='black')
    ax1.tick_params(axis='y', colors='black')
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Amplitude (V)")
    ax1.set_title("Ch 1: Input Signal", color='black', fontsize=10)
    ax1.text(0.02, 0.95, f'Amp: {amp_input:.2f} V', transform=ax1.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    with plot_col1:    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(3, 2), dpi=100)
    ax2.plot(t, y_output, color='cyan')
    ax2.set_facecolor("black")
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
    current_max = np.max(np.abs(y_output))
    dynamic_ylim = (current_max * 1.5) if current_max > 0 else 1.0
    ax2.set_ylim(-dynamic_ylim, dynamic_ylim)
    ax2.set_xlim(0, total_duration)
    ax2.tick_params(axis='x', colors='black')
    ax2.tick_params(axis='y', colors='black')
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Amplitude (V)")
    ax2.set_title("Ch 2: Output Signal", color='black', fontsize=10)
    ax2.text(0.02, 0.95, amplitude_display_text, transform=ax2.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    with plot_col2:    st.pyplot(fig2)

    st.subheader("Frequency Response (Gain vs. Frequency)")

    if 'frequency_response_data' not in st.session_state:
            st.session_state.frequency_response_data = []
    if 'sl_no_counter_filter' not in st.session_state:
            st.session_state.sl_no_counter_filter = 0

    if st.button("Add Current Point & Log to Table", key="add_point_log_button"):
            st.session_state.sl_no_counter_filter += 1

            freq_str = f"{input_freq:.2f}"
            amp_in_str = f"{amp_input:.2f}"
            amp_out_str = f"{output_amplitude:.2f}"
            gain_vv_str = f"{gain_vv:.3f}" if not np.isnan(gain_vv) else "N/A"
            gain_db_str = f"{gain_db:.2f}" if not np.isinf(gain_db) and not np.isnan(gain_db) else ("-Inf" if np.isinf(gain_db) else "N/A")

            new_table_entry = {
                "Sl No.": st.session_state.sl_no_counter_filter,
                "Input Freq (Hz)": freq_str,
                "Input Amp (V)": amp_in_str,
                "Output Amp (V)": amp_out_str,
                "Gain (V/V)": gain_vv_str,
                "Gain (dB)": gain_db_str
            }
            if 'filter_table_history' not in st.session_state:
                st.session_state.filter_table_history = []
            st.session_state.filter_table_history.append(new_table_entry)
            
            if input_freq > 0 and not np.isinf(gain_db) and not np.isnan(gain_db):
                st.session_state.frequency_response_data.append((input_freq, gain_db))
            
            st.rerun()

    fig_semilog, ax_semilog = plt.subplots(figsize=(6, 3), dpi=100)
    ax_semilog.set_facecolor("black")
    ax_semilog.axhline(0, color='gray', linewidth=0.5)
    ax_semilog.axvline(0, color='gray', linewidth=0.5)
        
    if not st.session_state.frequency_response_data:
            ax_semilog.text(0.5, 0.5, "No data to plot.\nClick 'Add Current Point & Log to Table'.",
                             horizontalalignment='center', verticalalignment='center',
                             transform=ax_semilog.transAxes, color='white', fontsize=12)
    else:
            sorted_data = sorted(st.session_state.frequency_response_data, key=lambda x: x[0])
            frequencies_plot = [d[0] for d in sorted_data]
            gains_db_plot = [d[1] for d in sorted_data]

            ax_semilog.semilogx(frequencies_plot, gains_db_plot, 'o-', color='yellow')
            ax_semilog.set_xlabel("Frequency (Hz)", color='black')
            ax_semilog.set_ylabel("Gain (dB)", color='black')
            ax_semilog.set_title("Frequency Response (Gain vs. Frequency)", color='white', fontsize=10)
            ax_semilog.tick_params(axis='x', colors='black')
            ax_semilog.tick_params(axis='y', colors='black')
            ax_semilog.grid(True, which="both", ls="-", color='gray', alpha=0.5)
            
            if fc > 0 and not np.isinf(fc) and not np.isnan(fc):
                ax_semilog.axvline(fc, color='red', linestyle=':', label=f'Cutoff Freq: {fc:.2f} Hz')
                ax_semilog.legend(loc='upper right', fontsize=7, facecolor='darkgray', edgecolor='white')

    st.pyplot(fig_semilog)

    col_clear1, col_clear2 = st.columns(2)
    with col_clear1:
            if st.button("Clear Freq Response Plot", key="clear_freq_plot_button"):
                st.session_state.frequency_response_data = []
                st.rerun()
    with col_clear2:
            if st.button("Clear Table History", key="clear_table_history_button"):
                st.session_state.filter_table_history = []
                st.session_state.sl_no_counter_filter = 0
                st.rerun()

    st.subheader("Simulation Results Table")
    if 'filter_table_history' in st.session_state and st.session_state.filter_table_history:
            df_history = pd.DataFrame(st.session_state.filter_table_history)
            st.dataframe(df_history, width='stretch')
    else:
            st.info("No simulation results logged yet. Adjust parameters and click 'Add Current Point & Log to Table'.")

# --- Postlab Tab ---
with tab5:
    st.header("Postlab: Analysis and Conclusion")
    st.text_input("Your Name",key="p3")
    user_answers = {}
    for i, mcq in enumerate(mcq_questions1):
        question_number = i + 1  # Calculates the question number starting from 1
      # Display the question with the number prepended
        question_prompt = f"**Question {question_number}**: {mcq['question']}"
        
        # *** FIX HERE: Use question_prompt instead of mcq["question"] ***
        user_answers[i] = st.radio(question_prompt, mcq["options"], key=f"mcq_{i}")

    if st.button("Submit Answers", key="submit_mcq"):
        st.subheader("Results")
        # Initialize score variables
        correct_count = 0
        total_questions = len(mcq_questions1)
        
        all_correct = True
        for i, mcq in enumerate(mcq_questions1):
            correct_answer = mcq["options"][mcq["correct_option_index"]]
            if user_answers[i] == correct_answer:
                st.success(f"**Question {i+1}: Correct!** ✅")
                st.markdown(f"**Explanation:** {mcq['explanation']}")
                correct_count += 1  # Increment the score
            else:
                st.error(f"**Question {i+1}: Incorrect.** ❌")
                st.markdown(f"**Correct Answer:** {correct_answer}")
                st.markdown(f"**Explanation:** {mcq['explanation']}")
                all_correct = False
        # Display the final score immediately after the per-question results
        st.markdown("---")
        st.subheader(f"📊 Final Score: {correct_count} / {total_questions}")
        st.markdown("---")
        
        if all_correct:
            st.balloons()
            st.info("You've answered all questions correctly! . 🎉")
        else:
            st.warning("Please review the theory and try again. 🤔")

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