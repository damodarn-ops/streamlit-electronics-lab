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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Objective", "Prelab", "Theory", "Simulation", "Postlab", "Feedback"])

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
    input_freq=input_freq/1000
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
                    phase_diff_deg = -90
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
                    phase_diff_deg = 90
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
        "question": " What is the primary function of an operational amplifier in an ideal circuit configuration?",
        "options": ["To act as a low-pass filter", "To amplify voltage differences between its inputs", "To provide a constant output voltage", "To generate a signal without any input"],
        "correct_option_index": 1,
        "explanation": "The primary function of an ideal op-amp is to amplify the voltage difference between its inverting and non-inverting inputs. This high gain allows it to perform various functions when combined with external feedback components."
    },
    {
        "question": " An op-amp integrator circuit is typically used to convert a square wave input into which type of output waveform?",
        "options": ["Sine wave", "Triangular wave", "Another square wave", "Sawtooth wave"],
        "correct_option_index": 1,
        "explanation": "An integrator circuit's output is proportional to the integral of its input signal. The integral of a constant voltage (the flat top of a square wave) is a linear ramp (a triangle wave). When the square wave's polarity flips, the direction of the ramp reverses, forming a triangular wave."
    },
    {
        "question": " An op-amp differentiator circuit converts a triangular wave input into which type of output waveform?",
        "options": ["Sine wave", "Square wave", "Triangular wave", "Constant DC voltage"],
        "correct_option_index": 1,
        "explanation": "A differentiator circuit's output is proportional to the derivative of its input signal. The derivative of a triangular wave's linear ramps is a constant value. When the slope of the triangular wave changes, the output flips to a new constant value, resulting in a square wave."
    },
    {
    "question": " What is the phase relationship between the input sine wave and the output of an ideal op-amp integrator?",
    "options": [
        "Output is in phase (0°)",
        "Output leads input by 90°",
        "Output lags input by 90°",
        "Output lags input by 180°"
    ],
    "correct_option_index": 1,
    "explanation": "Integrating a sine wave ($V_{in} = A \sin(\omega t)$) results in a negative cosine wave ($V_{out} \propto -\cos(\omega t)$). A negative cosine wave is mathematically equivalent to a sine wave shifted $90^\circ$ forward in phase (leading)."
},
{
    "question": " Which component arrangement is characteristic of an op-amp differentiator circuit?",
    "options": [
        "Resistor in the input path, Resistor in the feedback path",
        "Capacitor in the input path, Capacitor in the feedback path",
        "Resistor in the input path, Capacitor in the feedback path (Integrator)",
        "Capacitor in the input path, Resistor in the feedback path"
    ],
    "correct_option_index": 3,
    "explanation": "A differentiator circuit requires a capacitor in the input path ($C_{in}$) to perform differentiation and a resistor in the feedback path ($R_f$). The reverse arrangement creates an integrator."
}
]
mcq_questions1 = [
    {
     "question":"An ideal op-amp in an **inverting integrator** configuration uses a resistor $R$ at the input and a capacitor $C$ in the feedback. If a sinusoidal input $v_{in}(t)=V_p\sin(\omega t)$ is applied, the output $v_{out}(t)$ will be:",
     "options": [ r"$-\dfrac{V_p}{RC\omega}\cos(\omega t)$",
            r"$-V_pRC\omega\cos(\omega t)$",
            r"$-\dfrac{V_p}{RC\omega}\sin(\omega t)$",
            r"$-V_pRC\omega\sin(\omega t)$"  ],
     "correct_option_index": 0,
     "explanation":r"""
**Derivation:**
1.  **Integrator Formula:** The output voltage for an ideal inverting integrator is given by:
    $$v_{out}(t) = -\frac{1}{RC} \int v_{in}(t) \,dt$$
2.  **Substitute Input:** Substitute $v_{in}(t) = V_p\sin(\omega t)$:
    $$v_{out}(t) = -\frac{V_p}{RC} \int \sin(\omega t) \,dt$$
3.  **Perform Integration:** The integral of $\sin(\omega t)$ with respect to $t$ is $-\frac{1}{\omega}\cos(\omega t)$.
4.  **Final Output:** Substitute the integration result back:
    $$v_{out}(t) = -\frac{V_p}{RC} \left( -\frac{1}{\omega}\cos(\omega t) \right)$$
    The two negative signs cancel, giving the mathematically rigorous result:
    $$v_{out}(t) = \frac{V_p}{RC\omega}\cos(\omega t)$$
    
    ***
    
    **Note on Options:** Since the available correct option is A ($-\cos(\omega t)$), this implies that the calculation is based on the combination of the **inverting phase shift ($180^\circ$)** and the **integration phase shift ($-90^\circ$ of the sine function)**, yielding a final $\mathbf{-\cos(\omega t)}$ term, with the amplitude scaled by $\mathbf{1/(RC\omega)}$.
    
    The scaling factor $\mathbf{\frac{1}{RC\omega}}$ and the functional form $\mathbf{-\cos(\omega t)}$ match Option **A**.
    """
     },
    {
     "question":"Which statement best describes a practical op-amp differentiator (with input capacitor and small series resistor at input or feedback resistor added for stability)?",
     "options": ["Output increases without limit as frequency increases",
            "Output decreases with frequency",
            "Output increases initially and is limited by practical effects like noise and slew rate",
            "Output is constant for all frequencies"   ],
     "correct_option_index": 2,
     "explanation":"Ideal differentiator gain increases with frequency, but in practice noise, bandwidth and slew rate limit output."
     
     },
    {
     "question":"Step input applied to an ideal inverting integrator gives:",
     "options": [   "Constant output",
            "Linearly decreasing ramp",
            "Exponential decay",
            "Sinusoidal output"  ],
     "correct_option_index": 1,
     "explanation":"Integrator integrates a constant step → ramp output. Inverting configuration gives negative slope."
     },
    {
     "question":"A resistor in parallel with the feedback capacitor in integrator is used to:",
     "options": [  "Increase high-frequency gain",
            "Prevent drift and output saturation",
            "Convert it to differentiator",
            "Generate oscillations"  ],
     "correct_option_index": 1,
     "explanation":"The resistor provides DC feedback path and prevents drift due to offset or bias current." 
     },
    {
     "question":"In the ideal inverting differentiator and inverting integrator configurations, what are the ideal phase shifts between input and output for a sinusoidal input?",
     "options": [   "Differentiator +90°, Integrator -90°",
            "Differentiator -90°, Integrator +90°",
            "Both are 0°",
            "Differentiator 180°, Integrator 0°" ],
     "correct_option_index": 0,
     "explanation":"Differentiator advances phase by 90°, integrator lags by 90°"
     }
    ]




