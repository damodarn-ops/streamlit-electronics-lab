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

mcq_questions = [
    {
        "question":("What is the primary function of the RC circuit (RF and C) in this generator?"),
            "options": [
                "Filter the output signal to produce a pure sine wave.",
    "Provide a time-dependent voltage for the inverting input ($V_{in-}$), which dictates the switching points.",
    "Stabilize the DC operating point of the op-amp.",
    "Set the output amplitude (peak-to-peak voltage) of the square wave."
                ],
            "correct_option_index":1 ,
            "explanation":"The resistor $R_F$ and capacitor $C$ form a **timing circuit**. The capacitor's voltage $V_C$ charges and discharges exponentially towards the op-amp's output voltage. This voltage, fed back to the inverting input, is the $\\mathbf{V_{in-}}$ signal that is compared against the threshold voltage set by the $R_1/R_2$ divider. The time it takes to charge/discharge determines the oscillation **period**. "
            },
    
    {
        "question":("What is the role of the voltage divider (R1 and R2) at the non-inverting input?"),
            "options": [
                "The value of the timing resistor ($R_F$).",
    "The values of the voltage divider resistors ($R_1$ and $R_2$).",
    " The power supply voltages** ($\pm V_{CC}$) connected to the op-amp.",
    " The charging time constant ($\\tau = R_F C$)."
                ],
            "correct_option_index":2,
            "explanation":"The op-amp output voltage ($V_o$) is constrained by the power supplies ($\pm V_{CC}$). In saturation, the output voltage is near, but slightly less than, the supply voltage. Thus, $\mathbf{V_{sat} \\approx V_{CC}}$. The other components determine the **frequency**, not the amplitude."
            },
    {
        "question":("Identify the concept of positive and negative saturation in an op-amp."),
            "options": [
                " Ensure a linear, sinusoidal output waveform.",
    " Precisely control the charging and discharging of the capacitor.",
    " Force the output to quickly switch and remain at one of the saturation voltages ($+V_{sat}$ or $-V_{sat}$)." ,
    " Decrease the overall gain of the circuit for stability."
                ],
            "correct_option_index":2 ,
            "explanation":" Positive feedback is key for **comparator circuits and oscillators**. When the input voltages $V_{in+}$ and $V_{in-}$ cross, the positive feedback causes the op-amp to swiftly and decisively switch its output to the opposite saturation limit (either $+V_{sat}$ or $-V_{sat}$), maintaining the stable-but-temporary state required for oscillation."
            },
    {
        "question":("How does the capacitor's voltage affect the op-amp's output state?"),
            "options": [
                " Ground (0V).",
    " Positive saturation ($+V_{sat}$).",
    " Negative saturation ($-V_{sat}$).",
    "Oscillating rapidly between $+V_{sat}$ and $-V_{sat}$."
                ],
            "correct_option_index":1 ,
            "explanation":" The op-amp is acting as a comparator. If $\mathbf{V_{in+} > V_{in-}}$ (non-inverting input voltage is greater), the output is driven to the **maximum positive limit** ($+V_{sat}$). The capacitor voltage $V_C$ is $V_{in-}$, and $V_{ref}$ is $V_{in+}$."
            },
    {
        "question":("How would changing the value of C or RF affect the output frequency?"),
            "options": [
                " Decrease the value of the capacitor $C$.",
    " Decrease the value of the timing resistor $R_F$.",
    " Increase the value of $C$ or $R_F$** (or both).",
    "Only change the ratio of $R_1$ and $R_2$."
                ],
            "correct_option_index":2 ,
            "explanation":"The oscillation **frequency ($f$)** is inversely proportional to the **time constant** $\\tau = R_F C$. The formula for the frequency is $f = \\frac{1}{2 R_F C \\ln(1 + 2R_2/R_1)}$. To **decrease** the frequency (i.e., increase the period), you must **increase** the time constant $\\tau$, which means increasing $R_F$ or $C$."
            }
    ]
    


# --- Prelab Tab ---
with tab1:
    st.header("Prelab")
    st.markdown("""
    **Objective:** To understand the operation of an op-amp based square wave generator (astable multivibrator) and its relationship to the circuit's components.

    **Pre-requisites:**
    1.  Basic knowledge of operational amplifiers (op-amps) and their comparator function.
    2.  Understanding of resistor-capacitor (RC) circuits and their charging/discharging behavior.
    3.  Familiarity with positive feedback in op-amp circuits.

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
        
        st.image("images/squarewavegenerator.png", caption="Square Wave Generator Circuit", width='stretch')
        
        st.subheader("CRO Display")
        st.text_input("Your Name",key="p2")
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
                st.dataframe(df_history, width='stretch')
    
    if st.button("Clear Table History", key="clear_table_button_sq_wave"):
                st.session_state.square_wave_history = []
                st.rerun()
    else:
            st.warning("Please adjust parameters to allow for oscillation.")

# --- Postlab Tab ---
with tab4:
    st.header("Postlab")
    st.text_input("Your Name",key="p3")
    st.subheader("Conclusion:")
    st.write(" Summarize your observations from the simulation regarding the effect of changing RF, C, R1, and R2 on the output frequency and amplitude.")
    st.text_area("Your Answer ", height=100, key="postlab_q1")
    st.write(" Explain why this circuit is often called a free-running or astable multivibrator.")
    st.text_area("Your Answer ", height=100, key="postlab_q2")
    st.write(" What would happen if the capacitor C was replaced by a short circuit? Explain the outcome.")
    st.text_area("Your Answer ", height=100, key="postlab_q3")

    st.subheader("Analysis:")
    st.write(" Using the formula, calculate the period and frequency of the square wave if $R_F = 20k\Omega$, $C = 0.05\mu F$, $R_1 = 10k\Omega$, and $R_2 = 10k\Omega$.")
    st.text_area("Your Answer ", height=100, key="postlab_q4")
    st.write(" If you wanted to double the frequency of the output, what simple change could you make to the circuit's components?")
    st.text_area("Your Answer ", height=100, key="postlab_q5")
    st.write("How does the output amplitude of the square wave relate to the op-amp's power supply?")
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