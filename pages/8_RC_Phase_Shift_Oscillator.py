# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 01:38:39 2025

@author: damo3
"""

# pages/7_RC_Phase_Shift_Oscillator.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

st.set_page_config(layout="wide", page_title="RC Phase Shift Oscillator")

st.title("RC Phase Shift Oscillator Simulator")

# Create the tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Objective", "Prelab", "Theory", "Simulation", "Postlab", "Feedback"])
mcq_questions = [
    {
        "question":("The primary purpose of the op-amp in an RC phase shift oscillator is:"),
         "options": [
          " To provide $180^\circ$ of phase shift.",
         " To act as a voltage buffer.",
         "To provide sufficient gain to compensate for the feedback network\'s attenuation.",
         "To filter out unwanted frequencies."
         ],
         
    "correct_option_index": 2,
    "explanation":"The op-amp provides the necessary **amplification** ($A \geq 29$) to ensure the loop gain $ 1$, which is crucial for sustained oscillations according to the Barkhausen criterion."     
         },
    {
     
        "question":("How many RC stages are minimally required in the feedback network of an RC phase shift oscillator to produce $180^\circ$ phase shift?"),
        "options": [
            " One",
         "Two",
         "Three",
         "Four"
          ],
     "correct_option_index": 2,
     "explanation":"A single RC stage can provide a maximum phase shift of $90^\circ$. A minimum of **three** cascaded stages is required to reliably achieve the $180^\circ$ phase shift and maintain stable operation at a specific frequency."
     },
    {
     "question":("If the resistance R in all stages of an RC phase shift oscillator is doubled, the frequency of oscillation ($f_o$) will:"),
     "options": [
         "Remain the same.",
         "Halve (decrease by a factor of 2).",
         "Double (increase by a factor of 2).",
         " Decrease by a factor of $\sqrt{2}$."
         ],
     "correct_option_index": 1,
     "explanation":"The frequency of oscillation is $\mathbf{f_o \\propto \\frac{1}{RC}}$. If $R$ is doubled, the frequency becomes $f'_o \\propto \\frac{1}{(2R)C} = \\frac{1}{2} f_o$. The frequency is **halved**."
     },
    {
     "question":("The total phase shift around the loop in a sustained RC phase shift oscillator must be:"),
     "options": [
         "$90^\circ$",
          "$180^\circ$",
         "$270^\circ$",
         "$360^\circ$ (or $0^\circ$)"
         ],
     "correct_option_index": 3,
     "explanation":"The second condition of the Barkhausen criterion requires the total phase shift around the closed loop to be $0^\circ$ or $360^\circ n$ for positive feedback necessary for oscillation."
    
     },
    {
     "question":("The frequency of oscillation $f_o$ of a three-stage RC phase shift oscillator using identical R and C components is given by:"),
       "options": [
            "$\\frac{1}{2\\pi RC}$",
         "$\\frac{1}{2\\pi RC\\sqrt{2}}$",
         "$\\frac{1}{2\\pi RC\\sqrt{6}}$",
         "$\\frac{1}{2\\pi RC\\sqrt{3}}$"
           ],
     "correct_option_index": 2,
     "explanation":"This is the standard formula for the frequency of oscillation of an RC phase shift oscillator with three identical RC stages."
     }
    ]


mcq_questions1 = [
    {
     "question":"RC phase shift oscillator generates:",
     "options": [ "Square wave", "Triangular wave", "Sine wave", "Sawtooth wave" ],
     "correct_option_index": 2,
     "explanation":"RC phase shift oscillator produces sinusoidal oscillations."
     
     
     },
    {
     "question":"Total phase shift required for oscillation:",
     "options": [ "90°", "180°", "360°", "270°"  ],
     "correct_option_index": 2,
     "explanation":"For sustained oscillations, total phase shift must be 0° or 360°."
     
     },
    {
     "question":"Phase shift provided by each RC section is about:",
     "options": ["30°", "45°", "60°", "90°"  ],
     "correct_option_index": 2,
     "explanation":"Each RC network provides approximately 60° phase shift."
     },
    {
     "question":"Minimum gain for oscillation is:",
     "options": [ "10", "15", "45", "29" ],
     "correct_option_index": 3,
     "explanation":"Theoretical minimum gain is 29 due to RC attenuation." 
     },
    {
     "question":"If gain is reduced below minimum:",
     "options": [ "Frequency increases", "No oscillations", "Output becomes square", "Noise reduces"  ],
     "correct_option_index": 1,
     "explanation":"Oscillations stop if gain is insufficient."
     }
    ]




# --- Prelab Tab ---

with tab1:
    
    st.markdown("""
    **Objective:** To understand the operation of an RC phase shift oscillator and verify the conditions for sustained oscillation.

    **Pre-requisites:**
    1.  Knowledge of operational amplifiers (op-amps).
    2.  Understanding of resistor-capacitor (RC) networks and their phase shifting properties.
    3.  Familiarity with the Barkhausen criterion for oscillation.
    """)



with tab2:
    st.header("Prelab")
    
    
    st.subheader("Multiple Choice Questions (MCQ)")
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
with tab3:
    st.header("Theory")
    st.markdown(r"""
    An **RC phase shift oscillator** is a type of electronic oscillator that generates a sine wave output. It is composed of a three-stage RC ladder network and an inverting amplifier (typically an op-amp).

    ### Principle of Operation
    The circuit operates based on the **Barkhausen Criterion**, which states that for sustained oscillations to occur, two conditions must be met:
    1.  The **loop gain** ($A\beta$) must be equal to or greater than unity ($|A\beta| \ge 1$).
    2.  The **total phase shift** around the feedback loop must be 0° or 360° ($∠A\beta = 0°$ or $360°$).

    ### RC Phase Shift Network
    The oscillator uses a three-stage RC ladder network, which provides a total phase shift of **180°** at a specific frequency. Each RC section contributes a phase shift. While a single RC circuit can provide up to 90° of phase shift, cascading three identical sections allows for a stable 180° shift at the resonant frequency.

    ### The Amplifier
    The amplifier stage is an **inverting amplifier**, which provides its own 180° phase shift. It also provides the necessary gain to compensate for the signal attenuation caused by the RC network. The minimum gain required to overcome the attenuation of the three-stage RC network is **29**. Thus, the gain of the amplifier must be equal to or greater than 29 to satisfy the Barkhausen criterion for loop gain.

    ### Frequency of Oscillation
    The oscillation frequency ($f_o$) is determined by the values of R and C in the RC network and is given by the formula:
    
        
    $$f_o = \frac{1}{2 \pi R C \sqrt{6}}$$
    
    The amplifier gain ($A_v$) required for sustained oscillation is:
    $$A_v = \frac{R_F}{R_1} \ge 29$$
    """)

# --- Simulation Tab ---
with tab4:
    # --- Layout with Columns ---
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.header("Oscillator Parameters")
        
        # Number input for Resistance (R) in kΩ.
        R_kohm = st.number_input(
            "Resistance (R) (kΩ)",
            min_value=0.001,
            value=10.0,
            step=0.1,
            format="%.2f",
            key="R_input_oscillator"
        )
        
        # Number input for Capacitance (C) in µF.
        C_uF = st.number_input(
            "Capacitance (C) (µF)",
            min_value=0.0001,
            value=0.1,
            step=0.001,
            format="%.3f",
            key="C_input_oscillator"
        )
        
        # Number input for Desired Signal Frequency.
        f_desired = st.number_input(
            "Desired Signal Frequency (Hz)",
            min_value=0.0,
            value=100.0,
            step=1.0,
            format="%.1f",
            key="f_desired_input_oscillator"
        )
        
      

    # --- Core Simulation Logic ---
    def calculate_oscillation_parameters(R_kohm, C_uF, f_desired):
        R_ohms = R_kohm * 1000
        C_farads = C_uF * 1e-6
        f_observed = 0.0
        R_calculated_kohm_for_desired = 0.0
        R1_kohm_amp = 0.0
        RF_kohm_amp = 0.0
        
        if R_ohms > 0 and C_farads > 0:
            try:
                f_observed = 1 / (2 * np.pi * R_ohms * C_farads * np.sqrt(6))
            except ZeroDivisionError:
                st.error("R or C cannot be zero for frequency calculation.")
                f_observed = 0.0
        else:
            st.warning("Resistance (R) and Capacitance (C) must be positive for oscillation.")
            f_observed = 0.0
            
        if f_desired > 0 and C_farads > 0:
            try:
                R_calc_ohms_for_desired = 1 / (2 * np.pi * f_desired * C_farads * np.sqrt(6))
                R_calculated_kohm_for_desired = R_calc_ohms_for_desired / 1000
            except ZeroDivisionError:
                st.error("Desired frequency or capacitance cannot be zero for R calculation.")
                R_calculated_kohm_for_desired = 0.0
        else:
            R_calculated_kohm_for_desired = 0.0

        if R_calculated_kohm_for_desired > 0:
            R1_kohm_amp = 10 * R_calculated_kohm_for_desired
            RF_kohm_amp = 29 * R1_kohm_amp
        else:
            R1_kohm_amp = 10.0
            RF_kohm_amp = 29 * R1_kohm_amp

        num_cycles = 5
        amp = 1.0
        
        total_duration = num_cycles / f_observed if f_observed != 0 else 0.01
        sampling_rate = max(100 * f_observed, 1000) if f_observed != 0 else 10000
        num_points = int(sampling_rate * total_duration)
        if num_points < 2: num_points = 2

        t = np.linspace(0, total_duration, num_points, endpoint=False)
        y_signal = amp * np.sin(2 * np.pi * f_observed * t)
        
        time_period = 1 / f_observed if f_observed != 0 else float('inf')

        return {
            "R_input_kohm": R_kohm,
            "C_input_uF": C_uF,
            "f_desired": f_desired,
            "output_amplitude": amp,
            "time_period_s": time_period,
            "f_output": f_observed,
            "R_calculated_kohm_for_desired": R_calculated_kohm_for_desired,
            "R1_kohm_amp": R1_kohm_amp,
            "RF_kohm_amp": RF_kohm_amp,
            "y_signal": y_signal,
            "t_time": t,
            "total_duration": total_duration
        }
    with col2:    
            st.header("Calculated Values")
    # 3. RUN THE CALCULATION (Crucial step - must be after inputs, but before outputs)
            sim_results = calculate_oscillation_parameters(R_kohm, C_uF, f_desired)
    # st.metric requires: label, value (formatted as a string if you want decimals)
            st.metric(
              label="Calculated Frequency (f)",
              value=f"{sim_results['f_output']:.2f} Hz"
             )
    
    # Additional helpful metrics
            st.metric(
              label="Required R (for Desired Freq)",
              value=f"{sim_results['R_calculated_kohm_for_desired']:.2f} kΩ"
             )
          

    # --- CRO Display and Simulation Results ---
    with col3:
        st.header("Circuit Diagram")
        
        st.image("images/RCphaseshiftoscillator.png", caption="RC Phaseshift Oscillator Circuit", width='stretch')
        
    st.subheader("CRO Display")
    st.text_input("Your Name",key="p2")
    sim_results = calculate_oscillation_parameters(R_kohm, C_uF, f_desired)

        # Plotting for Output Signal (CH1)
    fig1, ax1 = plt.subplots(figsize=(6, 3), dpi=100)
    ax1.plot(sim_results["t_time"], sim_results["y_signal"], color='red')
    ax1.set_title("Oscillator Output Signal")
    ax1.set_xlabel("Time (sec)")
    ax1.set_ylabel("Amplitude (V)")
    ax1.grid(True)
    ax1.set_facecolor("black")
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
        
    plot_ylim = sim_results["output_amplitude"] * 1.5 if sim_results["output_amplitude"] != 0 else 1.0
    ax1.set_ylim(-plot_ylim, plot_ylim)
    ax1.set_xlim(0, sim_results["total_duration"])
    ax1.tick_params(axis='x', colors='black')
    ax1.tick_params(axis='y', colors='black')
        
    ax1.text(0.02, 0.95, f'Amp: {sim_results["output_amplitude"]:.2f} V', transform=ax1.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    ax1.text(0.02, 0.85, f'Freq: {sim_results["f_output"]:.2f} Hz', transform=ax1.transAxes,
                  fontsize=8, color='white', verticalalignment='top')
    st.pyplot(fig1)

    



    st.header("Simulation Results")

# 1. Initialize session state
    if 'oscillator_history' not in st.session_state:
        st.session_state.oscillator_history = []

# 2. Handle the "Log" Button Logic
    if st.button("Log Current Results to Table", key="log_button_oscillator"):
        new_entry = {
        "Input R (kΩ)": f"{sim_results['R_input_kohm']:.2f}",
        "Input C (µF)": f"{sim_results['C_input_uF']:.2f}",
        "Desired Freq (Hz)": f"{sim_results['f_desired']:.2f}",
        "Output Amp (V)": f"{sim_results['output_amplitude']:.2f}",
        "Time Period (s)": f"{sim_results['time_period_s']:.4f}",
        "Output Freq (Hz)": f"{sim_results['f_output']:.2f}",
        "Calc. R for F_des (kΩ)": f"{sim_results['R_calculated_kohm_for_desired']:.2f}",
        "R1 (kΩ)": f"{sim_results['R1_kohm_amp']:.2f}",
        "RF (kΩ)": f"{sim_results['RF_kohm_amp']:.2f}"
        }
        st.session_state.oscillator_history.append(new_entry)
        st.rerun()

# 3. Handle the Table Display Logic
    if st.session_state.oscillator_history:
    # START building the string
        markdown_table = (
        "| **Input R (kΩ)** | **Input C (µF)** | **Desired Freq (Hz)** | **Output Amp (V)** | **Time Period (s)** | **Output Freq (Hz)** | **Calc. R for $F_{des}$ (kΩ)** | **$R_1$ (kΩ)** | **$R_F$ (kΩ)** |\n"
        "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n"
        )

    # LOOP to add rows to the string
        for entry in st.session_state.oscillator_history:
            row_str = (
            f"| {entry['Input R (kΩ)']} "
            f"| {entry['Input C (µF)']} "
            f"| {entry['Desired Freq (Hz)']} "
            f"| {entry['Output Amp (V)']} "
            f"| {entry['Time Period (s)']} "
            f"| {entry['Output Freq (Hz)']} "
            f"| {entry['Calc. R for F_des (kΩ)']} "
            f"| {entry['R1 (kΩ)']} "
            f"| {entry['RF (kΩ)']} |\n"
            )
            markdown_table += row_str

    # DISPLAY the final string (Ensure this is NOT indented under the 'for' loop)
        st.markdown(markdown_table)

# 4. Clear Table Logic
    if st.button("Clear Table History", key="clear_table_button_oscillator"):
        st.session_state.oscillator_history = []
        st.rerun()

# --- Postlab Tab ---
with tab5:
    st.header("Postlab")
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