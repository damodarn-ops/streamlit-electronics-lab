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

st.title("Wien Bridge Oscillator Simulator")

# Create the tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Prelab", "Theory", "Simulation", "Postlab", "Feedback"])
mcq_questions = [
    {
        "question":("What is the total phase shift provided by the Wien Bridge network at the oscillation frequency ($f_o$)?"),
        "options": [
            "$90^\circ$",
          "$180^\circ$",
         "$0^\circ$",
         "$270^\circ$"
         ],
        "correct_option_index": 2,
        "explanation":"The Wien Bridge network is a band-pass filter that provides **$0^\circ$ phase shift** at its resonant frequency ($f_o$). Since the amplifier is non-inverting (also $0^\circ$ phase shift), the total loop phase shift is $0^\circ$, satisfying the Barkhausen criterion."
   },
    
    {
     "question":("What is the minimum amplifier gain ($A$) required to sustain oscillation in a Wien Bridge oscillator?"),
      "options": [
             "$A \ge 1$",
         "$A \ge 29$",
         " $A \ge 3$",
         "$A \ge \sqrt{2}$"
         ],
     "correct_option_index": 2,
     "explanation":"The attenuation ($\\beta$) of the Wien Bridge at $f_o$ is $\\mathbf{1/3}$. To meet the Barkhausen criterion ($\\mathbf{|A\\beta| \\ge 1}$), the minimum gain must be $\\mathbf{A_{\\text{min}} = \\frac{1}{\\beta} = \\frac{1}{1/3} = 3}$."
     },
    {
     "question":("If both the resistance ($R$) and capacitance ($C$) in the bridge network are doubled, the oscillation frequency ($f_o$) will:"),
     "options": [
         "Double.",
         "Halve.",
         "Quarter (decrease by a factor of 4).",
         "Remain the same."
         ],
     "correct_option_index": 2,
     "explanation":"The frequency formula is $\mathbf{f_o = \\frac{1}{2\\pi RC}}$. If both $R$ and $C$ are doubled, the new frequency $f'_o$ is $\\frac{1}{2\\pi (2R)(2C)} = \\frac{1}{4} \\left(\\frac{1}{2\\pi RC}\\right)$. The frequency is **quartered**."
     },
    {
     "question":("In a practical Wien Bridge oscillator, what is typically used to stabilize the output amplitude and prevent waveform distortion?"),
      "options": [
          "A high-pass filter.",
         "A Zener diode or thermistor in the negative feedback loop.",
          "A three-stage RC ladder network.",
          "A crystal resonator."
          ],
      "correct_option_index": 1,
      "explanation":"A practical Wien Bridge requires **Automatic Gain Control (AGC)** to keep the gain precisely at 3. Zener diodes or thermistors are commonly used in the negative feedback path to vary the gain dynamically, ensuring the sine wave remains stable without clipping."
      },
    {
     "question":("The op-amp in a standard Wien Bridge oscillator configuration is used as a:"),
     "options": [
         "Voltage Follower.",
          "Comparator.",
         "Inverting Amplifier.",
         "Non-Inverting Amplifier"
         ],
       "correct_option_index": 3,
      "explanation":"The Wien Bridge is connected to the non-inverting input ($+$), and the output is fed back to the inverting input ($-$) via $R_F$ and $R_1$. This configuration is a **non-inverting amplifier**, which provides the required $\mathbf{0^\circ}$ phase shift." 
     }
    
]




# --- Prelab Tab ---
with tab1:
    st.header("Prelab")
    st.markdown("""
    **Objective:** To understand the operation of a Wien bridge oscillator and verify the conditions for sustained oscillation.

    **Pre-requisites:**
    1.  Knowledge of operational amplifiers (op-amps).
    2.  Understanding of resistor-capacitor (RC) networks and their phase shifting properties.
    3.  Familiarity with the Barkhausen criterion for oscillation.
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
 ### Theory: Wien Bridge Oscillator

 A **Wien Bridge Oscillator** is a standard type of electronic oscillator widely used to generate **high-quality sine wave outputs** over a wide frequency range. It is distinguished by its use of a **frequency-selective Wien Bridge network** within the feedback loop of a non-inverting amplifier.

 ---

 ### Principle of Operation
 The circuit operates based on the **Barkhausen Criterion**, which states that for sustained oscillations to occur, two conditions must be met:
 1. The **loop gain** ($A\beta$) must be equal to or greater than unity ($\mathbf{|A\beta| \ge 1}$).
 2. The **total phase shift** around the feedback loop must be $0^\circ$ or $360^\circ$ ($\mathbf{\angle A\beta = 0^\circ \text{ or } 360^\circ}$).

---

 ### Wien Bridge Network (Feedback)
 The Wien Bridge network forms the **positive feedback** path and is composed of a series $RC$ arm and a parallel $RC$ arm.
 * **Phase Shift:** At the resonant frequency ($f_o$), the network acts as a band-pass filter and introduces a phase shift of exactly **$0^\circ$** (or $360^\circ$). This is critical because the amplifier is used in a non-inverting configuration, which also provides a $0^\circ$ phase shift.
 * **Attenuation ($\beta$):** At $f_o$, the network's attenuation ($\beta$) is exactly $\mathbf{1/3}$.

 ---

 ### The Amplifier
 The amplifier stage is typically a **non-inverting op-amp**, which provides a **$0^\circ$ phase shift** between its input and output.
 * **Minimum Gain:** To satisfy the loop gain criterion $|A\beta| \ge 1$ with $\beta = 1/3$, the minimum amplifier gain required is:
    $$\mathbf{A_v \ge 3}$$
 * **Gain Control:** To achieve amplitude stability and a pure sine wave, the gain is often set slightly above 3 to initiate oscillation, then reduced to exactly 3 using an **Automatic Gain Control (AGC)** mechanism (e.g., a thermistor or JFET).

 ---

 ### Frequency of Oscillation
 The oscillation frequency ($\mathbf{f_o}$) is determined by the values of $R$ and $C$ in the frequency-selective arms, assuming $R_{\text{series}} = R_{\text{parallel}} = R$ and $C_{\text{series}} = C_{\text{parallel}} = C$:
 $$\mathbf{f_o = \frac{1}{2 \pi R C}}$$

 The amplifier gain ($A_v$) required for sustained oscillation is set by the ratio of the feedback resistors $R_F$ and $R_1$:
 $$\mathbf{A_v = 1 + \frac{R_F}{R_1} \ge 3}$$
 """)