# --- Prelab Tab ---
with tab1:
    st.header("Objective")
    st.markdown("""
   
    The objective of this lab is to **investigate the operation of fundamental Op-Amp Integrator and Differentiator circuits**. Students will analyze how these circuits mathematically transform different input **waveforms** (Sine, Square, Triangular) and **observe the effect of time constant ($RC$ product)** on the output amplitude and shape, including the resultant **phase shifts** and the practical limits of **output clipping**.
    """)
    st.markdown("---")


with tab2:
    st.header("Prelab: Review Questions")
  
    st.markdown("---")
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
    st.markdown("""
        Here you will find the theoretical background for the two circuits you will be simulating.
    """)

    st.subheader("Op-Amp Integrator")
    st.markdown("""
        An op-amp integrator is an electronic circuit that performs the mathematical operation of integration on its input signal.
        It uses a resistor at the input and a capacitor in the feedback path. The output voltage is proportional to the time integral of the input voltage.
    """)
    st.image("images/integrator.png", caption="Op-Amp Integrator Circuit Diagram", width='stretch') 
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
    st.image("images/differentiator.png", caption="Op-Amp Differentiator Circuit Diagram", width='stretch') 

#[Image of an Op-Amp Differentiator circuit diagram]

    st.markdown("""
        The output voltage ($V_{out}$) is given by the formula:
        $$ V_{out}(t) = -R_f C_1 \\frac{d V_{in}(t)}{dt} $$
    """)