# --- Simulation Tab ---
with tab3:
    # --- Layout with Columns ---
    # col1 for RC parameters and desired frequency, col2 for CRO display.
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Oscillator Parameters")

        # Number input for Resistance (R) in kΩ.
        R_kohm = st.number_input(
            "Resistance (R) (kΩ)",
            min_value=0.001, # R cannot be zero
            value=10.0,
            step=0.1,
            format="%.3f",
            key="R_input_wien"
        )

        # Number input for Capacitance (C) in µF.
        C_uF = st.number_input(
            "Capacitance (C) (µF)",
            min_value=0.0001, # C cannot be zero
            value=0.1,
            step=0.001,
            format="%.5f",
            key="C_input_wien"
        )

        # Number input for Desired Signal Frequency.
        f_desired = st.number_input(
            "Desired Signal Frequency (Hz)",
            min_value=0.0, # Can be 0 for a theoretical check, but practical oscillators need >0 Hz
            value=100.0,
            step=1.0,
            format="%.1f",
            key="f_desired_input_wien"
        )

        st.markdown("---") # Horizontal line for visual separation.
        st.write("Developed by DAMODAR")


    # --- Core Simulation Logic ---
    def calculate_oscillation_parameters(R_kohm, C_uF, f_desired):
        """
        Calculates the oscillation frequency, generates the output waveform,
        and determines amplifier resistor values for a Wien Bridge oscillator.
        """
        R_ohms = R_kohm * 1000 # Convert R to Ohms
        C_farads = C_uF * 1e-6 # Convert C to Farads

        f_observed = 0.0
        R_calculated_kohm_for_desired = 0.0
        R1_kohm_amp = 0.0
        RF_kohm_amp = 0.0
        
        # Calculate the observed oscillation frequency based on R and C inputs for Wien Bridge
        if R_ohms > 0 and C_farads > 0:
            try:
                f_observed = 1 / (2 * np.pi * R_ohms * C_farads)
            except ZeroDivisionError:
                st.error("R or C cannot be zero for frequency calculation.")
                f_observed = 0.0
        else:
            st.warning("Resistance (R) and Capacitance (C) must be positive for oscillation.")
            f_observed = 0.0

        # Calculate the R value needed to achieve the desired frequency with the given C
        if f_desired > 0 and C_farads > 0:
            try:
                R_calc_ohms_for_desired = 1 / (2 * np.pi * f_desired * C_farads)
                R_calculated_kohm_for_desired = R_calc_ohms_for_desired / 1000
            except ZeroDivisionError:
                st.error("Desired frequency or capacitance cannot be zero for R calculation.")
                R_calculated_kohm_for_desired = 0.0
        else:
            R_calculated_kohm_for_desired = 0.0 # If desired freq or C is zero, R is undefined/infinite

        # Amplifier resistor calculations for a gain of 3 (minimum for sustained oscillation)
        # For a non-inverting amplifier, Gain = 1 + RF/R1. We need Gain >= 3, so RF/R1 >= 2.
        # The original Tkinter code used R1_kohm_amp = 10 and RF_kohm_amp = 2 * R1_kohm_amp.
        # This gives a gain of 1 + (2*R1)/R1 = 3, which is correct for Wien Bridge.
        
        R1_kohm_amp = 10.0 # Default R1 for amplifier (as per original Tkinter code)
        RF_kohm_amp = 2 * R1_kohm_amp # Feedback resistor for gain of 3 (RF/R1 = 2)

        # Generate the output waveform (sine wave at the observed frequency)
        num_cycles = 5 # Display 5 cycles for clarity
        amp = 1.0 # Ideal oscillator amplitude (can be expanded to model saturation)
        
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
            "output_amplitude": amp, # The simulated output amplitude
            "time_period_s": time_period,
            "f_output": f_observed,
            "R_calculated_kohm_for_desired": R_calculated_kohm_for_desired,
            "R1_kohm_amp": R1_kohm_amp,
            "RF_kohm_amp": RF_kohm_amp,
            "y_signal": y_signal,
            "t_time": t,
            "total_duration": total_duration
        }

    # --- CRO Display and Simulation Results ---
    with col2:
        st.header("Circuit Diagram")
        
        st.image("images/wienbridgeoscillator.png", caption="RC Phaseshift Oscillator Circuit", width='stretch')
        
        
        st.subheader("CRO Display")
        st.text_input("Your Name",key="p2")
        # Perform the simulation based on current widget values.
        sim_results = calculate_oscillation_parameters(R_kohm, C_uF, f_desired)

        # Plotting for Output Signal (CH1)
        fig1, ax1 = plt.subplots(figsize=(6, 3), dpi=100) # Larger plot for better visibility
        ax1.plot(sim_results["t_time"], sim_results["y_signal"], color='red')
        ax1.set_title("Oscillator Output Signal")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Amplitude (V)")
        ax1.grid(True)
        ax1.set_facecolor("black") # Set background to black
        ax1.axhline(0, color='gray', linewidth=0.5)
        ax1.axvline(0, color='gray', linewidth=0.5)
        
        # Set Y-axis limits based on the output amplitude, with some padding.
        plot_ylim = sim_results["output_amplitude"] * 1.5 if sim_results["output_amplitude"] != 0 else 1.0
        ax1.set_ylim(-plot_ylim, plot_ylim)
        ax1.set_xlim(0, sim_results["total_duration"])
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        
        ax1.text(0.02, 0.95, f'Amp: {sim_results["output_amplitude"]:.2f} V', transform=ax1.transAxes,
                 fontsize=8, color='white', verticalalignment='top')
        ax1.text(0.02, 0.85, f'Freq: {sim_results["f_output"]:.2f} Hz', transform=ax1.transAxes,
                 fontsize=8, color='white', verticalalignment='top')

        st.pyplot(fig1) # Display the Matplotlib figure in Streamlit.

    st.header("Simulation Results")

        # Initialize session state for history if it doesn't exist.
    if 'oscillator_history_wien' not in st.session_state: # Unique key for this page's history
            st.session_state.oscillator_history_wien = []

        # Button to log the current result to the table.
    if st.button("Log Current Results to Table", key="log_button_wien"):
            new_entry = {
                "Input R (kΩ)": f"{sim_results['R_input_kohm']:.2f}",
                "Input C (µF)": f"{sim_results['C_input_uF']:.2f}",
                "Desired Freq (Hz)": f"{sim_results['f_desired']:.2f}",
                "Output Amp (V)": f"{sim_results['output_amplitude']:.2f}",
                "Time Period (s)": f"{sim_results['time_period_s']:.4f}",
                "Output Freq (Hz)": f"{sim_results['f_output']:.2f}",
                "Calc. R for F_des (kΩ)": f"{sim_results['R_calculated_kohm_for_desired']:.2f}",
                "Amp R1 (kΩ)": f"{sim_results['R1_kohm_amp']:.2f}",
                "Amp RF (kΩ)": f"{sim_results['RF_kohm_amp']:.2f}"
            }
            st.session_state.oscillator_history_wien.append(new_entry)

        # Display the history as a Pandas DataFrame.
    if st.session_state.oscillator_history_wien:
            df_history = pd.DataFrame(st.session_state.oscillator_history_wien)
            st.dataframe(df_history, width='stretch') # use_container_width makes the table responsive.

        # Button to clear the table history.
    if st.button("Clear Table History", key="clear_table_button_wien"):
            st.session_state.oscillator_history_wien = [] # Reset the history list.
            st.rerun() # Rerun the app to immediately reflect the cleared table.

# --- Postlab Tab ---
with tab4:
    st.header("Postlab")
    st.text_input("Your Name",key="p3")
    st.subheader("Conclusion:")
    st.write("Summarize your observations from the simulation, focusing on the relationship between R, C (in the series and parallel arms of the bridge), and the output frequency.")
    st.text_area("Your Answer ", height=100, key="postlab_q1")
    st.write("Explain how the calculated amplifier resistor values (R1 and RF) are related to the required gain.")
    st.text_area("Your Answer ", height=100, key="postlab_q2")
    st.write(" Discuss the limitations of this ideal simulation compared to a real-world circuit.")
    st.text_area("Your Answer ", height=100, key="postlab_q3")

    st.subheader("Analysis:")
    st.write("Using the formula, calculate the required R and C values for a 1 KHz oscillation.")
    st.text_area("Your Answer ", height=100, key="postlab_q4")
    st.write("If the input R is 10kΩ and C is 0.01µF, what is the output frequency?")
    st.text_area("Your Answer ", height=100, key="postlab_q5")
    st.write("What are some advantages and disadvantages of using an Wien bridge oscillator?")
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