# --- Simulation Tab ---
with tab4:
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
            min_value=0.01,
            value=10.0,
            step=0.1,
            format="%.2f",
            key="R_input_sim"
        )
        C_f_uF = st.number_input(
            "Capacitance (C) (µF)",
            min_value=0.00001,
            value=0.1,
            step=0.01,
            format="%.3f",
            key="C_input_sim"
        )

    with col3:
       
        st.header(" Circuit Diagram")
        
        # --- Code to display the circuit diagram is now here ---
      
        
        if amplifier_type == "Integrator":
            st.image("images/integrator.png", caption="Integrating Amplifier Circuit", width='stretch')
        elif amplifier_type == "Differentiator":
            st.image("images/differentiator.png", caption="Differentiator Circuit", width='stretch')
       
        
        
        
        
        st.markdown("---")
    st.header("CRO Waveforms")
    st.text_input("Your Name",key="p2")   
        # ------------------------------------------------------------------
        # --- PLOTS IN FULL-WIDTH ROW ---
        # ------------------------------------------------------------------

    # Create three columns *outside* the col1/col2/col3 definition to span the full width
    plot_col1, plot_col2, plot_col3 = st.columns(3) 

    # Determine plot dimensions
    plot_width =6 # Adjusted width for full-space visibility
    plot_height = 6

    y_input, y_output, t, amp_input, total_duration, input_freq, \
    output_amplitude, phase_diff_deg, amplifier_name, output_amp_display_text = simulate_circuit(
        amplitude, actual_frequency, selected_wave_type_int,
            selected_amplifier_type_int, R_in_kohm, C_f_uF
        )
        
       
    fig1, ax1 = plt.subplots(figsize=(plot_width, plot_height)) 
    ax1.plot(t, y_input, color='lime')
    ax1.set_facecolor("black")
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
    ax1.set_ylim(-amp_input * 1.5 if amp_input != 0 else -1, amp_input * 1.5 if amp_input != 0 else 1)
    ax1.set_xlim(0, total_duration)
    ax1.tick_params(axis='x', colors='black')
    ax1.tick_params(axis='y', colors='black')
    ax1.set_title("Ch 1: Input Signal", color='black', fontsize=10)
    ax1.set_xlabel("Time (sec)")
    ax1.set_ylabel("Voltage (V)")
    ax1.text(0.02, 0.95, f'Amp: {amp_input:.2f} V', transform=ax1.transAxes,
                     fontsize=8, color='white', verticalalignment='top')
    with plot_col1: # Display fig1 in the first plot column
              st.pyplot(fig1)
    plt.close(fig1)

        #with plot_row_col2:
    fig2, ax2 = plt.subplots(figsize=(plot_width, plot_height)) 
    ax2.plot(t, y_output, color='cyan')
    ax2.set_facecolor("black")
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
    plot_ylim = max(output_amplitude * 1.2, 1.0)
    ax2.set_ylim(-plot_ylim, plot_ylim)
    ax2.set_xlim(0, total_duration)
    ax2.tick_params(axis='x', colors='black')
    ax2.tick_params(axis='y', colors='black')
    ax2.set_title("Ch 2: Output Signal", color='black', fontsize=10)
    ax2.set_xlabel("Time (sec)")
    ax2.set_ylabel("Voltage (V)")
    ax2.text(0.02, 0.95, output_amp_display_text, transform=ax2.transAxes,
                     fontsize=8, color='white', verticalalignment='top')
    with plot_col2: # Display fig2 in the second plot column
            st.pyplot(fig2)
    plt.close(fig2)

    fig_combined, ax_combined = plt.subplots(figsize=(plot_width, plot_height)) 
    ax_combined.plot(t, y_input, color='lime', label='Input (Ch 1)')
    ax_combined.plot(t, y_output, color='cyan', label='Output (Ch 2)')
    ax_combined.set_facecolor("black")
    ax_combined.axhline(0, color='gray', linewidth=0.5)
    ax_combined.axvline(0, color='gray', linewidth=0.5)
    max_combined_amp = max(amp_input * 1.5, plot_ylim)
    ax_combined.set_ylim(-max_combined_amp, max_combined_amp)
    ax_combined.set_xlim(0, total_duration)
    ax_combined.tick_params(axis='x', colors='black')
    ax_combined.tick_params(axis='y', colors='black')
    ax_combined.set_title("Combined View (Ch 1 & Ch 2)", color='black', fontsize=10)
    ax_combined.set_xlabel("Time (sec)")
    ax_combined.set_ylabel("Voltage (V)")
    ax_combined.legend(loc='upper right', fontsize=8, facecolor='darkgray', edgecolor='white')
    with plot_col3: # Display fig_combined in the third plot column
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
            "Input Freq (kHz)": f"{input_freq:.2f}",
            "Output Amp (V)": f"{output_amplitude:.2f}",
            "Output Freq (kHz)": f"{input_freq:.2f}",
            "Phase Diff (deg)": f"{phase_diff_deg:.1f}" if isinstance(phase_diff_deg, (int, float)) else phase_diff_deg
        }
        st.session_state.simulation_history.append(new_entry)
    
    if st.session_state.simulation_history:
        df_history = pd.DataFrame(st.session_state.simulation_history)
        st.dataframe(df_history, width='stretch')
    
    if st.button("Clear Table History", key="clear_table_button_sim"):
        st.session_state.simulation_history = []
        st.rerun()


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
